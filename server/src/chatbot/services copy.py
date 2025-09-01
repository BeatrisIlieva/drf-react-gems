import json

from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter

from src.chatbot.prompts import ENHANCED_SYSTEM_TEMPLATE, HUMAN_TEMPLATE, SYSTEM_TEMPLATE, ENHANCED_HUMAN_TEMPLATE


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
        if conversation_state:
            conversation_history = ChatbotService._build_conversation_history(
                conversation_state, user_query)
            print(conversation_history)
            enhanced_query = ChatbotService._create_enhanced_query(
                conversation_history)
            context = ContextService.get_context(
                vector_store, enhanced_query)

        else:
            context = ContextService.get_context(
                vector_store, user_query
            )

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

    @staticmethod
    def _build_conversation_history(conversation_state, user_query):
        conversation_history = []
        messages = conversation_state['channel_values']['messages']
        user_messages = [msg.content.split('INPUT:')[-1].strip()
                         for msg in messages if msg.__class__.__name__ == 'HumanMessage']
        assistant_messages = [msg.content.strip()
                              for msg in messages if msg.__class__.__name__ == 'AIMessage']

        for i in range(len(user_messages)):
            conversation_history.append(
                f'{i + 1}. user: {user_messages[i]}, assistant: {assistant_messages[i]};')

        conversation_history.append(
            f'{len(user_messages) + 1}. user: {user_query};')

        return conversation_history

    @staticmethod
    def _create_enhanced_query(conversation_history):
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                ENHANCED_SYSTEM_TEMPLATE),
            HumanMessagePromptTemplate.from_template(ENHANCED_HUMAN_TEMPLATE),
        ])

        messages = prompt.format_messages(
            conversation_history='\n'.join(conversation_history),
        )

        llm = LLMAdapter.get_llm()

        enhanced_query = llm.invoke(messages).content
        print(enhanced_query)
        return enhanced_query
    
    @staticmethod
    def _create_three_possible_responses():
        pass
