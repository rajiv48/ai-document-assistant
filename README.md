AI Document Assistant
A local AI-powered document question-answering application built with Retrieval-Augmented Generation (RAG). It extracts text from PDF documents, creates semantic embeddings, stores them in a vector database, retrieves relevant passages, and uses a locally running language model to answer questions based on document content.
Current Status
Version 0.1 — Local RAG prototype
The project currently runs as a command-line application. PDF processing, vector storage, semantic retrieval, and local LLM-based question answering have been tested with a sample document. A web API and frontend are planned but are not implemented yet.
Features
- Extract text from text-based PDF documents with PyPDF
- Split extracted text into overlapping chunks
- Generate local embeddings with Ollama and nomic-embed-text
- Store and retrieve embeddings with persistent ChromaDB storage
- Retrieve relevant document passages using semantic similarity
- Generate document-grounded answers using Ollama and qwen3:8b
- Ask multiple questions through a command-line interface
- Handle empty questions and report errors
Tech Stack
Component	Technology
Language	Python
Local LLM	Ollama — Qwen3:8B
Embedding model	Ollama — nomic-embed-text
Vector database	ChromaDB
PDF extraction	PyPDF
HTTP client	Requests
LLM API client	OpenAI Python SDK (pointed at Ollama's local OpenAI-compatible endpoint)
Planned backend	FastAPI


Architecture
PDF file
   |
   v
Text extraction (PyPDF)
   |
   v
Overlapping text chunks
   |
   v
Embeddings (Ollama / nomic-embed-text)
   |
   v
ChromaDB (persistent vector store)
   |
   +------------------------------+
                                  |
User question                     |
   |                              |
   v                              |
Question embedding                |
   |                              |
   +------> Similarity search <---+
                  |
                  v
         Relevant document chunks
                  |
                  v
          Qwen3:8B via Ollama
                  |
                  v
             AI answer





             ai-document-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py          # CLI entry point and LLM answer generation
│   ├── embeddings.py    # Ollama embedding requests
│   └── rag.py           # PDF processing and ChromaDB retrieval
├── documents/           # Local PDFs (excluded from Git)
├── chroma_db/           # Generated vector database (excluded from Git)
├── requirements.txt
├── .gitignore
└── README.md



Getting Started
Prerequisites
- Python and pip
- Ollama installed and running locally
- Enough memory and storage to run the Qwen3:8B model
1. Clone the repository
git clone <YOUR_REPOSITORY_URL>
cd ai-document-assistant
2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
On Windows, activate it with venv\Scripts\activate instead.
3. Install dependencies
python -m pip install -r requirements.txt
Ensure requirements.txt includes the packages used by the application: openai, python-dotenv, requests, pypdf, and chromadb.
4. Download the local models
ollama pull qwen3:8b
ollama pull nomic-embed-text
ollama list
Make sure Ollama is running. If it is not running as a background application, start the server with ollama serve in another terminal.
5. Add a PDF
Place a text-based PDF at:
documents/sample.pdf
The current CLI prototype expects this path. Scanned PDFs without extractable text are not yet supported.
6. Run the application
From the project root:
python -m app.main
Example interaction:
Processing PDF...
Stored 12 chunks in ChromaDB.

Ask a question (or 'exit'): What is this document about?
AI Answer: ...

Ask a question (or 'exit'): exit
Goodbye!
The number of chunks and answer will vary by document.
Limitations
- Command-line interface only; FastAPI upload and question endpoints are planned.
- The current CLI processes documents/sample.pdf on startup.
- PDF extraction works for selectable text; scanned documents require OCR.
- Responses are grounded using retrieved chunks, but may still be inaccurate; verify important answers against the source document.
- Page-level citations and document management are not yet implemented.
- Reprocessing a modified PDF may leave older chunks in the database; document re-indexing needs improvement.
Roadmap
- [x] Extract PDF text
- [x] Split text into chunks
- [x] Generate local embeddings
- [x] Store vectors in ChromaDB
- [x] Retrieve relevant chunks
- [x] Generate answers with Qwen3:8B
- [x] Command-line question answering
- [ ] Add page-level source citations
- [ ] Improve chunking and document re-indexing
- [ ] Add FastAPI endpoints for PDF upload and questions
- [ ] Support multiple documents and document management
- [ ] Add conversation history
- [ ] Build a frontend interface
- [ ] Add agent tools such as web search and a calculator
- [ ] Add tests and deployment configuration
Privacy and Security
The default RAG workflow uses locally running Ollama models. Do not commit private PDFs, .env files, API keys, or the local ChromaDB database. Review document sensitivity before uploading or sharing any sample files.
License
No license has been selected yet.