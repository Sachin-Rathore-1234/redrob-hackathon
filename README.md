# Redrob Hackathon Resume Ranker

A hybrid resume ranking system for the **Redrob Senior AI Engineer Hackathon** that combines:

- Semantic Retrieval (Sentence Transformers + FAISS)
- BM25 Keyword Retrieval
- Rule-based Feature Scoring
- Candidate Ranking with Explainable Reasoning

The system returns the **Top 100 candidates** for the provided job description.

---

# Repository Structure

```
.
├── artifacts/
│   ├── dense/
│   ├── sparse/
│   └── features/
├── data/
│   ├── job_description.docx
│   ├── submission_spec.docx
│   └── candidates.jsonl          # NOT included
├── modules/
├── pipelines/
│   ├── offline/
│   └── online/
├── outputs/
├── rank.py
├── requirements.txt
└── README.md
```

---

# Setup

Clone the repository:

```bash
git clone https://github.com/Sachin-Rathore-1234/redrob-hackathon.git
cd redrob-hackathon
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Dataset

The official competition dataset is **not included** in this repository.

Place the provided candidate dataset here:

```
data/candidates.jsonl
```

The repository contains a validation check that will display a helpful error message if the dataset is missing.

---

# Offline Preprocessing

The system is intentionally divided into an **offline preprocessing stage** and an **online ranking stage**.

Run the following commands **once** after placing the dataset:

```bash
python -m pipelines.offline.build_embeddings
python -m pipelines.offline.build_faiss
python -m pipelines.offline.build_bm25
python -m pipelines.offline.build_query_embedding
```

These scripts generate reusable artifacts:

- Dense candidate embeddings
- FAISS index
- BM25 index
- Candidate feature tables
- Query embedding

These artifacts are stored inside the `artifacts/` directory.

---

# Runtime Notes

The embedding generation step computes embeddings for the **entire candidate dataset**.

For datasets containing approximately **100,000 resumes**, this preprocessing step may take **20–60 minutes** on a CPU-only laptop depending on hardware.

This behavior is expected because embeddings are generated only once.

Subsequent executions reuse the cached artifacts and therefore do **not** regenerate embeddings unless:

- the candidate dataset changes, or
- `FORCE_REBUILD_EMBEDDINGS=1` is set.

If the artifacts already exist and are up-to-date, the embedding pipeline exits immediately.

Example:

```
Counting candidates...
Candidates = 100000
Embedding artifacts are current; skipping rebuild.
```

---

# Online Ranking

Once preprocessing is complete, ranking candidates requires only:

```bash
python rank.py --out outputs/submission.csv
```

The online pipeline:

- loads cached embeddings
- loads the FAISS index
- loads the BM25 index
- embeds only the job description
- retrieves candidates
- computes semantic and feature scores
- produces the final ranking

No candidate embeddings are recomputed during ranking.

---

# Runtime Requirement

The Redrob submission specification requires the **ranking pipeline** to execute within **5 minutes on CPU**.

This repository satisfies that requirement because:

- candidate embeddings are precomputed offline
- FAISS and BM25 indices are reused
- only the job description embedding is generated during ranking

The online ranking pipeline completes in only a few seconds on a typical CPU.

---

# Output

Generate the submission CSV:

```bash
python rank.py --out outputs/submission.csv
```

Output format:

```
candidate_id,rank,score,reasoning
```

The generated file contains:

- exactly 100 rows
- unique candidate IDs
- ranks from 1–100
- non-increasing scores
- human-readable reasoning for every candidate

---

# Cached Artifacts

Generated artifacts include:

```
artifacts/
├── dense/
│   ├── embeddings.npy
│   ├── faiss.index
│   └── query_embedding.npy
├── sparse/
│   └── bm25.pkl
└── features/
    ├── candidate_ids.json
    ├── candidate_texts.pkl
    └── feature_table.parquet
```

These artifacts are reused by the ranking pipeline.

---

# Notes

- CPU-only execution
- No external APIs
- No network access required during ranking
- Compatible with Apple Silicon and x86 CPUs
- Embedding generation uses chunked batching to reduce memory usage
- Cached artifacts prevent unnecessary recomputation

---

# Submission Metadata

Before final submission, update:

```
submission_metadata.yaml
```

with your actual:

- Team information
- Contact details
- GitHub repository
- Compute environment
- Demo/Sandbox links (if applicable)

---

# Author

**Sachin Rathore**

GitHub:
https://github.com/Sachin-Rathore-1234
