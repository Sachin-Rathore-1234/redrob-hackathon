from collections import Counter, defaultdict
import json
import math
import pickle
import sys
from pathlib import Path

from tqdm import tqdm

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from config import BM25_PATH, CANDIDATE_TEXTS_PATH


def build_inverted_bm25(tokenized_corpus):
    doc_len = [
        len(tokens)
        for tokens in tokenized_corpus
    ]
    avgdl = sum(doc_len) / len(doc_len)

    postings = defaultdict(list)
    document_frequency = defaultdict(int)

    for doc_id, tokens in enumerate(tokenized_corpus):
        counts = Counter(tokens)

        for token, freq in counts.items():
            postings[token].append((doc_id, freq))
            document_frequency[token] += 1

    num_docs = len(tokenized_corpus)
    idf = {}

    for token, df in document_frequency.items():
        idf[token] = math.log(
            1 + (num_docs - df + 0.5) / (df + 0.5)
        )

    return {
        "kind": "inverted_bm25",
        "postings": dict(postings),
        "idf": idf,
        "doc_len": doc_len,
        "avgdl": avgdl,
        "num_docs": num_docs,
        "k1": 1.5,
        "b": 0.75,
    }


def main():
    print("Building BM25 corpus...")

    print("Loading cached candidate texts...")
    with open(CANDIDATE_TEXTS_PATH, "rb") as f:
        candidate_texts = pickle.load(f)

    print("Tokenizing corpus...")
    tokenized_corpus = [
        text.lower().split()
        for text in tqdm(candidate_texts)
    ]

    print("Creating inverted BM25 index...")

    bm25 = build_inverted_bm25(tokenized_corpus)

    BM25_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(BM25_PATH, "wb") as f:
        pickle.dump(bm25, f)

    print("BM25 index saved.")
    print("Documents:", len(tokenized_corpus))


if __name__ == "__main__":
    main()
