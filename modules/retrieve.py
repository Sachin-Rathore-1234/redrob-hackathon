from collections import defaultdict
import heapq
import pickle

import faiss
import numpy as np

from config import (
    FAISS_INDEX_PATH,
    BM25_PATH,
    FAISS_TOP_K,
    BM25_TOP_K,
    FINAL_RETRIEVAL_TOP_K,
    DATA_DIR,
)
from modules.embedding import get_embedding_model


_faiss_index = None
_bm25 = None


def get_retrieval_resources():
    global _faiss_index, _bm25

    if _faiss_index is None or _bm25 is None:
        print("Loading retrieval resources...")

        _faiss_index = faiss.read_index(
            str(FAISS_INDEX_PATH)
        )

        with open(BM25_PATH, "rb") as f:
            _bm25 = pickle.load(f)

        print("Retrieval resources loaded.")

    return _faiss_index, _bm25

def faiss_search(
    query_text=None,
    top_k=FAISS_TOP_K,
    query_embedding=None,
):
    faiss_index, _ = get_retrieval_resources()

    if query_embedding is None:
        model = get_embedding_model()
        query_embedding = model.encode(
            [query_text],
            normalize_embeddings=True
        )

    query_embedding = np.ascontiguousarray(
        query_embedding.reshape(1, -1),
        dtype=np.float32,
    )

    query_norm = np.linalg.norm(query_embedding)
    if query_norm != 0:
        query_embedding = np.ascontiguousarray(
            query_embedding / query_norm,
            dtype=np.float32,
        )

    scores, indices = faiss_index.search(
        query_embedding,
        top_k
    )

    return indices[0].tolist()


def inverted_bm25_search(bm25, query_tokens, top_k):
    postings = bm25["postings"]
    idf = bm25["idf"]
    doc_len = bm25["doc_len"]
    avgdl = bm25["avgdl"]
    k1 = bm25["k1"]
    b = bm25["b"]

    scores = defaultdict(float)

    for token in query_tokens:
        token_postings = postings.get(token)
        if not token_postings:
            continue

        token_idf = idf.get(token, 0.0)

        for doc_id, freq in token_postings:
            denominator = (
                freq
                + k1
                * (
                    1
                    - b
                    + b * doc_len[doc_id] / avgdl
                )
            )
            scores[doc_id] += (
                token_idf
                * freq
                * (k1 + 1)
                / denominator
            )

    if not scores:
        return []

    return [
        doc_id
        for doc_id, _
        in heapq.nlargest(
            top_k,
            scores.items(),
            key=lambda item: (item[1], -item[0]),
        )
    ]


def legacy_bm25_search(bm25, query_tokens, top_k):
    scores = bm25.get_scores(
        query_tokens
    )

    scores = np.array(scores)

    top_indices = np.argsort(
        scores
    )[::-1][:top_k]

    return top_indices.tolist()


def bm25_search(query_text, top_k=BM25_TOP_K):
    _, bm25 = get_retrieval_resources()

    import re
    try:
        with open(DATA_DIR / "stopwords.txt") as f:
            stopwords = set(x.strip().lower() for x in f if x.strip())
    except Exception:
        stopwords = set()

    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]*", query_text.lower())
    query_tokens = [w for w in words if w not in stopwords and len(w) > 2]

    if isinstance(bm25, dict) and bm25.get("kind") == "inverted_bm25":
        return inverted_bm25_search(
            bm25,
            query_tokens,
            top_k,
        )

    return legacy_bm25_search(
        bm25,
        query_tokens,
        top_k,
    )

def rrf_fusion(
    faiss_results,
    bm25_results,
    k=60
):

    rrf_scores = {}

    for rank, idx in enumerate(
        faiss_results
    ):
        rrf_scores[idx] = (
            rrf_scores.get(idx, 0)
            + 1 / (k + rank + 1)
        )

    for rank, idx in enumerate(
        bm25_results
    ):
        rrf_scores[idx] = (
            rrf_scores.get(idx, 0)
            + 1 / (k + rank + 1)
        )

    ranked = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        idx
        for idx, _
        in ranked[:FINAL_RETRIEVAL_TOP_K]
    ]
    
def retrieve_candidates(
    jd_text,
    query_embedding=None,
):

    faiss_results = faiss_search(
        jd_text,
        query_embedding=query_embedding,
    )

    bm25_results = bm25_search(
        jd_text
    )

    final_results = rrf_fusion(
        faiss_results,
        bm25_results
    )

    return final_results
