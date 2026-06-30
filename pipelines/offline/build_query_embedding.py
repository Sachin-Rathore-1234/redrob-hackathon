import sys
from pathlib import Path

import numpy as np
from docx import Document

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from config import JD_EMBEDDING_PATH, JOB_DESCRIPTION_PATH
from modules.embedding import get_embedding_model
from modules.jd_parser import parse_jd


def load_jd_text(path):
    doc = Document(path)

    return "\n".join(
        p.text
        for p in doc.paragraphs
        if p.text.strip()
    )


def main():
    jd = parse_jd(
        load_jd_text(JOB_DESCRIPTION_PATH)
    )

    model = get_embedding_model()

    embedding = model.encode(
        [jd.raw_text],
        normalize_embeddings=True,
    ).astype(np.float32)

    JD_EMBEDDING_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.save(JD_EMBEDDING_PATH, embedding)

    print("JD embedding saved:", JD_EMBEDDING_PATH)


if __name__ == "__main__":
    main()
