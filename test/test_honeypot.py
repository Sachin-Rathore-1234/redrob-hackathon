import json

from utils.helper import parse_candidate
from modules.honeypot import compute_risk


with open("data/candidates.jsonl") as f:
    candidate = parse_candidate(json.loads(next(f)))

print(compute_risk(candidate))