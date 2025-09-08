import json

from src.chatbot.handlers import build_answer_to_recommend_product, build_conversation_history, build_conversation_summary, build_discovery_question, build_discovery_question_to_ask, build_optimized_query, extract_customer_preferences, extract_filtered_products
from src.chatbot.models import CustomerIntent


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

    def __init__(self, session_id, vector_store, memory, app, llm, customer_query):
        self.session_id = session_id
        self.vector_store = vector_store
        self.conversation_memory = memory
        self.app = app
        self.llm = llm
        self.config = {"configurable": {"thread_id": session_id}}
        self.customer_query = customer_query

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

        # 5. Determine whether the customer has provided all necessary preferences
        self.customer_preferences, ready_to_proceed = extract_customer_preferences(
            self.llm,
            self.optimized_query
        )

        if not ready_to_proceed:
            self._ask_clarifying_question()

        else:
            self._recommend_product()

        # 4. Define customer intent
        # customer_intent = classify_customer_intent(
        #     llm, conversation_summary, CustomerIntent, INTENT_CLASSIFICATION_SYSTEM_MESSAGE, INTENT_CLASSIFICATION_HUMAN_MESSAGE)

    def _ask_clarifying_question(self):
        discovery_question = build_discovery_question(
            self.llm,
            self.conversation_summary,
            self.customer_preferences,
        )

        system_message, human_message = build_discovery_question_to_ask(
            self.llm,
            discovery_question,
            self.customer_query,
        )

        self._generate_response(
            system_message,
            human_message
        )

    def _recommend_product(self):
        products = ContextService.get_context(
            self.vector_store,
            self.optimized_query
        )

        filtered_product = extract_filtered_products(
            self.llm,
            self.conversation_summary,
            self.customer_preferences,
            products,
        )

        system_message, human_message = build_answer_to_recommend_product(
            self.llm,
            filtered_product,
            self.customer_query,
        )

        self._generate_response(
            system_message,
            human_message,
        )

    def _generate_response(self, system_message, human_message):
        for event in self.app.stream(
            {"messages": [system_message, human_message]},
                self.config, stream_mode="updates"
        ):

            for chunk in event['model']['messages'].content:
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
