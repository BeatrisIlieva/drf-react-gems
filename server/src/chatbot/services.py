import json


from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.chatbot.utils import build_conversation_history, filter_chunk_with_most_keywords
from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter

from src.chatbot.prompts import OPTIMIZE_SEARCH_QUERY_HUMAN_MESSAGE, OPTIMIZE_SEARCH_QUERY_SYSTEM_MESSAGE, HUMAN_MESSAGE, SYSTEM_MESSAGE


class ContextService:
    """Handles document retrieval and context building."""

    @staticmethod
    def get_context(vectorstore, query, k=4):
        results = vectorstore.similarity_search(query, k=k)
        context = '\n'.join(result.page_content for result in results)

        # return results
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
        if conversation_state:
            conversation_history = build_conversation_history(
                conversation_state, user_query)

            enhanced_query = ChatbotService._create_enhanced_query(
                conversation_history)
            context = ContextService.get_context(
                vector_store, enhanced_query)

        else:
            context = ContextService.get_context(
                vector_store, user_query
            )

        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE),
        ])
        
        print('context:')
        print(context)
        print('-----')

        messages = prompt.format_messages(
            conversation_memory=conversation_memory,
            input=user_query,
            context=context,
        )

        system_message, human_message = messages[0], messages[1]

        for event in app.stream({"messages": [system_message, human_message]}, config, stream_mode="updates"):
            ai_response = event['model']['messages'].content

            for chunk in ai_response:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

    @staticmethod
    def _create_enhanced_query(conversation_history):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                OPTIMIZE_SEARCH_QUERY_SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(
                OPTIMIZE_SEARCH_QUERY_HUMAN_MESSAGE),
        ])

        messages = prompt.format_messages(
            conversation_history='\n'.join(conversation_history),
        )

        llm = LLMAdapter.get_llm()

        enhanced_query = llm.invoke(messages).content
        print('enhanced_query', enhanced_query)
        return enhanced_query
