# AI Document Assistant

An AI-powered document assistant built using **Retrieval-Augmented Generation (RAG)** that allows users to ask questions about PDF documents using a locally running Large Language Model (LLM).

The application extracts text from PDFs, divides it into chunks, generates vector embeddings, and stores them in ChromaDB. When a user asks a question, the system retrieves relevant document content and uses Qwen3:8B through Ollama to generate context-aware answers.

## Features

- PDF text extraction using PyPDF
- Document text chunking with overlap
- Local embedding generation using `nomic-embed-text`
- Vector storage and semantic search using ChromaDB
- AI-powered question answering using Qwen3:8B
- Local LLM execution using Ollama
- Document-grounded responses
- Interactive command-line interface
- Persistent vector database

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Ollama | Local model execution |
| Qwen3:8B | Answer generation |
| nomic-embed-text | Text embeddings |
| ChromaDB | Vector database |
| PyPDF | PDF text extraction |
| OpenAI Python SDK | Communication with Ollama's OpenAI-compatible API |
| Requests | Ollama embedding API requests |

## System Architecture

```text
PDF Document
      |
      v
Text Extraction (PyPDF)
      |
      v
Text Chunking
      |
      v
Embedding Generation (nomic-embed-text)
      |
      v
ChromaDB Vector Database
      |
      v
User Question
      |
      v
Semantic Search
      |
      v
Relevant Document Context
      |
      v
Qwen3:8B (Ollama)
      |
      v
AI-Generated Answer
```

## Project Structure

```text
ai-document-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── embeddings.py
│   └── rag.py
├── documents/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

The `documents/` folder stores local PDF files, while ChromaDB creates a persistent database directory during execution. These files are excluded from version control.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/rajiv48/ai-document-assistant.git
cd ai-document-assistant
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install Ollama

Download Ollama from https://ollama.com.

Pull the required models:

```bash
ollama pull qwen3:8b
ollama pull nomic-embed-text
```

Verify installation:

```bash
ollama list
```

Ensure the Ollama service is running.

### 5. Add a PDF

Create a `documents` directory if it does not exist, and place a text-based PDF named `sample.pdf` inside it.

### 6. Run the application

```bash
python -m app.main
```

### 7. Ask questions

Example:

```text
Processing PDF...
Stored 12 chunks in ChromaDB.

Ask a question (or 'exit'): What is this document about?

AI Answer:
This document discusses...
```

Type `exit` to stop the application.

## How RAG Works

**1. Document processing:** PyPDF extracts text from the uploaded PDF file.

**2. Text chunking:** Extracted text is divided into smaller overlapping segments.

**3. Embedding generation:** The `nomic-embed-text` model converts each segment into a numerical vector.

**4. Vector storage:** ChromaDB stores the embeddings alongside the original text chunks.

**5. Semantic retrieval:** A user question is converted into an embedding and compared against the stored vectors to retrieve relevant document chunks.

**6. Answer generation:** The retrieved context and question are sent to Qwen3:8B, which generates an answer grounded in the document content.

## Current Limitations

- The application currently runs through the terminal.
- PDF files must be added manually.
- Scanned PDFs requiring OCR are not yet supported.
- Page-level citations are not yet implemented.
- Answers may still contain inaccuracies and should be verified against source documents.

## Future Improvements

- [ ] Implement FastAPI backend
- [ ] Add PDF upload endpoint
- [ ] Add question-answering API
- [ ] Support multiple uploaded documents
- [ ] Add page-level citations and source references
- [ ] Improve document chunking and retrieval
- [ ] Add conversational memory
- [ ] Build a frontend interface
- [ ] Add web search and calculator tools
- [ ] Convert the RAG pipeline into a tool-using AI Agent
- [ ] Deploy the application

## Project Goal

The goal of this project is to develop a practical