from pathlib import Path

# ==========================================================
# Project Paths
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent

DATA_DIR = ROOT_DIR / "data"
ARTIFACT_DIR = ROOT_DIR / "artifacts"
DENSE_ARTIFACT_DIR = ARTIFACT_DIR / "dense"
SPARSE_ARTIFACT_DIR = ARTIFACT_DIR / "sparse"
FEATURE_ARTIFACT_DIR = ARTIFACT_DIR / "features"

CANDIDATES_PATH = DATA_DIR / "candidates.jsonl"
SCHEMA_PATH = DATA_DIR / "candidate_schema.json"
JOB_DESCRIPTION_PATH = DATA_DIR / "job_description.docx"

# ==========================================================
# Embedding Model
# ==========================================================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# ==========================================================
# Retrieval Parameters
# ==========================================================

BM25_TOP_K = 700
FAISS_TOP_K = 700

FINAL_RETRIEVAL_TOP_K = 1000

# ==========================================================
# Ranking Parameters
# ==========================================================

TOP_CANDIDATES_AFTER_SCORING = 300
TOP_CANDIDATES_FOR_RERANKING = 20
FINAL_TOP_K = 100

# ==========================================================
# Score Weights
# ==========================================================

SEMANTIC_WEIGHT = 0.35
SKILL_WEIGHT = 0.25
EXPERIENCE_WEIGHT = 0.20
EDUCATION_WEIGHT = 0.10
BEHAVIOR_WEIGHT = 0.05
AVAILABILITY_WEIGHT = 0.05

# ==========================================================
# Runtime
# ==========================================================

MAX_RUNTIME_SECONDS = 300

# ==========================================================
# Artifact Files
# ==========================================================

FAISS_INDEX_PATH = DENSE_ARTIFACT_DIR / "faiss.index"
BM25_PATH = SPARSE_ARTIFACT_DIR / "bm25.pkl"

EMBEDDINGS_PATH = DENSE_ARTIFACT_DIR / "embeddings.npy"
FEATURE_TABLE_PATH = FEATURE_ARTIFACT_DIR / "candidate_features.parquet"

CANDIDATE_IDS_PATH = FEATURE_ARTIFACT_DIR / "candidate_ids.json"
CANDIDATE_TEXTS_PATH = FEATURE_ARTIFACT_DIR / "candidate_texts.pkl"
JD_EMBEDDING_PATH = DENSE_ARTIFACT_DIR / "job_description_embedding.npy"

OUTPUT_DIR = ROOT_DIR / "outputs"
DEFAULT_SUBMISSION_PATH = OUTPUT_DIR / "submission.csv"
