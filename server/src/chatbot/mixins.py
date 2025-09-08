from src.chatbot.handlers import build_answer_to_recommend_product, build_discovery_question, build_discovery_question_to_ask, extract_customer_preferences, extract_filtered_products
from src.chatbot.utils import retrieve_relevant_content


class ProductRecommendationMixin:
    def handle_product_recommendation(self, llm, vector_store, optimized_query, conversation_summary, customer_query):
        # Determine whether the customer has provided all necessary preferences
        customer_preferences, ready_to_proceed = extract_customer_preferences(
            llm,
            optimized_query
        )

        if not ready_to_proceed:
            return self._ask_clarifying_question(llm, conversation_summary, customer_preferences, customer_query)

        else:
            return self._recommend_product(llm, vector_store, conversation_summary, customer_preferences, customer_query)

    def _ask_clarifying_question(self, llm, conversation_summary, customer_preferences, customer_query):
        discovery_question = build_discovery_question(
            llm,
            conversation_summary,
            customer_preferences,
        )

        system_message, human_message = build_discovery_question_to_ask(
            llm,
            discovery_question,
            customer_query,
        )

        return system_message, human_message

    def _recommend_product(self, llm, vector_store, optimized_query, conversation_summary, customer_preferences, customer_query):
        products = retrieve_relevant_content(
            vector_store,
            optimized_query
        )

        filtered_product = extract_filtered_products(
            llm,
            conversation_summary,
            customer_preferences,
            products,
        )

        system_message, human_message = build_answer_to_recommend_product(
            llm,
            filtered_product,
            customer_query,
        )

        return system_message, human_message
    
class ProductDetailsMixin:
    def handle_product_details(self):
        pass