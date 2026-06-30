from modules.scoring.scorer import CandidateScorer
from modules.honeypot import compute_risk
from modules.embedding import get_embedding_model
from modules.scoring.jd_disqualifiers import compute_disqualifier_penalty
from config import (
    SEMANTIC_WEIGHT,
    SKILL_WEIGHT,
    EXPERIENCE_WEIGHT,
    EDUCATION_WEIGHT,
    BEHAVIOR_WEIGHT,
    AVAILABILITY_WEIGHT,
)


class CandidateRanker:

    def __init__(self, jd, jd_embedding=None):
        self.jd = jd

        if jd_embedding is None:
            self.model = get_embedding_model()
            self.jd_embedding = self.model.encode(
                jd.raw_text,
                normalize_embeddings=True,
            )
        else:
            self.model = None
            self.jd_embedding = jd_embedding

    def score(
        self,
        candidate,
        candidate_embedding,
    ):

        scorer = CandidateScorer(
            self.jd,
            candidate,
            self.jd_embedding,
            candidate_embedding,
        )

        breakdown = scorer.breakdown()

        manual = (
            SEMANTIC_WEIGHT * breakdown["semantic"]
            + SKILL_WEIGHT * breakdown["skill"]
            + EXPERIENCE_WEIGHT * breakdown["experience"]
            + EDUCATION_WEIGHT * breakdown["education"]
            + BEHAVIOR_WEIGHT * breakdown["behavior"]
            + AVAILABILITY_WEIGHT * breakdown["availability"]
        )

        risk = compute_risk(candidate)
        
        disqualifier_penalty = compute_disqualifier_penalty(candidate)

        final = manual * (1 - 0.30 * risk) * disqualifier_penalty

        return {
            "candidate_id": candidate.candidate_id,
            "manual_score": manual,
            "risk_score": risk,
            "final_score": final,
            "breakdown": breakdown,
        }
