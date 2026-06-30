import json
import pickle
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

torch.set_num_threads(1)

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


def main():
    print("Loading embedding model...")

    model = SentenceTransformer(
        EMBEDDING_MODEL,
        device="cpu"
    )

    candidate_ids = []
    candidate_texts = []
    feature_rows = []

    with open(CANDIDATES_PATH, "r", encoding="utf-8") as f:
        for line in tqdm(f):
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
    print("Starting multi-process pool...")
    pool = model.start_multi_process_pool()

    print("Generating embeddings (multi-process)...")
    embeddings = model.encode(
        candidate_texts,
        pool=pool,
        batch_size=256,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    model.stop_multi_process_pool(pool)

    print("Embedding shape =", embeddings.shape)

    np.save(
        EMBEDDINGS_PATH,
        embeddings
    )

    print("Embeddings saved.")
    print(df.head())
    print()
    print("Number of candidates =", len(df))


if __name__ == "__main__":
    main()
