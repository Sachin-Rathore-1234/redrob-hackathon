def compute_availability_score(redrob):
    
    score = 0.0

    # Open to work (40%)
    if redrob.open_to_work_flag:
        score += 0.40

    # Notice period (30%)
    if redrob.notice_period_days <= 30:
        score += 0.30
    elif redrob.notice_period_days <= 60:
        score += 0.20
    elif redrob.notice_period_days <= 90:
        score += 0.10

    # Willing to relocate (20%)
    if redrob.willing_to_relocate:
        score += 0.20

    # Verified profile (10%)
    if (
        redrob.verified_email
        and redrob.verified_phone
    ):
        score += 0.10

    return min(score, 1.0)