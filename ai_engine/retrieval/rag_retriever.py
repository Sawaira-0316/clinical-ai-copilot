"""
ai_engine/retrieval/rag_retriever.py
Retrieves relevant medical knowledge from Qdrant for a given query.
"""

from ai_engine.embeddings.qdrant_service import search_similar


class RAGRetriever:
    @staticmethod
    def retrieve(query: str, top_k: int = 5) -> list[dict]:
        """
        Retrieve relevant knowledge chunks from Qdrant.
        Returns list of relevant chunks with text and source.
        """
        try:
            results = search_similar(query, top_k=top_k)
            return results
        except Exception as e:
            print(f"RAG retrieval error: {e}")
            return []

    @staticmethod
    def format_for_prompt(chunks: list[dict]) -> str:
        """Format retrieved chunks for inclusion in a prompt."""
        if not chunks:
            return "No relevant medical guidelines found in knowledge base."

        formatted = []
        for i, chunk in enumerate(chunks, 1):
            source = chunk.get("source", "Unknown")
            section = chunk.get("section_title", "")
            text = chunk.get("text", "")
            score = chunk.get("score", 0)

            header = f"[Source {i}: {source}"
            if section:
                header += f" — {section}"
            header += f" (relevance: {score:.2f})]"

            formatted.append(f"{header}\n{text}")

        return "\n\n".join(formatted)