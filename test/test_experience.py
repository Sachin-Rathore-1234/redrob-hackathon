from modules.scoring.experience import *
from utils.helper import parse_candidate
from modules.jd_parser import parse_jd
import json

with open("data/candidates.jsonl") as f:
    candidate = parse_candidate(json.loads(next(f)))

jd = parse_jd("""
Machine Learning Engineer

Minimum 3 years experience

Python
PyTorch
""")

score = compute_experience_score(
    jd,
    candidate
)

print(score)