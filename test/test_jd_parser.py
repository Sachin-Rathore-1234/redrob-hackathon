from modules.jd_parser import parse_jd

jd = """
We are hiring a Senior Machine Learning Engineer.

Requirements

Minimum 3 years experience.

Python

PyTorch

Docker

AWS

Bachelor's degree

Remote work
"""

parsed = parse_jd(jd)

print(parsed)