from collections import Counter


ADVANCED = {"advanced", "expert"}


def advanced_skill_ratio(candidate):

    if not candidate.skills:
        return 0

    advanced = sum(
        skill.proficiency.lower() in ADVANCED
        for skill in candidate.skills
    )

    return advanced / len(candidate.skills)


def assessment_gap(candidate):

    assessments = candidate.redrob_signals.skill_assessment_scores

    if not assessments:
        return 0

    gap = 0
    total = 0

    skill_lookup = {
        skill.name.lower(): skill.proficiency.lower()
        for skill in candidate.skills
    }

    for skill_name, score in assessments.items():

        prof = skill_lookup.get(skill_name.lower())

        if prof in ADVANCED:

            total += 1

            if score < 50:
                gap += 1

    if total == 0:
        return 0

    return gap / total


def endorsement_vs_github(candidate):

    endorsements = candidate.redrob_signals.endorsements_received
    github = candidate.redrob_signals.github_activity_score

    if endorsements > 100 and github < 2:
        return 1

    if endorsements > 50 and github < 4:
        return 0.6

    return 0


def unrelated_skill_penalty(candidate):

    words = []

    for skill in candidate.skills:
        words.extend(skill.name.lower().split())

    unique = len(set(words))

    if unique > 40:
        return 1

    if unique > 30:
        return 0.5

    return 0


def short_skill_penalty(candidate):

    if not candidate.skills:
        return 0

    short = sum(
        skill.duration_months < 6
        for skill in candidate.skills
    )

    return short / len(candidate.skills)


def compute_risk(candidate):

    risk = (
        0.30 * advanced_skill_ratio(candidate)
        + 0.30 * assessment_gap(candidate)
        + 0.20 * endorsement_vs_github(candidate)
        + 0.10 * unrelated_skill_penalty(candidate)
        + 0.10 * short_skill_penalty(candidate)
    )

    return min(risk, 1.0)