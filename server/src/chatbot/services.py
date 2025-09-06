import json


from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.chatbot.models import ConversationStage, CustomerIntent
from src.chatbot.utils import build_conversation_history
from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter

from src.chatbot.prompts import CONVERSATION_STAGE_CLASSIFICATION_HUMAN_MESSAGE, CONVERSATION_STAGE_CLASSIFICATION_SYSTEM_MESSAGE, INTENT_CLASSIFICATION_HUMAN_MESSAGE, INTENT_CLASSIFICATION_SYSTEM_MESSAGE, OPTIMIZED_SEARCH_QUERY_HUMAN_MESSAGE, OPTIMIZED_SEARCH_QUERY_SYSTEM_MESSAGE, HUMAN_MESSAGE, SYSTEM_MESSAGE
from langchain.output_parsers import PydanticOutputParser


class ContextService:
    """Handles document retrieval and context building."""

    @staticmethod
    def get_context(vectorstore, query, k=3):
        results = vectorstore.similarity_search(query, k=k)
        context = '\n'.join(result.page_content for result in results)

        # return results
        return context.strip()


class ChatbotService:
    """Core service for generating chatbot responses."""

    @staticmethod
    def generate_response_stream(customer_query, session_id):
        vector_store = VectorStoreAdapter.get_vectorstore()
        conversation_memory = MemoryAdapter.get_memory()
        app = MemoryAdapter.get_app()

        # Yield session_id first
        yield f"data: {json.dumps({'session_id': session_id})}\n\n"

        config = {"configurable": {"thread_id": session_id}}
        conversation_history = []
        conversation_state = conversation_memory.get(config)
        if conversation_state:
            conversation_history = build_conversation_history(
                conversation_state, customer_query)

            enhanced_query = ChatbotService._create_enhanced_query(
                conversation_history)
            context = ContextService.get_context(
                vector_store, enhanced_query)

        else:
            context = ContextService.get_context(
                vector_store, customer_query
            )
            
        # customer_intent = ChatbotService._classify_customer_intent(conversation_history, customer_query)
        conversation_stage = ChatbotService._classify_conversation_stage(conversation_history, customer_query)
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE),
        ])
        
        # print('context:')
        # print(context)
        # print('-----')

        messages = prompt.format_messages(
            conversation_memory=conversation_memory,
            input=customer_query,
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
                OPTIMIZED_SEARCH_QUERY_SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(
                OPTIMIZED_SEARCH_QUERY_HUMAN_MESSAGE),
        ])

        messages = prompt.format_messages(
            conversation_history='\n'.join(conversation_history),
        )

        llm = LLMAdapter.get_llm()

        enhanced_query = llm.invoke(messages).content
        # print('enhanced_query', enhanced_query)
        return enhanced_query
    
    @staticmethod
    def _classify_customer_intent(conversation_history, customer_query):
        print(conversation_history)
        intent_parser = PydanticOutputParser(pydantic_object=CustomerIntent)
        format_instructions=intent_parser.get_format_instructions()
        # print('instructions', format_instructions + '\n\n')
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                INTENT_CLASSIFICATION_SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(
                INTENT_CLASSIFICATION_HUMAN_MESSAGE),
        ])

        messages = prompt.format_messages(
            conversation_history='\n'.join(conversation_history),
            customer_query=customer_query,
            format_instructions=format_instructions
        )

        llm = LLMAdapter.get_llm()

        customer_intent = llm.invoke(messages).content
        print('customer_intent', customer_intent)
        return customer_intent

    @staticmethod
    def _classify_conversation_stage(conversation_history, customer_query):
        print(conversation_history)
        intent_parser = PydanticOutputParser(pydantic_object=ConversationStage)
        format_instructions=intent_parser.get_format_instructions()
        # print('instructions', format_instructions + '\n\n')
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                CONVERSATION_STAGE_CLASSIFICATION_SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(
                CONVERSATION_STAGE_CLASSIFICATION_HUMAN_MESSAGE),
        ])

        messages = prompt.format_messages(
            conversation_history='\n'.join(conversation_history),
            customer_query=customer_query,
            format_instructions=format_instructions
        )

        llm = LLMAdapter.get_llm()

        conversation_stage = llm.invoke(messages).content
        print('conversation_stage', conversation_stage)
        return conversation_stage
    
    