import json
import re


from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from src.chatbot.handlers import PreferenceHandler
from src.chatbot.models import  CustomerIntent
from src.chatbot.prompts.conversation_stage import RECOMMENDATION_PHASE_SYSTEM_MESSAGE
from src.chatbot.prompts.prompt import ASK_DISCOVERY_QUESTION_HUMAN_MESSAGE, ASK_DISCOVERY_QUESTION_SYSTEM_MESSAGE, CLASSIFICATION_HUMAN_MESSAGE, CLASSIFICATION_SYSTEM_MESSAGE, CONVERSATION_SUMMARY_HUMAN_MESSAGE, CONVERSATION_SUMMARY_SYSTEM_MESSAGE, HUMAN_MESSAGE, INTENT_CLASSIFICATION_HUMAN_MESSAGE, INTENT_CLASSIFICATION_SYSTEM_MESSAGE, OPTIMIZED_SEARCH_QUERY_HUMAN_MESSAGE, OPTIMIZED_SEARCH_QUERY_SYSTEM_MESSAGE, DISCOVERY_PHASE_SYSTEM_MESSAGE, DISCOVERY_PHASE_HUMAN_MESSAGE
from src.chatbot.utils import build_conversation_history, classify_customer_intent, create_conversation_summary, create_enhanced_query, formulate_question_to_discover_customer_preferences, make_product_recommendation
from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter

from langchain.output_parsers import PydanticOutputParser


class ContextService:
    """Handles document retrieval and context building."""

    @staticmethod
    def get_context(vectorstore, query, k=1):
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
        llm = LLMAdapter.get_llm()

        # 1. Get session_id
        yield f"data: {json.dumps({'session_id': session_id})}\n\n"

        config = {"configurable": {"thread_id": session_id}}

        # 2. Build conversation history
        conversation_state = conversation_memory.get(config)
        if conversation_state:
            conversation_history = build_conversation_history(
                conversation_state, customer_query)
        else:
            conversation_history = [f'{1}. customer: {customer_query};']
            
        # 3. Create conversation summary
        conversation_summary = create_conversation_summary(llm, conversation_history, CONVERSATION_SUMMARY_SYSTEM_MESSAGE,  CONVERSATION_SUMMARY_HUMAN_MESSAGE)
        
        # 3. Determine whether the customer has provided all necessary preferences 
        #    to proceed to product recommendations or should remain in the discovery stage
        customer_preferences, ready_to_proceed = PreferenceHandler.extract_customer_preferences(llm, conversation_summary,  customer_query,  CLASSIFICATION_HUMAN_MESSAGE, CLASSIFICATION_SYSTEM_MESSAGE)

        if not ready_to_proceed:
            discovery_question = formulate_question_to_discover_customer_preferences(llm, conversation_summary, customer_preferences, DISCOVERY_PHASE_SYSTEM_MESSAGE, DISCOVERY_PHASE_HUMAN_MESSAGE)
            prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(ASK_DISCOVERY_QUESTION_SYSTEM_MESSAGE),
            HumanMessagePromptTemplate.from_template(ASK_DISCOVERY_QUESTION_HUMAN_MESSAGE),
        ])

            messages = prompt.format_messages(
                conversation_summary=conversation_summary,
                customer_preferences=customer_preferences,
            )

            system_message, human_message = messages[0], messages[1]
            
            ChatbotService._generate_response(app, config, discovery_question, system_message, human_message)
        else:
            enhanced_query = create_enhanced_query(
            llm, customer_preferences, OPTIMIZED_SEARCH_QUERY_SYSTEM_MESSAGE, OPTIMIZED_SEARCH_QUERY_HUMAN_MESSAGE)
            product_to_recommend = ContextService.get_context(
            vector_store, enhanced_query)
            
            prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(RECOMMENDATION_PHASE_SYSTEM_MESSAGE),
        ])

            messages = prompt.format_messages(
                product_to_recommend=product_to_recommend,
            )

            system_message = messages[0]
            
            ChatbotService._generate_response(app, config, discovery_question, system_message)
        
        # 4. Define customer intent
        customer_intent = classify_customer_intent(llm, conversation_summary, CustomerIntent, INTENT_CLASSIFICATION_SYSTEM_MESSAGE, INTENT_CLASSIFICATION_HUMAN_MESSAGE)
        
        

        # enhanced_query = create_enhanced_query(
        #     llm, conversation_history, OPTIMIZED_SEARCH_QUERY_SYSTEM_MESSAGE, OPTIMIZED_SEARCH_QUERY_HUMAN_MESSAGE)
        # context = ContextService.get_context(
        #     vector_store, enhanced_query)
            
        print(customer_preferences)
        print(ready_to_proceed)
        # customer_intent = ChatbotService._classify_customer_intent(conversation_history, customer_query)
        # conversation_stage = ChatbotService._classify_conversation_stage(
        #     conversation_history, customer_query)

        

        # prompt = ChatPromptTemplate.from_messages([
        #     SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE),
        #     HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE),
        # ])

        # messages = prompt.format_messages(
        #     conversation_memory=conversation_memory,
        #     input=customer_query,
        #     context=context,
        # )

        # system_message, human_message = messages[0], messages[1]

        # for event in app.stream({"messages": [system_message, human_message]}, config, stream_mode="updates"):

        #     for chunk in event['model']['messages'].content:
        #         yield f"data: {json.dumps({'chunk': chunk})}\n\n"

    @staticmethod
    def _generate_response(app, config, system_message, human_message):
        for event in app.stream({"messages": [system_message, human_message]}, config, stream_mode="updates"):

            for chunk in event['model']['messages'].content:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"




    
