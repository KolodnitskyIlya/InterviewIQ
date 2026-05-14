from __future__ import annotations
import argparse
import json
from collections.abc import Iterator
from hashlib import blake2b
from pathlib import Path
from typing import Any
from sqlalchemy.dialects.postgresql import insert
from app.db.session import SessionLocal
from app.models.question import Question

DATASET_PATH = Path(__file__).resolve().parents[3] / "dataset" / "hr_interview_questions_dataset.json"
DEFAULT_BATCH_SIZE = 1000
DATASET_CATEGORIES = {
    "adaptability",
    "career-goals",
    "conflict-resolution",
    "culture-fit",
    "leadership",
    "motivation",
    "team-collaboration",
    "work-style",
}

def iter_json_array(path: Path, chunk_size: int = 1024 * 1024) -> Iterator[dict[str, Any]]:
    decoder = json.JSONDecoder()
    buffer = ""
    position = 0
    started = False

    with path.open("r", encoding="utf-8") as file:
        eof = False

        while True:
            if position >= len(buffer) and not eof:
                chunk = file.read(chunk_size)
                if chunk:
                    buffer = buffer[position:] + chunk
                    position = 0
                else:
                    eof = True

            while position < len(buffer) and buffer[position] in " \r\n\t,":
                position += 1

            if position >= len(buffer):
                if eof:
                    return
                continue

            if not started:
                if buffer[position] != "[":
                    raise ValueError("Dataset must be a JSON array")
                started = True
                position += 1
                continue

            if buffer[position] == "]":
                return

            try:
                item, end = decoder.raw_decode(buffer, position)
            except json.JSONDecodeError:
                if eof:
                    raise
                chunk = file.read(chunk_size)
                if chunk:
                    buffer += chunk
                    continue
                eof = True
                continue

            if isinstance(item, dict):
                yield item

            position = end
            if position > chunk_size:
                buffer = buffer[position:]
                position = 0

def normalize_difficulty(value: Any) -> str:
    difficulty = str(value or "").strip().lower()
    if difficulty in {"easy", "medium", "hard"}:
        return difficulty
    return "medium"

def slugify(value: Any) -> str:
    slug = str(value or "").strip().lower().replace("&", "and")
    slug = "-".join(part for part in slug.replace("_", " ").split() if part)
    return slug

def resolve_category(item: dict[str, Any], target_category: str) -> str:
    if target_category != "dataset":
        return target_category

    category = slugify(item.get("category"))
    return category if category in DATASET_CATEGORIES else "career-goals"

def question_id(item: dict[str, Any], target_category: str) -> str:
    id_parts = []
    if target_category not in {"dataset", "hr"}:
        id_parts.append(target_category)

    id_parts.extend(
        [
            str(item.get("question", "")).strip(),
            str(item.get("category", "")).strip(),
            str(item.get("role", "")).strip(),
            str(item.get("experience", "")).strip(),
            str(item.get("difficulty", "")).strip(),
            str(item.get("source_type", "")).strip(),
        ]
    )
    raw = "|".join(
        id_parts
    )
    digest = blake2b(raw.encode("utf-8"), digest_size=12).hexdigest()
    if target_category in {"dataset", "hr"}:
        return f"qds_{digest}"
    return f"qds_{target_category[:3]}_{digest}"

def truncate(value: str, limit: int) -> str:
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "..."

def dataset_item_to_question(item: dict[str, Any], target_category: str) -> dict[str, str | None]:
    question = str(item.get("question") or "").strip()
    role = str(item.get("role") or "").strip()
    experience = str(item.get("experience") or "").strip()
    source_category = str(item.get("category") or "").strip()
    source_type = str(item.get("source_type") or "").strip()

    description_parts = []
    if role:
        description_parts.append(f"Target role: {role}.")
    if experience:
        description_parts.append(f"Experience level: {experience}.")
    if source_category:
        description_parts.append(f"Topic: {source_category}.")
    if source_type:
        description_parts.append(f"Question type: {source_type}.")

    category = resolve_category(item, target_category)

    return {
        "id": question_id(item, target_category),
        "category": category,
        "difficulty": normalize_difficulty(item.get("difficulty")),
        "target_role": truncate(role, 120) or None,
        "title": truncate(question, 255),
        "description": " ".join(description_parts) or "Practice a concise, structured HR interview answer.",
    }

def flush_batch(batch: list[dict[str, str | None]]) -> None:
    if not batch:
        return

    deduplicated = {item["id"]: item for item in batch}

    statement = insert(Question).values(list(deduplicated.values()))
    statement = statement.on_conflict_do_update(
        index_elements=[Question.id],
        set_={
            "category": statement.excluded.category,
            "difficulty": statement.excluded.difficulty,
            "target_role": statement.excluded.target_role,
            "title": statement.excluded.title,
            "description": statement.excluded.description,
        },
    )

    db = SessionLocal()
    try:
        db.execute(statement)
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def main() -> None:
    parser = argparse.ArgumentParser(description="Import HR interview dataset questions into PostgreSQL.")
    parser.add_argument("--path", type=Path, default=DATASET_PATH)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--limit", type=int, default=0, help="Import only N questions. 0 means all.")
    parser.add_argument(
        "--target-category",
        choices=["dataset", "hr", "behavioral", "technical", "system-design"],
        default="dataset",
        help="Application category to assign. Use dataset to map the source category field.",
    )
    args = parser.parse_args()

    if not args.path.exists():
        raise FileNotFoundError(f"Dataset file not found: {args.path}")

    batch: list[dict[str, str | None]] = []
    processed = 0

    for item in iter_json_array(args.path):
        if not str(item.get("question") or "").strip():
            continue

        batch.append(dataset_item_to_question(item, args.target_category))
        processed += 1

        if len(batch) >= args.batch_size:
            flush_batch(batch)
            print(f"Imported {processed} questions...")
            batch.clear()

        if args.limit and processed >= args.limit:
            break

    flush_batch(batch)
    print(f"Done. Imported or updated {processed} dataset questions.")

if __name__ == "__main__":
    main()
