PROFICIENCY_MAP = {
    "beginner": 0.4,
    "intermediate": 0.7,
    "advanced": 0.9,
    "expert": 1.0,
}


def skill_match_score(jd_skills, candidate_skills):

    if not jd_skills:
        return 1.0

    candidate = {
        s.name.strip().lower()
        for s in candidate_skills
    }

    matched = sum(
        skill.strip().lower() in candidate
        for skill in jd_skills
    )

    return matched / len(jd_skills)


def proficiency_score(jd_skills, candidate_skills):

    lookup = {
        s.name.strip().lower(): s
        for s in candidate_skills
    }

    scores = []

    for skill in jd_skills:

        key = skill.strip().lower()

        if key in lookup:

            prof = lookup[key].proficiency.lower()

            scores.append(
                PROFICIENCY_MAP.get(prof, 0.5)
            )

    if not scores:
        return 0

    return sum(scores) / len(scores)


def assessment_score(jd_skills, redrob):

    assessments = {
        k.lower(): v
        for k, v in redrob.skill_assessment_scores.items()
    }

    values = []

    for skill in jd_skills:

        key = skill.strip().lower()

        if key in assessments:
            values.append(
                assessments[key] / 100
            )

    if not values:
        return 0

    return sum(values) / len(values)


def github_bonus(redrob):

    return min(
        redrob.github_activity_score / 10,
        1.0,
    )


def compute_skill_score(
    jd,
    candidate,
    redrob,
):

    skill = skill_match_score(
        jd.skills,
        candidate
    )

    assessment = assessment_score(
        jd.skills,
        redrob
    )

    proficiency = proficiency_score(
        jd.skills,
        candidate
    )

    github = github_bonus(
        redrob
    )

    return (
        0.50 * skill
        + 0.25 * assessment
        + 0.15 * proficiency
        + 0.10 * github
    )