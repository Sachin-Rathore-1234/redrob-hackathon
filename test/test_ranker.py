import json
from docx import Document

from modules.jd_parser import parse_jd
from modules.ranker import CandidateRanker
from utils.helper import parse_candidate


# ----------------------------
# Load Job Description
# ----------------------------
doc = Document("data/job_description.docx")

jd_text = "\n".join(
    p.text
    for p in doc.paragraphs
    if p.text.strip()
)

jd = parse_jd(jd_text)


# ----------------------------
# Load First Candidate
# ----------------------------
with open("data/candidates.jsonl", "r") as f:
    candidate = parse_candidate(
        json.loads(next(f))
    )


# ----------------------------
# Rank Candidate
# ----------------------------
ranker = CandidateRanker(jd)

import numpy as np
dummy_embedding = np.random.rand(384).astype(np.float32)
result = ranker.score(candidate, dummy_embedding)

print(result)