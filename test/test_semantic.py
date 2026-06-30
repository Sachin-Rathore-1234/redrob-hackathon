import numpy as np

from modules.scoring.semantic import semantic_scores

jd = np.random.rand(384).astype(np.float32)

candidates = np.random.rand(5, 384).astype(np.float32)

scores = semantic_scores(jd, candidates)

print(scores)
print(scores.shape)