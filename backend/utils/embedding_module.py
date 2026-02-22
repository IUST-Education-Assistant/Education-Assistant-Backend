import os
from pathlib import Path

from sentence_transformers import SentenceTransformer

_BASE_DIR = Path(__file__).resolve().parent.parent
_default_local_model = _BASE_DIR / "embedding_model"
_model_id = (
    os.getenv("EMBEDDING_MODEL_PATH")
    or os.getenv("EMBEDDING_MODEL_NAME")
    or (str(_default_local_model) if _default_local_model.exists() else "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
)
_model = SentenceTransformer(_model_id)

def embed_chunk(chunk):
    return _model.encode(chunk).tolist()