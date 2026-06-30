import json
import numpy as np

from utils.helper import parse_candidate
from modules.jd_parser import parse_jd
from modules.scoring.scorer import CandidateScorer

with open("data/candidates.jsonl") as f:
    candidate = parse_candidate(json.loads(next(f)))

jd = parse_jd("""
Machine Learning Engineer

Minimum 3 years experience

Python
PyTorch
Docker
AWS
""")

jd_embedding = np.random.rand(384).astype(np.float32)
candidate_embedding = np.random.rand(384).astype(np.float32)

scorer = CandidateScorer(
    jd,
    candidate,
    jd_embedding,
    candidate_embedding,
)

print(scorer.final_score())