EDUCATION_LEVEL = {
    "phd": 5,
    "doctorate": 5,
    "masters": 4,
    "master": 4,
    "mtech": 4,
    "mba": 4,
    "bachelors": 3,
    "bachelor": 3,
    "btech": 3,
    "be": 3,
    "bs": 3,
    "diploma": 2,
    "highschool": 1,
}


def compute_education_score(jd, candidate):

    if jd.education is None:
        return 1.0

    required = EDUCATION_LEVEL.get(
        jd.education.lower(),
        0,
    )

    best = 0

    for edu in candidate.education:

        degree = edu.degree.lower()

        for key, value in EDUCATION_LEVEL.items():
            if key in degree:
                best = max(best, value)

    if best >= required:
        return 1.0

    if required == 0:
        return 0.0

    return best / required