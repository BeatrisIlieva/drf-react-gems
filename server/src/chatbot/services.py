import json

from src.chatbot.handlers import build_conversation_history, build_conversation_summary, build_optimized_query, extract_customer_intent
from src.chatbot.mixins import ProductRecommendationMixin
from src.chatbot.models import CustomerIntentEnum


class ChatbotService(ProductRecommendationMixin):
    """Core service for generating chatbot responses."""

    def __init__(self, session_id, vector_store, memory, app, llm, customer_query):
        self.session_id = session_id
        self.vector_store = vector_store
        self.conversation_memory = memory
        self.app = app
        self.llm = llm
        self.customer_query = customer_query
        self.config = {"configurable": {"thread_id": session_id}}

        self.conversation_history = None
        self.conversation_summary = None
        self.optimized_query = None
        self.customer_preferences = None

    def generate_response_stream(self):
        # 1. Get session_id
        yield f"data: {json.dumps({'session_id': self.session_id})}\n\n"

        # 2. Build conversation history
        conversation_state = self.conversation_memory.get(self.config)

        self.conversation_history = build_conversation_history(
            self.customer_query,
            conversation_state
        )

        # 3. Build conversation summary
        self.conversation_summary = build_conversation_summary(
            self.llm,
            self.conversation_history
        )

        # 4. Build optimized query
        self.optimized_query = build_optimized_query(
            self.llm,
            self.conversation_summary
        )

        # 5. Define customer intent
        customer_intent = extract_customer_intent(
            self.llm, self.optimized_query
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
                self.llm, self.vector_store, self.optimized_query,
                self.conversation_summary, self.customer_query
            ),
            # CustomerIntentEnum.DETAILS_ABOUT_RECOMMENDED_PRODUCT: lambda: self.handle_details_about_recommended_product(
            #     self.llm, self.vector_store, self.optimized_query,
            #     self.conversation_summary, self.customer_query
            # ),
            # CustomerIntentEnum.SIZING_HELP: lambda: self.handle_sizing_help(
            #     self.vector_store, self.optimized_query, self.customer_query
            # ),
            # CustomerIntentEnum.CARE_INSTRUCTIONS: lambda: self.handle_care_instructions(
            #     self.llm, self.vector_store, self.optimized_query, self.customer_query
            # ),
            # CustomerIntentEnum.RETURN_POLICY: lambda: self.handle_return_policy(
            #     self.vector_store, self.customer_query
            # ),
            # CustomerIntentEnum.SHIPPING_INFORMATION: lambda: self.handle_shipping_information(
            #     self.vector_store, self.customer_query, self.conversation_summary
            # ),
            # CustomerIntentEnum.BRAND_INFORMATION: lambda: self.handle_brand_information(
            #     self.vector_store, self.customer_query
            # ),
            # CustomerIntentEnum.ISSUE_OR_CONCERN_OR_HESITATION: lambda: self.handle_issue_or_concern_or_hesitation(
            #     self.customer_query, self.conversation_summary
            # ),
            # CustomerIntentEnum.OFF_TOPIC: lambda: self.handle_off_topic(
            #     self.customer_query
            # ),
        }
