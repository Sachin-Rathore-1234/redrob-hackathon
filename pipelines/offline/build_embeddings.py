import json
import os
import pickle
import sys
from pathlib import Path

import numpy as np
from tqdm import tqdm

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from config import (
    CANDIDATES_PATH,
    CANDIDATE_IDS_PATH,
    CANDIDATE_TEXTS_PATH,
    EMBEDDING_MODEL,
    EMBEDDINGS_PATH,
    FEATURE_TABLE_PATH,
)
from utils.helper import parse_candidate


ENCODE_BATCH_SIZE = int(os.environ.get("EMBEDDING_BATCH_SIZE", "256"))
ENCODE_CHUNK_SIZE = int(os.environ.get("EMBEDDING_CHUNK_SIZE", "4096"))
FORCE_REBUILD = os.environ.get("FORCE_REBUILD_EMBEDDINGS") == "1"


def configure_torch():
    import torch

    thread_count = min(4, os.cpu_count() or 1)
    torch.set_num_threads(thread_count)


def choose_device():
    import torch

    if torch.cuda.is_available():
        return "cuda"

    if torch.backends.mps.is_available():
        return "mps"

    return "cpu"


def count_candidates():
    with open(CANDIDATES_PATH, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def artifacts_are_current(candidate_count):
    required_paths = [
        EMBEDDINGS_PATH,
        FEATURE_TABLE_PATH,
        CANDIDATE_IDS_PATH,
        CANDIDATE_TEXTS_PATH,
    ]

    if any(not path.exists() for path in required_paths):
        return False

    candidates_mtime = CANDIDATES_PATH.stat().st_mtime

    if any(path.stat().st_mtime < candidates_mtime for path in required_paths):
        return False

    embeddings = np.load(
        EMBEDDINGS_PATH,
        mmap_mode="r",
    )

    return embeddings.shape[0] == candidate_count


def main():
    print("Counting candidates...")
    candidate_count = count_candidates()
    print("Candidates =", candidate_count)

    if not FORCE_REBUILD and artifacts_are_current(candidate_count):
        print("Embedding artifacts are current; skipping rebuild.")
        return

    if FORCE_REBUILD:
        print("FORCE_REBUILD_EMBEDDINGS=1; rebuilding artifacts.")

    configure_torch()

    candidate_ids = []
    candidate_texts = []
    feature_rows = []

    print("Parsing candidates...")
    with open(CANDIDATES_PATH, "r", encoding="utf-8") as f:
        for line in tqdm(f, total=candidate_count):
            data = json.loads(line)
            candidate = parse_candidate(data)

            candidate_ids.append(candidate.candidate_id)
            candidate_texts.append(
                candidate.text_for_embedding()
            )

            feature_rows.append(
                {
                    "candidate_id": candidate.candidate_id,
                    "years_of_experience":
                        candidate.profile.years_of_experience,
                    "current_title":
                        candidate.profile.current_title,
                    "current_company":
                        candidate.profile.current_company,
                    "num_skills":
                        len(candidate.skills),
                    "github_activity_score":
                        candidate.redrob_signals.github_activity_score,
                    "profile_completeness_score":
                        candidate.redrob_signals.profile_completeness_score,
                    "notice_period_days":
                        candidate.redrob_signals.notice_period_days,
                    "open_to_work":
                        candidate.redrob_signals.open_to_work_flag,
                }
            )

    import pandas as pd

    df = pd.DataFrame(feature_rows)

    FEATURE_TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EMBEDDINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE_IDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATE_TEXTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(FEATURE_TABLE_PATH, index=False)

    with open(CANDIDATE_IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(candidate_ids, f)

    with open(CANDIDATE_TEXTS_PATH, "wb") as f:
        pickle.dump(candidate_texts, f)

    print("Candidate texts saved.")
    print()

    device = choose_device()
    print("Loading embedding model on", device)
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(
        EMBEDDING_MODEL,
        device=device,
    )

    embedding_dimension = model.get_sentence_embedding_dimension()
    temp_embeddings_path = EMBEDDINGS_PATH.with_suffix(".npy.tmp")

    embeddings = np.lib.format.open_memmap(
        temp_embeddings_path,
        mode="w+",
        dtype=np.float32,
        shape=(candidate_count, embedding_dimension),
    )

    print("Generating embeddings in chunks...")
    print("Batch size =", ENCODE_BATCH_SIZE)
    print("Chunk size =", ENCODE_CHUNK_SIZE)

    for start in tqdm(
        range(0, candidate_count, ENCODE_CHUNK_SIZE),
        total=(candidate_count + ENCODE_CHUNK_SIZE - 1) // ENCODE_CHUNK_SIZE,
    ):
        end = min(start + ENCODE_CHUNK_SIZE, candidate_count)

        chunk_embeddings = model.encode(
            candidate_texts[start:end],
            batch_size=ENCODE_BATCH_SIZE,
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).astype(np.float32)

        embeddings[start:end] = chunk_embeddings
        embeddings.flush()

    del embeddings
    temp_embeddings_path.replace(EMBEDDINGS_PATH)

    print("Embedding shape =", (candidate_count, embedding_dimension))
    print("Embeddings saved.")
    print(df.head())
    print()
    print("Number of candidates =", len(df))


if __name__ == "__main__":
    main()
