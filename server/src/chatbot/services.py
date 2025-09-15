import json

from src.chatbot.handlers import build_conversation_history
from src.chatbot.mixins import (
    AnalyzeConversationInsightsMixin,
    CustomerSupportMixin,
    ExtractCustomerIntentMixin,
    ObjectionHandlingMixin,
    OffTopicMixin,
    OfferSizeHelp,
    ProductRecommendationMixin,
    ProvideSizeHelp
)
from src.chatbot.models import CustomerIntentEnum


class ChatbotService(
    ProductRecommendationMixin,
    CustomerSupportMixin,
    ObjectionHandlingMixin,
    OffTopicMixin,
    OfferSizeHelp,
    ProvideSizeHelp,
    AnalyzeConversationInsightsMixin,
    ExtractCustomerIntentMixin
):
    """Core service for generating chatbot responses."""

    def __init__(
        self,
        session_id,
        vector_store,
        memory,
        app,
        llm,
        customer_query
    ):
        self.session_id = session_id
        self.vector_store = vector_store
        self.conversation_memory = memory
        self.app = app
        self.llm = llm
        self.customer_query = customer_query
        self.config = {
            'configurable': {'thread_id': session_id}
        }

        self.customer_preferences = None
        self.conversation_insights = None

    def generate_response_stream(self):
        # 1. Get session_id
        yield f'data: {json.dumps({'session_id': self.session_id})}\n\n'

        # 2. Build conversation history
        conversation_state = self.conversation_memory.get(
            self.config
        )
        conversation_history = build_conversation_history(
            self.customer_query,
            conversation_state
        )

        # 3. Extract conversation insights
        self.conversation_insights = self.analyze_conversation_insights(
            self.llm,
            conversation_history,
        )
        
        print('conversation_insights')
        print(self.conversation_insights)
        print('-----')

        # 4. Define customer intent
        customer_intent = self.extract_customer_intent(
            self.llm,
            self.conversation_insights,
        )
        
        print('customer_intent')
        print(customer_intent)
        print('-----')

        # 5. Handle customer query
        handler = self._intent_handler_map.get(
            customer_intent['primary_intent'],
        )
        system_message, human_message = handler()

        # 6. Generate response stream
        for event in self.app.stream(
            {'messages': [system_message, human_message]},
                self.config, stream_mode='updates'
        ):

            for chunk in event['model']['messages'].content:
                yield f'data: {json.dumps({'chunk': chunk})}\n\n'

    @property
    def _intent_handler_map(self):
        return {
            CustomerIntentEnum.WANTS_PRODUCT_INFORMATION_OR_SHARES_PREFERENCES:
                lambda: self.handle_product_recommendation(
                    self.llm,
                    self.vector_store,
                    self.conversation_memory,
                    self.conversation_insights,
                ),
            CustomerIntentEnum.IS_INTERESTED_IN_A_SPECIFIC_PRODUCT_THAT_HAS_BEEN_RECOMMENDED_DURING_THE_CURRENT_CONVERSATION:
                lambda: self.handle_offer_size_help(
                    self.llm,
                    self.conversation_memory,
                    self.conversation_insights,
                ),
            CustomerIntentEnum.IS_INTERESTED_IN_RECEIVING_HELP_IN_SELECTING_IDEAL_SIZE_FOR_SELF_PURCHASE:
                lambda: self.handle_provide_size_help(
                    self.llm,
                    self.conversation_memory,
                ),
            CustomerIntentEnum.SIZING_HELP:
                lambda: self.handle_customer_support(
                    self.llm,
                    self.conversation_memory,
                    self.conversation_insights,
                ),
            CustomerIntentEnum.CARE_INSTRUCTIONS:
                lambda: self.handle_customer_support(
                    self.llm,
                    self.conversation_memory,
                    self.conversation_insights,
                ),
            CustomerIntentEnum.RETURN_POLICY:
                lambda: self.handle_customer_support(
                    self.llm,
                    self.conversation_memory,
                    self.conversation_insights,
                ),
            CustomerIntentEnum.SHIPPING_INFORMATION:
                lambda: self.handle_customer_support(
                    self.llm,
                    self.conversation_memory,
                    self.conversation_insights,
                ),
            CustomerIntentEnum.BRAND_INFORMATION:
                lambda: self.handle_customer_support(
                    self.llm,
                    self.conversation_memory,
                    self.conversation_insights,
                ),
            CustomerIntentEnum.ISSUE_OR_CONCERN_OR_HESITATION:
                lambda: self.handle_objections(
                    self.llm,
                    self.conversation_memory,
                    self.conversation_insights,
                ),
            CustomerIntentEnum.OFF_TOPIC:
                lambda: self.handle_off_topic(
                    self.llm,
                    self.conversation_memory,
                ),
        }
