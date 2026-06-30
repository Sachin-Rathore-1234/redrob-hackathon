from datetime import datetime


def experience_match(required_years, candidate_years):
    """
    Compare required experience with candidate experience.
    """

    if required_years is None:
        return 1.0

    if candidate_years >= required_years:
        return 1.0

    return candidate_years / required_years


from datetime import datetime

def recency_score(career_history):
    """
    Higher score if candidate is currently working.
    """

    if not career_history:
        return 0.5

    current = career_history[0]

    if current.is_current:
        return 1.0

    if current.end_date is None:
        return 1.0

    end = datetime.strptime(current.end_date, "%Y-%m-%d")

    # Use a fixed reference date (June 30, 2026) instead of datetime.today() for deterministic scores
    ref_date = datetime(2026, 6, 30)
    months = (
        (ref_date.year - end.year) * 12
        + (ref_date.month - end.month)
    )

    return max(0, 1 - months / 36)


def progression_score(career_history):
    """
    Reward progression to larger companies.
    """

    if len(career_history) <= 1:
        return 0.5

    sizes = {
        "1-10": 1,
        "11-50": 2,
        "51-200": 3,
        "201-500": 4,
        "501-1000": 5,
        "1001-5000": 6,
        "5001-10000": 7,
        "10001+": 8,
    }

    values = [
        sizes.get(job.company_size, 4)
        for job in career_history
    ]

    if values[-1] <= values[0]:
        return 0.6

    return 1.0


def stability_score(career_history):
    """
    Penalize job hopping.
    """

    if not career_history:
        return 0.5

    durations = [
        job.duration_months
        for job in career_history
    ]

    avg = sum(durations) / len(durations)

    if avg >= 24:
        return 1.0

    if avg >= 18:
        return 0.8

    if avg >= 12:
        return 0.6

    return 0.3

def compute_experience_score(jd, candidate):
    """
    Final experience score.
    """

    exp = experience_match(
        jd.min_experience,
        candidate.profile.years_of_experience,
    )

    recent = recency_score(
        candidate.career_history
    )

    progress = progression_score(
        candidate.career_history
    )

    stability = stability_score(
        candidate.career_history
    )

    return (
        0.40 * exp
        + 0.30 * recent
        + 0.20 * progress
        + 0.10 * stability
    )