import json
import re


from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.chatbot.handlers import build_answer_to_recommend_product, build_conversation_history, build_conversation_summary, build_discovery_question, build_discovery_question_to_ask, build_optimized_query, extract_customer_preferences, extract_filtered_products
from src.chatbot.models import CustomerIntent, FilteredProduct
from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter


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
        conversation_history = build_conversation_history(
            customer_query,
            conversation_state
        )

        # 3. Build conversation summary
        conversation_summary = build_conversation_summary(
            llm,
            conversation_history
        )

        # 4. Build optimized query
        optimized_query = build_optimized_query(
            llm,
            conversation_summary
        )

        # 5. Determine whether the customer has provided all necessary preferences
        #    to proceed to product recommendations or should remain in the discovery stage
        customer_preferences, ready_to_proceed = extract_customer_preferences(
            llm,
            optimized_query
        )

        if not ready_to_proceed:
            ChatbotService._ask_clarifying_question(
                llm,
                conversation_summary,
                customer_preferences,
                customer_query,
                app,
                config
            )

        else:
            ChatbotService._recommend_product(
                vector_store,
                optimized_query,
                llm,
                conversation_summary,
                customer_preferences,
                customer_query,
                app,
                config
            )

        # 4. Define customer intent
        customer_intent = classify_customer_intent(
            llm, conversation_summary, CustomerIntent, INTENT_CLASSIFICATION_SYSTEM_MESSAGE, INTENT_CLASSIFICATION_HUMAN_MESSAGE)

    @staticmethod
    def _generate_response(app, config, system_message, human_message):
        for event in app.stream({"messages": [system_message, human_message]}, config, stream_mode="updates"):

            for chunk in event['model']['messages'].content:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

    @staticmethod
    def _ask_clarifying_question(llm, conversation_summary, customer_preferences, customer_query, app, config):
        discovery_question = build_discovery_question(
            llm, conversation_summary, customer_preferences)

        system_message, human_message = build_discovery_question_to_ask(
            llm, discovery_question, customer_query)

        ChatbotService._generate_response(
            app,
            config,
            system_message,
            human_message
        )

    @staticmethod
    def _recommend_product(vector_store, optimized_query, llm, conversation_summary, customer_preferences, customer_query, app, config):
        products = ContextService.get_context(
            vector_store,
            optimized_query
        )

        filtered_product = extract_filtered_products(
            llm, conversation_summary, customer_preferences, products)

        system_message, human_message = build_answer_to_recommend_product(
            llm, filtered_product, customer_query)

        ChatbotService._generate_response(
            app, config, system_message, human_message
        )
