from dataclasses import dataclass
from typing import List, Dict, Optional


# ==========================
# Profile
# ==========================
@dataclass
class Profile:
    anonymized_name: str
    headline: str
    summary: str
    location: str
    country: str
    years_of_experience: float
    current_title: str
    current_company: str
    current_company_size: str
    current_industry: str


# ==========================
# Career History
# ==========================
@dataclass
class CareerEntry:
    company: str
    title: str
    start_date: str
    end_date: Optional[str]
    duration_months: int
    is_current: bool
    industry: str
    company_size: str
    description: str


# ==========================
# Education
# ==========================
@dataclass
class Education:
    institution: str
    degree: str
    field_of_study: str
    start_year: int
    end_year: int
    grade: str
    tier: str


# ==========================
# Skill
# ==========================
@dataclass
class Skill:
    name: str
    proficiency: str
    endorsements: int
    duration_months: int


# ==========================
# Language
# ==========================
@dataclass
class Language:
    language: str
    proficiency: str


# ==========================
# Redrob Signals
# ==========================
@dataclass
class RedrobSignals:
    profile_completeness_score: float
    signup_date: str
    last_active_date: str
    open_to_work_flag: bool
    profile_views_received_30d: int
    applications_submitted_30d: int
    recruiter_response_rate: float
    avg_response_time_hours: float
    skill_assessment_scores: Dict[str, float]
    connection_count: int
    endorsements_received: int
    notice_period_days: int
    expected_salary_range_inr_lpa: Dict
    preferred_work_mode: str
    willing_to_relocate: bool
    github_activity_score: float
    search_appearance_30d: int
    saved_by_recruiters_30d: int
    interview_completion_rate: float
    offer_acceptance_rate: float
    verified_email: bool
    verified_phone: bool
    linkedin_connected: bool


# ==========================
# Candidate
# ==========================
@dataclass
class Candidate:
    candidate_id: str
    profile: Profile
    career_history: List[CareerEntry]
    education: List[Education]
    skills: List[Skill]
    certifications: List
    languages: List[Language]
    redrob_signals: RedrobSignals

    def get_skill_names(self):
        return [skill.name for skill in self.skills]

    def text_for_embedding(self):

        career_text = " ".join(
            [
                c.title + " " + c.company
                for c in self.career_history
            ]
        )

        skills_text = " ".join(
            [
                skill.name
                for skill in self.skills
            ]
        )

        education_text = " ".join(
            [
                e.degree + " " + e.field_of_study
                for e in self.education
            ]
        )

        return (
            self.profile.headline + " "
            + self.profile.summary + " "
            + career_text + " "
            + skills_text + " "
            + education_text
        )