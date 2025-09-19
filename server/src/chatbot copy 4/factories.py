# from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter
# from src.chatbot.services import ChatbotService


# class ChatbotServiceFactory:
#     """Factory for creating ChatbotService instances with proper dependencies."""

#     @staticmethod
#     def create(session_id: str, customer_query: str) -> ChatbotService:
#         return ChatbotService(
#             session_id=session_id,
#             vector_store=VectorStoreAdapter.get_vectorstore(),
#             memory=MemoryAdapter.get_memory(),
#             app=MemoryAdapter.get_app(),
#             llm=LLMAdapter.get_llm(),
#             customer_query=customer_query,
#         )


# factories.py - Async Factory
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.chatbot.services import AsyncChatbotService

from src.chatbot.adapters import AsyncLLMAdapter, AsyncMemoryAdapter, AsyncVectorStoreAdapter


class AsyncChatbotServiceFactory:
    """Async factory for creating ChatbotService instances with proper dependencies."""

    @staticmethod
    async def create(session_id: str, customer_query: str) -> 'AsyncChatbotService':
        # Import here to avoid circular imports
        from src.chatbot.services import AsyncChatbotService
        
        # Initialize all adapters concurrently
        vector_store_task = AsyncVectorStoreAdapter.get_vectorstore()
        memory_task = AsyncMemoryAdapter.get_memory()
        app_task = AsyncMemoryAdapter.get_app()
        llm_task = AsyncLLMAdapter.get_llm()

        # Wait for all adapters to be ready
        vector_store, memory, app, llm = await asyncio.gather(
            vector_store_task,
            memory_task,
            app_task,
            llm_task
        )

        return AsyncChatbotService(
            session_id=session_id,
            vector_store=vector_store,
            memory=memory,
            app=app,
            llm=llm,
            customer_query=customer_query,
        )