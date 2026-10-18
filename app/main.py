
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from .rag import process_pdf, collection
from .llm import ask_question


# Initialize FastAPI
app = FastAPI(
    title="AI Document Assistant",
    description="RAG-powered PDF question answering using Ollama",
    version="0.3.0"
)

# Upload configuration
UPLOAD_DIR = Path("documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_UPLOAD_SIZE = 20 * 1024 * 1024  # 20 MB


# Request model
class QuestionRequest(BaseModel):
    question: str
    document_id: str


# 1. Home endpoint
@app.get("/")
def home():
    return {
        "message": "AI Document Assistant API is running",
        "version": "0.3.0"
    }


# 2. Upload PDF endpoint
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    content = await file.read(MAX_UPLOAD_SIZE + 1)

    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail="PDF exceeds the 20 MB upload limit."
        )

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF."
        )

    # Generate unique filename
    filename = f"{uuid4().hex}.pdf"
    file_path = UPLOAD_DIR / filename

    file_path.write_bytes(content)

    try:
        result = process_pdf(file_path)

        return {
            "message": "PDF uploaded and processed successfully",
            "filename": filename,
            "document_id": result["document_id"],
            "chunks_stored": result["chunks_stored"]
        }

    except Exception as e:
        import traceback

        print("\nPDF PROCESING ERROR")
        traceback.print_exc()

        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Unable to process PDF. Check Server Logs"
        )


# 3. Ask question endpoint
@app.post("/ask")
def ask(request: QuestionRequest):

    question = request.question.strip()
    document_id = request.document_id.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    if not document_id:
        raise HTTPException(
            status_code=400,
            detail="Document ID cannot be empty."
        )

    # Check whether the selected document exists
    document_exists = collection.get(
        where={"document_id": document_id},
        limit=1
    )

    if not document_exists["ids"]:
        raise HTTPException(
            status_code=404,
            detail="Document not found. Upload a PDF first."
        )

    try:
        result = ask_question(
            question,
            document_id=document_id
        )

        return result

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to answer question."
        )


# 4. List uploaded documents
@app.get("/documents")
def list_documents():

    results = collection.get(
        include=["metadatas"]
    )

    documents = {}

    for metadata in results["metadatas"]:
        if not metadata:
            continue

        document_id = metadata.get("document_id")

        if not document_id:
            continue

        documents[document_id] = {
            "document_id": document_id,
            "filename": metadata.get("source")
        }

    return {
        "total": len(documents),
        "documents": list(documents.values())
    }


# 5. Delete a document
@app.delete("/documents/{document_id}")
def delete_document(document_id: str):

    results = collection.get(
        where={"document_id": document_id},
        include=["metadatas"]
    )

    if not results["ids"]:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    # Collect filenames before deleting records
    filenames = {
        metadata.get("source")
        for metadata in results["metadatas"]
        if metadata and metadata.get("source")
    }

    # Delete embeddings from ChromaDB
    collection.delete(
        ids=results["ids"]
    )

    # Delete saved PDF files
    for filename in filenames:
        file_path = UPLOAD_DIR / Path(filename).name

        if file_path.exists():
            file_path.unlink()

    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }
