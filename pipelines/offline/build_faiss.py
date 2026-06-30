import sys
from pathlib import Path

import numpy as np
import faiss

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from config import (
    EMBEDDINGS_PATH,
    FAISS_INDEX_PATH
)


def main():
    print("Loading embeddings...")

    embeddings = np.load(
        EMBEDDINGS_PATH
    )

    print("Shape:", embeddings.shape)

    dimension = embeddings.shape[1]

    print("Creating FAISS index...")

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    print("Vectors indexed:", index.ntotal)

    FAISS_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(
        index,
        str(FAISS_INDEX_PATH)
    )

    print("FAISS index saved.")


if __name__ == "__main__":
    main()
