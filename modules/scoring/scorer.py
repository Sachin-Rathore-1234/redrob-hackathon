from modules.scoring.semantic import semantic_scores
from modules.scoring.skill_score import compute_skill_score
from modules.scoring.experience import compute_experience_score
from modules.scoring.behavior import compute_behavior_score
from modules.scoring.availability import compute_availability_score
from modules.scoring.education import compute_education_score
from config import (
    SEMANTIC_WEIGHT,
    SKILL_WEIGHT,
    EXPERIENCE_WEIGHT,
    EDUCATION_WEIGHT,
    BEHAVIOR_WEIGHT,
    AVAILABILITY_WEIGHT,
)


class CandidateScorer:

    def __init__(
        self,
        jd,
        candidate,
        jd_embedding=None,
        candidate_embedding=None,
    ):

        self.jd = jd
        self.candidate = candidate

        self.profile = candidate.profile
        self.redrob = candidate.redrob_signals
        self.career = candidate.career_history

        self.jd_embedding = jd_embedding
        self.candidate_embedding = candidate_embedding

    # ----------------------------
    # Individual Scores
    # ----------------------------

    def semantic(self):

        if (
            self.jd_embedding is None
            or self.candidate_embedding is None
        ):
            return 0.0

        score = float(
            semantic_scores(
                self.jd_embedding,
                self.candidate_embedding.reshape(1, -1),
            )[0]
        )

        return score

    def skill(self):

        return compute_skill_score(
            self.jd,
            self.candidate.skills,
            self.redrob,
        )

    def experience(self):

        return compute_experience_score(
            self.jd,
            self.candidate,
        )

    # ----------------------------
    # Placeholder Scores
    # ----------------------------

    def education(self):
        return compute_education_score(
        self.jd,
        self.candidate,
    )

    def behavior(self):
        return compute_behavior_score(
        self.redrob
    )

    def availability(self):
        return compute_availability_score(
        self.redrob
    )

    # ----------------------------
    # Debug Breakdown
    # ----------------------------

    def breakdown(self):

        return {
            "semantic": self.semantic(),
            "skill": self.skill(),
            "experience": self.experience(),
            "education": self.education(),
            "behavior": self.behavior(),
            "availability": self.availability(),
        }

    # ----------------------------
    # Final Weighted Score
    # ----------------------------

    def final_score(self):

        scores = self.breakdown()

        total = (
            SEMANTIC_WEIGHT * scores["semantic"]
            + SKILL_WEIGHT * scores["skill"]
            + EXPERIENCE_WEIGHT * scores["experience"]
            + EDUCATION_WEIGHT * scores["education"]
            + BEHAVIOR_WEIGHT * scores["behavior"]
            + AVAILABILITY_WEIGHT * scores["availability"]
        )

        return total
