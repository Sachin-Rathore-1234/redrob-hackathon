from config import EMBEDDING_MODEL

_model = None


def get_embedding_model():
    """
    Loads the embedding model only once.

    Returns
    -------
    SentenceTransformer
        Cached embedding model.
    """

    global _model

    if _model is None:
        from sentence_transformers import SentenceTransformer

        print("Loading embedding model...")
        _model = SentenceTransformer(
            EMBEDDING_MODEL
        )

    return _model
