from dataclasses import dataclass
from pathlib import Path
import json
import re

DATA_DIR = Path("data")


@dataclass
class ParsedJD:
    raw_text: str

    skills: list
    keywords: list

    min_experience: float | None

    education: str | None

    work_mode: str | None


with open(DATA_DIR / "skills.txt") as f:
    SKILLS = [x.strip().lower() for x in f if x.strip()]

with open(DATA_DIR / "work_modes.json") as f:
    WORK_MODES = json.load(f)

with open(DATA_DIR / "education_keywords.json") as f:
    EDUCATION = json.load(f)

with open(DATA_DIR / "stopwords.txt") as f:
    STOPWORDS = set(x.strip().lower() for x in f)

def extract_experience(text: str):
    
    text = text.lower()

    # First look for ranges like "5-9 years" or "5 to 9 years" and extract the lower bound
    range_match = re.search(r"(\d+)\s*(?:-|to)\s*(\d+)\s*years", text)
    if range_match:
        return float(range_match.group(1))

    patterns = [
        r"(\d+)\+?\s*years",
        r"minimum\s*(\d+)",
        r"at least\s*(\d+)"
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            return float(m.group(1))

    return None

def extract_skills(text: str):
    
    text = text.lower()

    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill)

    return sorted(set(found))

def extract_education(text):
    
    text = text.lower()

    # Search in order of highest degree first to avoid shadowing
    for degree in ["phd", "master", "bachelor"]:
        aliases = EDUCATION.get(degree, [])
        for alias in aliases:
            # Avoid matching common words/verbs like "be" and "ms" as substrings/subwords
            if alias == "be":
                pattern = r"\b(b\.e\.|b\.e|be\s+degree)\b"
            elif alias == "ms":
                pattern = r"\b(m\.s\.|m\.s|ms\s+degree)\b"
            else:
                pattern = rf"\b{re.escape(alias)}\b"

            if re.search(pattern, text):
                return degree

    return None

def extract_work_mode(text):
    
    text = text.lower()

    for mode, aliases in WORK_MODES.items():

        for alias in aliases:
            # Use word boundaries to avoid matching substrings
            pattern = rf"\b{re.escape(alias)}\b"
            if re.search(pattern, text):
                return mode

    return None

def extract_keywords(text):
    
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]*", text.lower())

    keywords = []

    for w in words:

        if w not in STOPWORDS and len(w) > 2:
            keywords.append(w)

    return list(dict.fromkeys(keywords))

def parse_jd(text: str):
    
    return ParsedJD(
        raw_text=text,

        skills=extract_skills(text),

        keywords=extract_keywords(text),

        min_experience=extract_experience(text),

        education=extract_education(text),

        work_mode=extract_work_mode(text),
    )