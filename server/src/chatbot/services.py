import json

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.chatbot.adapters import MemoryAdapter, VectorStoreAdapter

from src.chatbot.config import ENHANCED_HUMAN_TEMPLATE, ENHANCED_SYSTEM_TEMPLATE, HUMAN_TEMPLATE, SYSTEM_TEMPLATE


class ContextService:
    """Handles document retrieval and context building."""

    @staticmethod
    def get_context(vectorstore, query, k=10):
        results = vectorstore.similarity_search(query, k=k)
        # for i, doc in enumerate(results, 1):
        # print(f"--- Chunk {i} ---")
        # print(doc.page_content, "...\n")
        context = '\n'.join(result.page_content for result in results)

        return context.strip()


class ChatbotService:
    """Core service for generating chatbot responses."""

    @staticmethod
    def generate_response_stream(user_query, session_id):
        vector_store = VectorStoreAdapter.get_vectorstore()
        conversation_memory = MemoryAdapter.get_memory()
        app = MemoryAdapter.get_app()

        # Yield session_id first
        yield f"data: {json.dumps({'session_id': session_id})}\n\n"

        config = {"configurable": {"thread_id": session_id}}

        conversation_state = conversation_memory.get(config)
        human_messages = [user_query]
        if conversation_state:
            messages = conversation_state['channel_values']['messages']
            human_messages.extend([msg.content.split('INPUT:')[-1].strip()
                                  for msg in messages if msg.__class__.__name__ == 'HumanMessage'])

        enhanced_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                ENHANCED_SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template(ENHANCED_HUMAN_TEMPLATE)
        ])

        enhanced_messages = enhanced_prompt.format_messages(
            conversation_memory=' '.join(human_messages),
        )

        enhanced_system_message, enhanced_human_message = enhanced_messages[
            0], enhanced_messages[1]

        for event in app.stream({"messages": [enhanced_system_message, enhanced_human_message]}, config, stream_mode="updates"):
            enhanced_ai_response = event['model']['messages'].content

        context = ContextService.get_context(
            vector_store, enhanced_ai_response)

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE),
        ])

        messages = prompt.format_messages(
            conversation_memory=conversation_memory,
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
