import chromadb
from pypdf import PdfReader

from .embeddings import get_embedding

# Create a persistent vector database
chroma_client = chromadb.PersistentClient(path="./chroma_db")

collection = chroma_client.get_or_create_collection(
    name="documents"
)


def process_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += (page.extract_text() or "") + "\n"

    if not text.strip():
        raise ValueError("No extractable text found in PDF")

    # Split text into smaller chunks
    chunk_size = 1000
    overlap = 200
    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    # Store chunks in ChromaDB
    import hashlib

    document_id = hashlib.sha256(
        str(file_path).encode()
    ).hexdigest()[:16]

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)

        collection.upsert(
            ids=[f"{document_id}_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{
                "source": str(file_path),
                "chunk": i
            }]
        )

    return len(chunks)


def search_documents(question):
    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(3, collection.count())
    ) if collection.count() > 0 else None

    if results is None:
        return []

    return results["documents"][0]