# How to Use

## Step 1: Clone the Repository

```bash
git clone https://github.com/Sachin-Rathore-1234/redrob-hackathon.git
cd redrob-hackathon
```

## Step 2: Create a Virtual Environment

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

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Add the Official Dataset

The repository does **not** include the official candidate dataset.

Place the provided dataset at:

```
data/candidates.jsonl
```

---

# First-Time Setup (Offline Preprocessing)

Run the following commands **once** for every new candidate dataset:

```bash
python -m pipelines.offline.build_embeddings
python -m pipelines.offline.build_faiss
python -m pipelines.offline.build_bm25
python -m pipelines.offline.build_query_embedding
```

These commands generate reusable artifacts including:

- Candidate embeddings
- FAISS index
- BM25 index
- Feature tables
- Query embedding

---

# Runtime Information

The offline preprocessing stage computes embeddings for the **entire candidate dataset**.

For a dataset of approximately **100,000 resumes (≈465 MB)**, this step may take **20–60 minutes** on a CPU-only machine depending on hardware.

This is expected and only needs to be performed **once per dataset**.

If the artifacts already exist and the dataset has not changed, rerunning:

```bash
python -m pipelines.offline.build_embeddings
```

will immediately detect the cached artifacts and skip rebuilding.

Example:

```
Counting candidates...
Candidates = 100000
Embedding artifacts are current; skipping rebuild.
```

---

# Running the Ranker (Online)

After preprocessing has completed, generate the submission CSV:

```bash
python rank.py --out outputs/submission.csv
```

The online ranking pipeline:

- loads cached embeddings
- loads the FAISS index
- loads the BM25 index
- embeds only the job description
- retrieves candidates
- computes semantic and feature scores
- generates the final Top-100 ranking

No candidate embeddings are recomputed during ranking.

---

# Competition Runtime Requirement

The Redrob Hackathon specifies that the **ranking pipeline** should execute within **5 minutes on CPU**.

This repository satisfies that requirement by separating the workflow into:

### Offline (one-time)

- Build embeddings
- Build FAISS
- Build BM25
- Build query embedding

These preprocessing steps may take longer than five minutes for large datasets because embeddings are generated for every candidate.

### Online (every ranking request)

```bash
python rank.py --out outputs/submission.csv
```

The online ranking stage reuses the cached artifacts and completes in only a few seconds on a typical CPU, satisfying the competition runtime requirement.

---

# Output

Running

```bash
python rank.py --out outputs/submission.csv
```

produces a CSV with the required format:

```
candidate_id,rank,score,reasoning
```

The output contains:

- Exactly 100 ranked candidates
- Unique candidate IDs
- Ranks from 1 to 100
- Scores in descending order
- Explainable reasoning for each candidate
