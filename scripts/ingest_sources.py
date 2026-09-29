"""Archive/register PDFs and generate immutable evidence bundles; never edit ontology claims."""
import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = "1"
VERSION = "1.26.6"


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def read(path):
    return json.loads(path.read_text())


def inside(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes project: {relative}")
    return path


def immutable(path, blob):
    if path.exists():
        if path.read_bytes() != blob:
            raise ValueError(f"Existing artifact differs; preserve it and version the pipeline: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(blob)


def save_json(path, value):
    blob = encoded(value)
    if path.exists() and path.read_bytes() == blob:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(blob)
    temporary.replace(path)


def inspect_pdf(blob):
    if not blob.startswith(b"%PDF-"):
        raise ValueError("Input is not a PDF; HTML/error responses cannot be registered")
    doc = pymupdf.open(stream=blob, filetype="pdf")
    if doc.needs_pass or not doc.page_count:
        doc.close()
        raise ValueError("Encrypted or empty PDF is unsupported")
    return doc


def register(root, input_path, record_path):
    record = read(record_path)
    required = ("id", "title", "authority", "url", "acquisition_method", "acquired_at", "version", "role")
    if any(not isinstance(record.get(k), str) or not record[k].strip() for k in required):
        raise ValueError(f"Record requires nonempty fields: {required}")
    if not re.fullmatch(r"src:[a-zA-Z0-9:_-]+", record["id"]):
        raise ValueError("Invalid source ID")
    if urlparse(record["url"]).scheme not in ("https", "http"):
        raise ValueError("Source URL must be HTTP(S)")
    date.fromisoformat(record["acquired_at"])
    blob = input_path.read_bytes()
    sha = digest(blob)
    manifest_path = root / "data/sources.json"
    manifest = read(manifest_path)
    existing = [s for s in manifest["sources"] if s["id"] == record["id"]]
    if existing:
        raise ValueError("Source ID already registered; use build for repeat runs or a new edition ID")
    with inspect_pdf(blob) as doc:
        record.update(sha256=sha, bytes=len(blob), page_count=doc.page_count,
                      pdf_metadata=doc.metadata, archive_path=f"sources/originals/{sha}.pdf",
                      acquisition_status="full-document-acquired",
                      review_status="full-document-review-pending",
                      publication_date=None, effective_date=None, superseded_date=None,
                      retrieved_date=record["acquired_at"], policy_status="applicability-review-pending")
    record.setdefault("provenance_note", "Acquisition method is supplied by the operator; hash identifies bytes, not authenticity or policy applicability.")
    # Validate and inspect everything before changing the manifest.
    immutable(root / record["archive_path"], blob)
    manifest["sources"].append(record)
    save_json(manifest_path, manifest)
    return record["id"]


def build(root):
    if pymupdf.VersionBind != VERSION:
        raise ValueError(f"Install pinned PyMuPDF {VERSION}; found {pymupdf.VersionBind}")
    manifest = read(root / "data/sources.json")
    config = read(root / "data/ingestion-config.json")
    if not isinstance(config["render_scale"], (int, float)) or not 0 < config["render_scale"] <= 4:
        raise ValueError("Render scale must be greater than zero and at most four")
    sources = manifest["sources"]
    ids = [s["id"] for s in sources]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate source IDs")
    records, plans = [], []
    for source in sources:
        if source.get("acquisition_status") != "full-document-acquired":
            continue
        blob = inside(root, source["archive_path"]).read_bytes()
        sha = digest(blob)
        if sha != source["sha256"] or len(blob) != source["bytes"]:
            raise ValueError(f"Archive integrity failure: {source['id']}")
        selected = sorted(set(config["selected_pages"].get(source["id"], [1])))
        with inspect_pdf(blob) as doc:
            if doc.page_count != source["page_count"]:
                raise ValueError("Manifest page count mismatch")
            if any(type(p) is not int or not 1 <= p <= doc.page_count for p in selected):
                raise ValueError(f"Invalid evidence page selection: {source['id']}")
            # Configuration participates in bundle identity; a new render selection preserves old bundles.
            recipe = {"pipeline": PIPELINE, "pymupdf": VERSION,
                      "selected_pages": selected, "scale": config["render_scale"]}
            recipe_hash = digest(encoded(recipe))[:16]
            prefix = f"sources/processed/{sha}/{recipe_hash}"
            pages = [{"pdf_page": i + 1, "text": p.get_text()} for i, p in enumerate(doc)]
            artifacts = {
                "pages.json": encoded({"sha256": sha, "recipe": recipe, "pages": pages}),
                "metadata.json": encoded({"sha256": sha, "bytes": len(blob),
                                          "page_count": doc.page_count, "pdf_metadata": doc.metadata}),
                "review-queue.json": encoded({"sha256": sha, "note": "Generated tasks, not review decisions. Store decisions separately.",
                    "tasks": [{"id": f"review:{sha}:page:{p['pdf_page']}",
                               "pdf_page": p["pdf_page"], "status": "pending-semantic-review",
                               "text_empty": not bool(p["text"].strip()),
                               "evidence_rendered": p["pdf_page"] in selected}
                              for p in pages]})}
            for page in selected:
                artifacts[f"page-{page}.png"] = doc[page - 1].get_pixmap(
                    matrix=pymupdf.Matrix(config["render_scale"], config["render_scale"]), alpha=False).tobytes("png")
            files = [{"path": f"{prefix}/{name}", "sha256": digest(content)}
                     for name, content in artifacts.items()]
            records.append({"source_id": source["id"], "sha256": sha,
                            "archive_path": source["archive_path"], "page_count": len(pages),
                            "selected_pages": selected, "recipe": recipe, "artifacts": files})
            plans.extend((inside(root, f"{prefix}/{name}"), content) for name, content in artifacts.items())
    # Preflight all existing outputs before writing any, then write immutable files.
    for path, content in plans:
        if path.exists() and path.read_bytes() != content:
            raise ValueError(f"Generated output changed: {path}")
    for path, content in plans:
        immutable(path, content)
    receipt = {"pipeline_version": PIPELINE, "policy_snapshot": manifest["snapshot_date"],
               "documents": records, "semantic_promotion": False}
    save_json(root / "data/ingestion-manifest.json", receipt)
    return receipt


def check(root):
    receipt = read(root / "data/ingestion-manifest.json")
    sources = read(root / "data/sources.json")
    config = read(root / "data/ingestion-config.json")
    if receipt.get("semantic_promotion") is not False or receipt["policy_snapshot"] != sources["snapshot_date"] or receipt["pipeline_version"] != PIPELINE:
        raise ValueError("Invalid receipt boundary or snapshot")
    if len({s["id"] for s in sources["sources"]}) != len(sources["sources"]):
        raise ValueError("Duplicate source IDs")
    acquired = {s["id"]: s for s in sources["sources"] if s.get("acquisition_status") == "full-document-acquired"}
    if {d["source_id"] for d in receipt["documents"]} != set(acquired) or len(receipt["documents"]) != len(acquired):
        raise ValueError("Ingestion receipt does not cover acquired sources")
    for record in receipt["documents"]:
        source = acquired[record["source_id"]]
        selected = sorted(set(config["selected_pages"].get(source["id"], [1])))
        expected_recipe = {"pipeline": PIPELINE, "pymupdf": VERSION,
                           "selected_pages": selected, "scale": config["render_scale"]}
        if record["selected_pages"] != selected or record["recipe"] != expected_recipe:
            raise ValueError("Receipt is stale relative to ingestion configuration")
        if record["archive_path"] != source["archive_path"] or record["page_count"] != source["page_count"]:
            raise ValueError("Receipt/source metadata mismatch")
        prefix = f"sources/processed/{source['sha256']}/{digest(encoded(expected_recipe))[:16]}"
        expected_paths = {f"{prefix}/{name}" for name in ["metadata.json", "pages.json", "review-queue.json"]}
        expected_paths.update(f"{prefix}/page-{page}.png" for page in selected)
        if {a["path"] for a in record["artifacts"]} != expected_paths or len(record["artifacts"]) != len(expected_paths):
            raise ValueError("Artifact inventory does not match the recipe")
        if record["sha256"] != source["sha256"]:
            raise ValueError("Receipt/source hash mismatch")
        if digest(inside(root, source["archive_path"]).read_bytes()) != record["sha256"]:
            raise ValueError("Archive hash mismatch")
        for artifact in record["artifacts"]:
            if digest(inside(root, artifact["path"]).read_bytes()) != artifact["sha256"]:
                raise ValueError(f"Artifact hash mismatch: {artifact['path']}")
        artifacts = {Path(a["path"]).name: read(inside(root, a["path"]))
                     for a in record["artifacts"] if a["path"].endswith(".json")}
        if any(a["sha256"] != source["sha256"] for a in artifacts.values()):
            raise ValueError("Embedded source hash mismatch")
        if artifacts["pages.json"]["recipe"] != expected_recipe:
            raise ValueError("Embedded recipe mismatch")
        if artifacts["metadata.json"]["page_count"] != source["page_count"] or artifacts["metadata.json"]["bytes"] != source["bytes"]:
            raise ValueError("Embedded metadata mismatch")
        pages = artifacts["pages.json"]["pages"]
        tasks = artifacts["review-queue.json"]["tasks"]
        if [p["pdf_page"] for p in pages] != list(range(1, source["page_count"] + 1)) or len(tasks) != len(pages):
            raise ValueError("Page/queue coverage mismatch")
        if any(t["status"] != "pending-semantic-review" for t in tasks):
            raise ValueError("Generated queue must not contain review decisions")
        if [t["pdf_page"] for t in tasks] != list(range(1, source["page_count"] + 1)):
            raise ValueError("Review task page sequence mismatch")
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["register", "build", "check"])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "register":
            if not args.input or not args.record:
                parser.error("register requires --input and --record")
            print("Registered:", register(args.root, args.input, args.record))
        else:
            result = build(args.root) if args.command == "build" else check(args.root)
            print(f"{args.command}: {len(result['documents'])} PDFs; "
                  f"{sum(d['page_count'] for d in result['documents'])} pages; no ontology promotion")
    except (ValueError, OSError, KeyError) as error:
        print(f"Ingestion failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
