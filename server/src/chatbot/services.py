import json

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.chatbot.adapters import MemoryAdapter, VectorstoreAdapter
from src.chatbot.config import HUMAN_TEMPLATE, SYSTEM_TEMPLATE


class ContextService:
    """Handles document retrieval and context building."""

    @staticmethod
    def get_context(vectorstore, query, k=4):
        results = vectorstore.similarity_search(query, k=k)
        for i, doc in enumerate(results, 1):
            print(f"--- Chunk {i} ---")
            print(doc.page_content, "...\n")
        context = '\n'.join(result.page_content for result in results)

        return context.strip()


class ChatbotService:
    """Core service for generating chatbot responses."""

    @staticmethod
    def generate_response_stream(user_query, session_id):
        vectorstore = VectorstoreAdapter.get_vectorstore()
        context = ContextService.get_context(vectorstore, user_query)
        memory = MemoryAdapter.get_memory()
        app = MemoryAdapter.get_app()

        # Yield session_id first
        yield f"data: {json.dumps({'session_id': session_id})}\n\n"

        config = {"configurable": {"thread_id": session_id}}

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE)
        ])

        # Format messages
        messages = prompt.format_messages(
            chat_history=memory,
            input=user_query,
            context=context
        )

        system_message, human_message = messages[0], messages[1]

        for event in app.stream({"messages": [system_message, human_message]}, config, stream_mode="updates"):
            ai_response = event['model']['messages'].content
            for chunk in ai_response:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

        # Completion signal
        yield f"data: {json.dumps({'chunk': '[DONE]'})}\n\n"
