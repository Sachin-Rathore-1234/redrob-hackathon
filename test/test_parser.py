import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import json
from utils.helper import parse_candidate

with open("data/candidates.jsonl", "r", encoding="utf-8") as f:
    first_candidate = json.loads(next(f))

candidate = parse_candidate(first_candidate)

print("Candidate ID:", candidate.candidate_id)
print("Current Title:", candidate.profile.current_title)
print("Current Company:", candidate.profile.current_company)
print("Github Score:", candidate.redrob_signals.github_activity_score)

print("\nTop Skills:")
for skill in candidate.skills[:5]:
    print("-", skill.name)

print("\nEmbedding Text Preview:")
print(candidate.text_for_embedding()[:300])