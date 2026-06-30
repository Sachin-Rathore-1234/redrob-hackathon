import numpy as np


def semantic_scores(jd_embedding: np.ndarray,
                    candidate_embeddings: np.ndarray):

    """
    Compute cosine similarity between the
    JD embedding and candidate embeddings.

    Parameters
    ----------
    jd_embedding : (384,)
    candidate_embeddings : (N,384)

    Returns
    -------
    numpy array (N,) of cosine similarities
    """

    jd_embedding = np.asarray(jd_embedding, dtype=np.float32).reshape(-1)
    candidate_embeddings = np.asarray(
        candidate_embeddings,
        dtype=np.float32,
    )

    jd_norm = np.linalg.norm(jd_embedding)
    candidate_norms = np.linalg.norm(
        candidate_embeddings,
        axis=1,
        keepdims=True,
    )

    if jd_norm == 0:
        return np.zeros(candidate_embeddings.shape[0], dtype=np.float32)

    safe_candidate_norms = np.where(
        candidate_norms == 0,
        1.0,
        candidate_norms,
    )

    return (
        candidate_embeddings / safe_candidate_norms
    ) @ (
        jd_embedding / jd_norm
    )
