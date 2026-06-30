import sys
from pathlib import Path

ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

sys.path.append(
    str(ROOT_DIR)
)

from modules.retrieve import (
    retrieve_candidates
)

jd = """
Looking for an AI Engineer with
Python, NLP, LLM, LangChain,
Vector Database and RAG experience.
"""

results = retrieve_candidates(
    jd
)

print(
    "Retrieved:",
    len(results)
)

print(
    "First 20 indices:"
)

print(
    results[:20]
)