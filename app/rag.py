import hashlib
from pathlib import Path

import chromadb
from pypdf import PdfReader

from .embeddings import get_embedding


# Persistent vector database
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="documents"
)


def process_pdf(file_path):
    file_path = Path(file_path)
    reader = PdfReader(str(file_path))

    # Unique ID based on PDF contents
    document_id = hashlib.sha256(
        file_path.read_bytes()
    ).hexdigest()[:16]

    # Remove previous chunks for this document
    existing = collection.get(
        where={"document_id": document_id}
    )

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    chunk_size = 1000
    overlap = 200
    step = chunk_size - overlap

    total_chunks = 0

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if not text.strip():
            continue

        for i in range(0, len(text), step):
            chunk = text[i:i + chunk_size]

            if not chunk.strip():
                continue

            embedding = get_embedding(chunk)

            collection.upsert(
                ids=[f"{document_id}_{page_number}_{i}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    "document_id": document_id,
                    "source": file_path.name,
                    "page": page_number
                }]
            )

            total_chunks += 1

    if total_chunks == 0:
        raise ValueError(
            "No extractable text found in this PDF."
        )

    return {
        "document_id": document_id,
        "chunks_stored": total_chunks
    }   


def search_documents(question, document_id=None, limit=3):
    if collection.count() == 0:
        return []

    question_embedding = get_embedding(question)

    query_args = {
        "query_embeddings": [question_embedding],
        "n_results": min(limit, collection.count()),
        "include": ["documents", "metadatas", "distances"]
    }

    if document_id:
        query_args["where"] = {"document_id": document_id}

    results = collection.query(**query_args)

    matches = []

    for text, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        matches.append({
            "text": text,
            "source": metadata.get("source"),
            "page": metadata.get("page")
        })

    return matches