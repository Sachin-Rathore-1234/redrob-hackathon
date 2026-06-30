import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from pipelines.offline.build_bm25 import main as build_bm25
from pipelines.offline.build_embeddings import main as build_embeddings
from pipelines.offline.build_faiss import main as build_faiss
from pipelines.offline.build_query_embedding import main as build_query_embedding


def main():
    build_embeddings()
    build_faiss()
    build_bm25()
    build_query_embedding()


if __name__ == "__main__":
    main()
