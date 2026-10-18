from openai import OpenAI

from .rag import search_documents


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def ask_question(question, document_id=None):
    matches = search_documents(
        question,
        document_id=document_id
    )

    if not matches:
        return {
            "answer": "No documents found. Upload a PDF first.",
            "sources": []
        }

    context = "\n\n".join(
        f"Source: {match['source']}, Page: {match['page']}\n"
        f"{match['text']}"
        for match in matches
    )

    response = client.chat.completions.create(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI document assistant. "
                    "Answer questions using only the provided "
                    "document context. If the answer cannot be "
                    "found in the context, say so. "
                    "Do not invent information. "
                    "Keep answers clear and concise."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Document context:\n{context}\n\n"
                    f"Question: {question}\n/no_think"
                )
            }
        ]
    )

    sources = [
        {
            "filename": match["source"],
            "page": match["page"]
        }
        for match in matches
    ]

    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }