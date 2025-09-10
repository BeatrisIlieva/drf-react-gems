import json

from src.chatbot.handlers import analyze_conversation_insights, build_conversation_history, extract_customer_intent
from src.chatbot.mixins import CustomerSupportMixin, ObjectionHandlingMixin, ProductDetailsMixin, ProductRecommendationMixin
from src.chatbot.models import CustomerIntentEnum


class ChatbotService(ProductRecommendationMixin, ProductDetailsMixin, CustomerSupportMixin, ObjectionHandlingMixin):
    """Core service for generating chatbot responses."""

    def __init__(self, session_id, vector_store, memory, app, llm, customer_query):
        self.session_id = session_id
        self.vector_store = vector_store
        self.conversation_memory = memory
        self.app = app
        self.llm = llm
        self.customer_query = customer_query
        self.config = {"configurable": {"thread_id": session_id}}

        self.customer_preferences = None
        self.conversation_insights = None
        

    def generate_response_stream(self):
        # 1. Get session_id
        yield f"data: {json.dumps({'session_id': self.session_id})}\n\n"

        # 2. Build conversation history
        conversation_state = self.conversation_memory.get(self.config)

        conversation_history = build_conversation_history(
            self.customer_query,
            conversation_state
        )
        
        self.conversation_insights = analyze_conversation_insights(self.llm, conversation_history)

        # 5. Define customer intent
        customer_intent = extract_customer_intent(
            self.llm, self.conversation_insights
        )

        # 6. Handle customer query
        handler = self._intent_handler_map.get(customer_intent)
        system_message, human_message = handler()

        # 7. Generate response stream
        for event in self.app.stream(
            {"messages": [system_message, human_message]},
                self.config, stream_mode="updates"
        ):

            for chunk in event['model']['messages'].content:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

    @property
    def _intent_handler_map(self):
        return {
            CustomerIntentEnum.PRODUCT_INFORMATION: lambda: self.handle_product_recommendation(
                self.llm,
                self.vector_store,
                self.conversation_memory,
                self.conversation_insights,
                self.customer_query
            ),
            CustomerIntentEnum.DETAILS_ABOUT_RECOMMENDED_PRODUCT: lambda: self.handle_details_about_recommended_product(
                self.llm,
                self.conversation_memory,
                self.customer_query,
            ),
            CustomerIntentEnum.SIZING_HELP: lambda: self.handle_customer_support(self, self.llm, self.conversation_memory, self.conversation_insights, self.customer_query),
            CustomerIntentEnum.CARE_INSTRUCTIONS: lambda: self.handle_customer_support(self, self.llm, self.conversation_memory, self.conversation_insights, self.customer_query),
            CustomerIntentEnum.RETURN_POLICY: lambda: self.handle_customer_support(self, self.llm, self.conversation_memory, self.conversation_insights, self.customer_query),
            CustomerIntentEnum.SHIPPING_INFORMATION: lambda: self.handle_customer_support(self, self.llm, self.conversation_memory, self.conversation_insights, self.customer_query),
            CustomerIntentEnum.BRAND_INFORMATION: lambda: self.handle_customer_support(self, self.llm, self.conversation_memory, self.conversation_insights, self.customer_query),
            CustomerIntentEnum.ISSUE_OR_CONCERN: lambda: self.handle_objections(
                self, self.llm, self.conversation_memory, self.conversation_insights, self.customer_query
            ),
            CustomerIntentEnum.OFF_TOPIC: lambda: self.handle_off_topic(
                self.llm,
                self.conversation_memory,
                self.customer_query,
            ),
        }
