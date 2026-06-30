import argparse
import json
import sys
from pathlib import Path

import numpy as np
from docx import Document

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from config import (
    CANDIDATES_PATH,
    DEFAULT_SUBMISSION_PATH,
    EMBEDDINGS_PATH,
    FINAL_TOP_K,
    JD_EMBEDDING_PATH,
    JOB_DESCRIPTION_PATH,
)

from modules.embedding import get_embedding_model
from modules.jd_parser import parse_jd
from modules.ranker import CandidateRanker
from modules.retrieve import retrieve_candidates
from modules.submission import (
    build_reasoning,
    validate_submission_rows,
    write_submission,
)
from utils.helper import parse_candidate


def load_jd(job_description_path):
    doc = Document(job_description_path)

    jd_text = "\n".join(
        p.text
        for p in doc.paragraphs
        if p.text.strip()
    )

    return parse_jd(jd_text)


def load_or_create_jd_embedding(jd, job_description_path):
    if (
        Path(job_description_path).resolve()
        == JOB_DESCRIPTION_PATH.resolve()
        and JD_EMBEDDING_PATH.exists()
    ):
        embedding = np.load(JD_EMBEDDING_PATH)
        return embedding.reshape(1, -1).astype(np.float32)

    model = get_embedding_model()
    return model.encode(
        [jd.raw_text],
        normalize_embeddings=True,
    ).astype(np.float32)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Rank candidates and write a Redrob submission CSV."
    )
    parser.add_argument(
        "--candidates",
        type=Path,
        default=CANDIDATES_PATH,
        help="Path to candidates.jsonl.",
    )
    parser.add_argument(
        "--job-description",
        type=Path,
        default=JOB_DESCRIPTION_PATH,
        help="Path to job_description.docx.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_SUBMISSION_PATH,
        help="Path to write the submission CSV.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=FINAL_TOP_K,
        help="Number of ranked candidates to write.",
    )
    return parser.parse_args()


def main(
    candidates_path=CANDIDATES_PATH,
    job_description_path=JOB_DESCRIPTION_PATH,
    output_path=DEFAULT_SUBMISSION_PATH,
    top_k=FINAL_TOP_K,
):
    print("Loading embeddings...")
    embeddings = np.load(EMBEDDINGS_PATH)

    jd = load_jd(job_description_path)
    jd_embedding = load_or_create_jd_embedding(
        jd,
        job_description_path,
    )

    print("Retrieving candidate shortlist...")
    candidate_indices = set(
        retrieve_candidates(
            jd.raw_text,
            query_embedding=jd_embedding,
        )
    )

    ranker = CandidateRanker(
        jd,
        jd_embedding=jd_embedding.reshape(-1),
    )

    results = []

    print("Scoring candidates...")

    with open(candidates_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if idx not in candidate_indices:
                continue

            candidate = parse_candidate(
                json.loads(line)
            )

            candidate_embedding = embeddings[idx]

            result = ranker.score(
                candidate,
                candidate_embedding,
            )
            result["reasoning"] = build_reasoning(
                jd,
                candidate,
                result,
            )

            results.append(result)

    results.sort(
        key=lambda x: (
            -x["final_score"],
            x["candidate_id"],
        ),
    )

    rows = write_submission(
        results,
        output_path,
        top_k,
    )
    validate_submission_rows(
        rows,
        top_k,
    )

    print("Submission written:", output_path)
    return rows


if __name__ == "__main__":
    args = parse_args()
    main(
        candidates_path=args.candidates,
        job_description_path=args.job_description,
        output_path=args.out,
        top_k=args.top_k,
    )
