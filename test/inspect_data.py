import json

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
    first_candidate = json.loads(next(f))

print(first_candidate.keys())
print(first_candidate)