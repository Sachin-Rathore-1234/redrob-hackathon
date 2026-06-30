import csv


def _candidate_skill_lookup(candidate):
    return {
        skill.name.strip().lower(): skill.name.strip()
        for skill in candidate.skills
    }


def _matched_skills(jd, candidate, limit=3):
    skills = _candidate_skill_lookup(candidate)
    matches = [
        skills[skill.strip().lower()]
        for skill in jd.skills
        if skill.strip().lower() in skills
    ]

    return matches[:limit]


def _fallback_skills(candidate, limit=3):
    ranked = sorted(
        candidate.skills,
        key=lambda skill: (
            skill.proficiency.lower() not in {"expert", "advanced"},
            -skill.endorsements,
            -skill.duration_months,
            skill.name.lower(),
        ),
    )

    return [
        skill.name.strip()
        for skill in ranked[:limit]
    ]


def build_reasoning(jd, candidate, result):
    profile = candidate.profile
    redrob = candidate.redrob_signals

    skills = _matched_skills(jd, candidate)
    if not skills:
        skills = _fallback_skills(candidate)

    parts = [
        (
            f"{profile.current_title} with "
            f"{profile.years_of_experience:.1f} yrs"
        )
    ]

    if skills:
        parts.append(
            "strongest listed skills: " + ", ".join(skills)
        )

    parts.append(
        f"response rate {redrob.recruiter_response_rate:.2f}"
    )

    if redrob.open_to_work_flag:
        parts.append("open to work")

    if redrob.notice_period_days <= 30:
        parts.append(
            f"{redrob.notice_period_days}d notice"
        )
    elif redrob.notice_period_days >= 90:
        parts.append(
            f"long notice period ({redrob.notice_period_days}d)"
        )

    if result["risk_score"] >= 0.45:
        parts.append("down-weighted for profile risk signals")

    return "; ".join(parts) + "."


def write_submission(results, output_path, top_k):
    rows = []

    for rank, item in enumerate(results[:top_k], start=1):
        rows.append(
            {
                "candidate_id": item["candidate_id"],
                "rank": rank,
                "score": f"{item['final_score']:.4f}",
                "reasoning": item["reasoning"],
            }
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "candidate_id",
                "rank",
                "score",
                "reasoning",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    return rows


def validate_submission_rows(rows, top_k):
    if len(rows) != top_k:
        raise ValueError(
            f"Expected {top_k} rows, got {len(rows)}"
        )

    ranks = [
        row["rank"]
        for row in rows
    ]
    if ranks != list(range(1, top_k + 1)):
        raise ValueError("Ranks must be exactly 1 through top_k")

    candidate_ids = [
        row["candidate_id"]
        for row in rows
    ]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("Duplicate candidate_id in submission")

    scores = [
        float(row["score"])
        for row in rows
    ]
    if any(
        scores[i] < scores[i + 1]
        for i in range(len(scores) - 1)
    ):
        raise ValueError("Scores must be non-increasing by rank")
