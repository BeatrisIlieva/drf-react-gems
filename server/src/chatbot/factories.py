from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter
from src.chatbot.services import ChatbotService


class ChatbotServiceFactory:
    """Factory for creating ChatbotService instances with proper dependencies."""

    @staticmethod
    def create(session_id: str, customer_query: str) -> ChatbotService:
        return ChatbotService(
            session_id=session_id,
            vector_store=VectorStoreAdapter.get_vectorstore(),
            memory=MemoryAdapter.get_memory(),
            app=MemoryAdapter.get_app(),
            llm=LLMAdapter.get_llm(),
            customer_query=customer_query,
        )
