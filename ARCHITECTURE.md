# Candidate Ranking Architecture

The project is split by lifecycle so ranking does not rebuild candidate indexes
at runtime.

## Folder Layout

```text
data/
  candidates.jsonl              # source candidate feed
  job_description.docx          # fixed challenge JD

artifacts/
  dense/
    embeddings.npy              # offline candidate embeddings
    faiss.index                 # dense vector index
    job_description_embedding.npy # offline query embedding for fixed JD
  sparse/
    bm25.pkl                    # lexical BM25 index
  features/
    candidate_features.parquet  # offline candidate features
    candidate_ids.json          # row index to candidate id mapping
    candidate_texts.pkl         # text used for indexing

modules/
  retrieve.py                   # online hybrid retrieval: FAISS + BM25 + RRF
  ranker.py                     # manual scoring over retrieved shortlist
  submission.py                 # CSV writer and validator
  scoring/                      # scoring feature functions

pipelines/
  offline/
    build_embeddings.py         # parse candidates, write features and vectors
    build_faiss.py              # build dense index from embeddings
    build_bm25.py               # build sparse lexical index
    build_query_embedding.py    # cache fixed JD embedding
    build_all_indexes.py        # run all offline index builders
  online/
    rank_candidates.py          # retrieve shortlist, score, write CSV

rank.py                         # competition CLI entrypoint
```

## Runtime Flow

```text
Offline:
Candidate JSONL
-> parse/normalize
-> candidate embeddings + feature table
-> FAISS index + BM25 index
-> fixed JD embedding

Online:
Job description
-> load fixed JD embedding
-> FAISS top K and BM25 top K
-> RRF fusion
-> manual scoring on shortlist
-> outputs/submission.csv
```

## Commands

```bash
./venv/bin/python -m pipelines.offline.build_all_indexes
./venv/bin/python rank.py --out outputs/submission.csv
```

