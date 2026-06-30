# Redrob Hackathon – Intelligent Candidate Discovery & Ranking

This repository contains our solution for the Redrob Intelligent Candidate Discovery & Ranking Challenge.

The system ranks candidates for a given Job Description using a hybrid retrieval and scoring pipeline combining:

- Dense semantic retrieval (Sentence Transformers + FAISS)
- Sparse retrieval (BM25)
- Structured feature engineering
- Learning-to-Rank (LightGBM)
- Rule-based business signals

---

# Repository Structure

```
.
├── data/
│   ├── candidates.jsonl          # Place the released dataset here
│   ├── job_description.txt
│   └── ...
│
├── artifacts/
│   ├── dense/
│   ├── bm25/
│   ├── features/
│   └── ...
│
├── pipelines/
│   ├── offline/
│   │   ├── build_embeddings.py
│   │   ├── build_faiss.py
│   │   ├── build_bm25.py
│   │   └── ...
│   │
│   └── online/
│       └── ...
│
├── rank.py
├── requirements.txt
└── submission_metadata.yaml
```

---

# Requirements

- Python 3.11
- CPU only
- macOS / Linux

Create a virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Dataset

The released dataset is **not included** in this repository.

Download the official hackathon dataset and place

```
candidates.jsonl
```

inside

```
data/
```

Result:

```
data/
    candidates.jsonl
```

---

# Offline Precomputation

The following scripts build reusable artifacts.

These are **offline preprocessing steps** and are **NOT part of the online ranking runtime**.

## 1. Build candidate embeddings

```bash
python -m pipelines.offline.build_embeddings
```

## 2. Build FAISS index

```bash
python -m pipelines.offline.build_faiss
```

## 3. Build BM25 index

```bash
python -m pipelines.offline.build_bm25
```

These scripts generate:

- candidate embeddings
- FAISS index
- BM25 index
- engineered feature tables

The embedding builder detects existing up-to-date artifacts and skips unnecessary recomputation.

---

# Ranking (Submission Generation)

After preprocessing has completed, generate the submission:

```bash
python rank.py
```

This loads the precomputed artifacts and produces the ranked submission CSV.

---

# Runtime Notes

The Redrob competition limits the **ranking step** to:

- CPU only
- ≤16 GB RAM
- ≤5 minutes runtime
- No external API calls

This repository follows that requirement by separating expensive preprocessing from online ranking.

Offline embedding generation may take significantly longer depending on hardware.

The online ranking stage only loads cached artifacts and performs retrieval + ranking.

---

# Methodology

The ranking pipeline consists of:

1. Dense semantic retrieval using Sentence Transformers.
2. FAISS Approximate Nearest Neighbor search.
3. BM25 lexical retrieval.
4. Hybrid candidate retrieval.
5. Feature engineering using:
   - semantic similarity
   - lexical similarity
   - structured profile features
   - behavioral signals
6. Learning-to-Rank with LightGBM.
7. Final score calibration and ranking.

---

# Reproducibility

Complete workflow:

```bash
python3.11 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python -m pipelines.offline.build_embeddings

python -m pipelines.offline.build_faiss

python -m pipelines.offline.build_bm25

python rank.py
```

---

# Compute Environment

Tested on

- Apple MacBook Air M3
- 16 GB RAM
- Python 3.11
- CPU execution

---

# Notes

- No hosted LLM APIs are used during ranking.
- The online ranking stage uses only locally generated artifacts.
- Precomputation is performed once and reused for subsequent ranking runs.
