from src.chatbot.handlers import extract_customer_preferences
from src.chatbot.models import CustomerIntent, FilteredProduct
from src.chatbot.prompts.customer_intent import ANSWER_TO_PROVIDE_CUSTOMER_SUPPORT_SYSTEM_MESSAGE, ANSWER_TO_PROVIDE_DETAILS_ABOUT_RECOMMENDED_PRODUCT_SYSTEM_MESSAGE, ANSWER_TO_RECOMMEND_PRODUCT_SYSTEM_MESSAGE, DISCOVERY_QUESTION_TO_ASK_SYSTEM_MESSAGE, OBJECTION_HANDLING_SYSTEM_MESSAGE, OFF_TOPIC_SYSTEM_MESSAGE, OFFER_HELP_WITH_SELECTING_IDEAL_SIZE_SYSTEM_MESSAGE, PLAIN_HUMAN_MESSAGE, PROVIDE_HELP_WITH_SELECTING_IDEAL_SIZE_SYSTEM_MESSAGE, WITH_MEMORY_AND_CONVERSATION_INSIGHTS_HUMAN_MESSAGE, WITH_MEMORY_AND_DB_CONTENT_HUMAN_MESSAGE, WITH_MEMORY_HUMAN_MESSAGE
from src.chatbot.prompts.helper_calls import ANALYZE_CONVERSATION_INSIGHTS_HUMAN_MESSAGE, ANALYZE_CONVERSATION_INSIGHTS_SYSTEM_MESSAGE, CUSTOMER_INTENT_HUMAN_MESSAGE, CUSTOMER_INTENT_SYSTEM_MESSAGE, DISCOVERY_QUESTION_HUMAN_MESSAGE, DISCOVERY_QUESTION_SYSTEM_MESSAGE, FILTERED_PRODUCTS_HUMAN_MESSAGE, FILTERED_PRODUCTS_SYSTEM_MESSAGE
from src.chatbot.utils import generate_formatted_response, retrieve_relevant_content


class AnalyzeConversationInsightsMixin:
    def analyze_conversation_insights(llm, conversation_history):
        return generate_formatted_response(
            llm,
            ANALYZE_CONVERSATION_INSIGHTS_SYSTEM_MESSAGE,
            ANALYZE_CONVERSATION_INSIGHTS_HUMAN_MESSAGE,
            'extract_ai_response_content',
            conversation_history=conversation_history,
        )


class ExtractCustomerIntentMixin:
    def extract_customer_intent(llm, conversation_insights):
        return generate_formatted_response(
            llm,
            CUSTOMER_INTENT_SYSTEM_MESSAGE,
            CUSTOMER_INTENT_HUMAN_MESSAGE,
            'extract_and_strip_ai_response_content',
            response_model=CustomerIntent,
            conversation_insights=conversation_insights,
        )


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
        discovery_question = generate_formatted_response(
            llm,
            DISCOVERY_QUESTION_SYSTEM_MESSAGE,
            DISCOVERY_QUESTION_HUMAN_MESSAGE,
            'extract_ai_response_content',
            customer_preferences=customer_preferences,
        )

        return generate_formatted_response(
            llm,
            DISCOVERY_QUESTION_TO_ASK_SYSTEM_MESSAGE,
            PLAIN_HUMAN_MESSAGE,
            'destructure_messages',
            discovery_question=discovery_question,
            customer_query=customer_query,
        )

    def _recommend_product(self, llm, vector_store, conversation_memory, conversation_insights, customer_preferences, customer_query):
        products = retrieve_relevant_content(
            vector_store,
            conversation_insights
        )

        filtered_product = generate_formatted_response(
            llm,
            FILTERED_PRODUCTS_SYSTEM_MESSAGE,
            FILTERED_PRODUCTS_HUMAN_MESSAGE,
            'extract_and_strip_ai_response_content',
            response_model=FilteredProduct,
            customer_preferences=customer_preferences,
            products=products,
        )

        return generate_formatted_response(
            llm,
            ANSWER_TO_RECOMMEND_PRODUCT_SYSTEM_MESSAGE,
            WITH_MEMORY_HUMAN_MESSAGE,
            'destructure_messages',
            product_to_recommend=filtered_product,
            customer_query=customer_query,
            conversation_memory=conversation_memory
        )


class ProductDetailsMixin:
    def handle_details_about_recommended_product(self, llm, conversation_memory, customer_query):
        return generate_formatted_response(
            llm,
            ANSWER_TO_PROVIDE_DETAILS_ABOUT_RECOMMENDED_PRODUCT_SYSTEM_MESSAGE,
            WITH_MEMORY_HUMAN_MESSAGE,
            'destructure_messages',
            conversation_memory=conversation_memory,
            customer_query=customer_query,
        )


class OfferSizeHelp:
    def handle_offer_size_help(llm, conversation_memory, conversation_insights, customer_query):
        return generate_formatted_response(
            llm,
            OFFER_HELP_WITH_SELECTING_IDEAL_SIZE_SYSTEM_MESSAGE,
            WITH_MEMORY_AND_CONVERSATION_INSIGHTS_HUMAN_MESSAGE,
            'destructure_messages',
            conversation_memory=conversation_memory,
            customer_query=customer_query,
            conversation_insights=conversation_insights,
        )


class ProvideSizeHelp:
    def handle_provide_size_help(llm, conversation_memory, conversation_insights, customer_query):
        return generate_formatted_response(
            llm,
            PROVIDE_HELP_WITH_SELECTING_IDEAL_SIZE_SYSTEM_MESSAGE,
            WITH_MEMORY_AND_CONVERSATION_INSIGHTS_HUMAN_MESSAGE,
            'destructure_messages',
            conversation_memory=conversation_memory,
            customer_query=customer_query,
            conversation_insights=conversation_insights,
        )


class CustomerSupportMixin:
    def handle_customer_support(self, llm, vector_store, conversation_memory, conversation_insights, customer_query):
        content = retrieve_relevant_content(
            vector_store,
            conversation_insights
        )

        return generate_formatted_response(
            llm,
            ANSWER_TO_PROVIDE_CUSTOMER_SUPPORT_SYSTEM_MESSAGE,
            WITH_MEMORY_AND_DB_CONTENT_HUMAN_MESSAGE,
            'destructure_messages',
            conversation_memory=conversation_memory,
            customer_query=customer_query,
            content=content,
        )


class ObjectionHandlingMixin:
    def handle_objections(self, llm, vector_store, conversation_memory, conversation_insights, customer_query):
        content = retrieve_relevant_content(
            vector_store,
            conversation_insights
        )

        return generate_formatted_response(
            llm,
            OBJECTION_HANDLING_SYSTEM_MESSAGE,
            WITH_MEMORY_AND_DB_CONTENT_HUMAN_MESSAGE,
            'destructure_messages',
            conversation_memory=conversation_memory,
            customer_query=customer_query,
            content=content,
        )


class OffTopicMixin:
    def handle_off_topic(self, llm, conversation_memory, customer_query):
        return generate_formatted_response(
            llm,
            OFF_TOPIC_SYSTEM_MESSAGE,
            WITH_MEMORY_HUMAN_MESSAGE,
            'destructure_messages',
            conversation_memory=conversation_memory,
            customer_query=customer_query,
        )
