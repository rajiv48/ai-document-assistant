from openai import OpenAI

from .rag import process_pdf, search_documents

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)


def ask_question(question):
    chunks = search_documents(question)

    if not chunks:
        return "No documents found. Please add a PDF first."

    context = "\n\n".join(chunks)

    response = client.chat.completions.create(
        model="qwen3:8b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer using only the provided document context. "
                    "If the answer is not in the context, say you "
                    "cannot find it in the document. "
                    "Keep answers concise."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Context:\n{context}\n\n"
                    f"Question: {question}\n/no_think"
                )
            }
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    pdf_path = "documents/sample.pdf"

    print("Processing PDF...")
    count = process_pdf(pdf_path)

    print(f"Stored {count} chunks in ChromaDB.")

    while True:
    question = input("\nAsk a question (or 'exit'): ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        print("Please enter a question.")
        continue

    try:
        answer = ask_question(question)
        print("\nAI Answer:")
        print(answer)

    except Exception as e:
        print(f"\nError: {e}")