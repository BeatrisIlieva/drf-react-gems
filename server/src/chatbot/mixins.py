from src.chatbot.handlers import build_answer_to_provide_customer_support, build_answer_to_provide_details_about_recommended_product, build_answer_to_recommend_product, build_discovery_question, build_discovery_question_to_ask, build_objection_handling_answer, build_off_topic_answer, extract_customer_preferences, extract_filtered_products
from src.chatbot.utils import retrieve_relevant_content


class ProductRecommendationMixin:
    def handle_product_recommendation(self, llm, vector_store, conversation_memory, conversation_insights, customer_query):
        # Determine whether the customer has provided all necessary preferences
        customer_preferences, ready_to_proceed = extract_customer_preferences(
            llm,
            conversation_insights
        )

        if not ready_to_proceed:
            return self._ask_clarifying_question(llm, customer_preferences, customer_query)

        else:
            return self._recommend_product(llm, vector_store, conversation_memory, conversation_insights, customer_preferences, customer_query)

    def _ask_clarifying_question(self, llm, customer_preferences, customer_query):
        discovery_question = build_discovery_question(
            llm,
            customer_preferences,
        )

        return build_discovery_question_to_ask(
            llm,
            discovery_question,
            customer_query,
        )

    def _recommend_product(self, llm, vector_store, conversation_memory, conversation_insights, customer_preferences, customer_query):
        products = retrieve_relevant_content(
            vector_store,
            conversation_insights
        )

        filtered_product = extract_filtered_products(
            llm,
            customer_preferences,
            products,
        )

        return build_answer_to_recommend_product(
            llm,
            filtered_product,
            conversation_memory,
            customer_query,
        )


class ProductDetailsMixin:
    def handle_details_about_recommended_product(self, llm, conversation_memory, customer_query):
        return build_answer_to_provide_details_about_recommended_product(llm, conversation_memory, customer_query)


class CustomerSupportMixin:
    def handle_customer_support(self, llm, vector_store, conversation_memory, conversation_insights, customer_query):
        content = retrieve_relevant_content(
            vector_store,
            conversation_insights
        )

        return build_answer_to_provide_customer_support(llm, conversation_memory, customer_query, content)


class ObjectionHandlingMixin:
    def handle_objections(self, llm, vector_store, conversation_memory, conversation_insights, customer_query):
        content = retrieve_relevant_content(
            vector_store,
            conversation_insights
        )

        return build_objection_handling_answer(llm, conversation_memory, customer_query, content)


class OffTopicMixin:
    def handle_off_topic(self, llm, conversation_memory, customer_query):
        return build_off_topic_answer(llm, conversation_memory, customer_query)
