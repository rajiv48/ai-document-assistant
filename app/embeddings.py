import requests

OLLAMA_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "nomic-embed-text"


def get_embedding(text):

    if not text or not text.strip():
        raise ValueError("Cannot generate embedding for empty text.")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": text
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    embeddings = data.get("embeddings")

    if not embeddings:
        raise ValueError(
            f"Ollama returned no embeddings: {data}"
        )

    return embeddings[0]