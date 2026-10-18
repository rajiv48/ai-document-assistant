
import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  async function fetchDocuments() {
    try {
      const response = await fetch(`${API_URL}/documents`);
      if (!response.ok) throw new Error("Unable to load documents");

      const data = await response.json();
      setDocuments(data.documents || []);
    } catch (error) {
      setStatus(error.message);
    }
  }

  useEffect(() => {
    fetchDocuments();
  }, []);

  async function uploadPDF(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setStatus("Uploading and processing PDF...");

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Upload failed");
      }

      const data = await response.json();

      await fetchDocuments();
      setSelectedDocument(data.document_id);
      setMessages([]);
      setStatus("PDF uploaded successfully!");
    } catch (error) {
      setStatus(error.message);
    } finally {
      setLoading(false);
      event.target.value = "";
    }
  }

  async function askQuestion(event) {
    event.preventDefault();

    const text = question.trim();
    if (!text || !selectedDocument || loading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", text },
    ]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: text,
          document_id: selectedDocument,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Unable to answer");
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          text: data.answer,
          sources: data.sources || [],
        },
      ]);
    } catch (error) {
      setStatus(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function deleteDocument(documentId) {
    if (loading) return;

    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/documents/${encodeURIComponent(documentId)}`,
        { method: "DELETE" }
      );

      if (!response.ok) throw new Error("Delete failed");

      await fetchDocuments();

      if (selectedDocument === documentId) {
        setSelectedDocument("");
        setMessages([]);
      }

      setStatus("Document deleted successfully.");
    } catch (error) {
      setStatus(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h2>AI Document Assistant</h2>
        <p>Chat with your PDFs</p>

        <label className="upload-button">
          + Upload PDF
          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={uploadPDF}
            disabled={loading}
            hidden
          />
        </label>

        <h3>Your Documents</h3>

        {documents.length === 0 && <p>No documents yet.</p>}

        {documents.map((doc) => (
          <div
            key={doc.document_id}
            className={
              selectedDocument === doc.document_id
                ? "document selected"
                : "document"
            }
          >
            <button
              className="document-name"
              onClick={() => {
                setSelectedDocument(doc.document_id);
                setMessages([]);
              }}
            >
              {doc.filename}
            </button>

            <button
              className="delete-button"
              onClick={() => deleteDocument(doc.document_id)}
              disabled={loading}
              title="Delete document"
            >
              ×
            </button>
          </div>
        ))}
      </aside>

      <main className="chat-area">
        <header>
          <h2>Document Chat</h2>
          <p>
            {selectedDocument
              ? "Ask questions about your selected PDF"
              : "Upload or select a PDF to begin"}
          </p>
        </header>

        <section className="messages">
          {messages.length === 0 && (
            <div className="welcome">
              <h1>Ask your documents anything</h1>
              <p>
                Upload a PDF, select it, and start asking questions.
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role}`}
            >
              <p>{message.text}</p>

              {message.sources?.length > 0 && (
                <small>
                  Sources:{" "}
                  {message.sources
                    .map((source) => `Page ${source.page}`)
                    .join(", ")}
                </small>
              )}
            </div>
          ))}
        </section>

        {status && <p className="status">{status}</p>}

        <form className="chat-form" onSubmit={askQuestion}>
          <input
            type="text"
            placeholder="Ask a question about your PDF..."
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            disabled={!selectedDocument || loading}
          />

          <button
            type="submit"
            disabled={!selectedDocument || loading || !question.trim()}
          >
            {loading ? "Working..." : "Send"}
          </button>
        </form>
      </main>
    </div>
  );
}
