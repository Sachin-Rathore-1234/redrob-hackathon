import json
import pickle
import sys
from pathlib import Path

from tqdm import tqdm

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from config import CANDIDATES_PATH, CANDIDATE_TEXTS_PATH
from utils.helper import parse_candidate


def main():
    candidate_texts = []

    with open(CANDIDATES_PATH, "r", encoding="utf-8") as f:
        for line in tqdm(f):
            candidate = parse_candidate(json.loads(line))
            candidate_texts.append(
                candidate.text_for_embedding()
            )

    CANDIDATE_TEXTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CANDIDATE_TEXTS_PATH, "wb") as f:
        pickle.dump(candidate_texts, f)

    print("Saved", len(candidate_texts), "texts")


if __name__ == "__main__":
    main()
