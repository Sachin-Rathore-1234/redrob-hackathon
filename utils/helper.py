from docx import Document
from modules.jd_parser import parse_jd


def parse_jd_docx(path):

    doc = Document(path)

    text = "\n".join(
        p.text
        for p in doc.paragraphs
        if p.text.strip()
    )

    return parse_jd(text)
from modules.parser import (
    Candidate,
    Profile,
    CareerEntry,
    Education,
    Skill,
    Language,
    RedrobSignals,
)


def parse_candidate(data):

    profile = Profile(**data["profile"])

    career_history = [
        CareerEntry(**entry)
        for entry in data["career_history"]
    ]

    education = [
        Education(**entry)
        for entry in data["education"]
    ]

    skills = [
        Skill(**entry)
        for entry in data["skills"]
    ]

    languages = [
        Language(**entry)
        for entry in data["languages"]
    ]

    redrob_signals = RedrobSignals(
        **data["redrob_signals"]
    )

    return Candidate(
        candidate_id=data["candidate_id"],
        profile=profile,
        career_history=career_history,
        education=education,
        skills=skills,
        certifications=data["certifications"],
        languages=languages,
        redrob_signals=redrob_signals,
    )