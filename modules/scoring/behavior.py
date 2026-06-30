def compute_behavior_score(redrob):
    
    score = 0.0

    # Profile completeness (20%) - kept / 100 since it is 0-100 percentage
    score += 0.20 * (
        redrob.profile_completeness_score / 100
    )

    # Recruiter response rate (25%) - already a fraction [0.0, 1.0]
    score += 0.25 * redrob.recruiter_response_rate

    # Interview completion rate (20%) - already a fraction [0.0, 1.0]
    score += 0.20 * redrob.interview_completion_rate

    # Offer acceptance rate (10%) - fraction [0.0, 1.0], or -1 if no history
    if redrob.offer_acceptance_rate == -1:
        offer_score = 0.5  # Neutral default
    else:
        offer_score = redrob.offer_acceptance_rate
    score += 0.10 * offer_score

    # Saved by recruiters (15%)
    score += 0.15 * min(
        redrob.saved_by_recruiters_30d / 20,
        1.0,
    )

    # Search appearance (10%)
    score += 0.10 * min(
        redrob.search_appearance_30d / 50,
        1.0,
    )

    return min(score, 1.0)