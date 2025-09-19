import json

from src.chatbot.config import TOP_N_RESULTS
from src.chatbot.handlers import HANDLERS_MAPPER
from src.chatbot.mixins import JewelryConsultationMixin, GeneralInfoMixin
from src.chatbot.models import CustomerIntentEnum
from src.chatbot.utils import build_conversation_history
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch


class ChatbotService(GeneralInfoMixin, JewelryConsultationMixin):
    """Core service for generating chatbot responses."""

    def __init__(self, session_id, vector_store, memory, app, llm, customer_query):
        self.session_id = session_id
        self.vector_store = vector_store
        self.conversation_memory = memory
        self.app = app
        self.llm = llm
        self.customer_query = customer_query
        self.config = {
            'configurable': {'thread_id': session_id}
        }
        conversation_state = self.conversation_memory.get(
            self.config
        )
        self.conversation_history = build_conversation_history(
            customer_query, conversation_state
        )


    def generate_response_stream(self):
        """Generate streaming response for the customer query."""
        # Yield session_id first
        yield f"data: {json.dumps({'session_id': self.session_id})}\n\n"

        try:
            # Build and execute the main chain
            chain = self._build_main_chain()

            system_message, human_message = chain.invoke({
                "conversation_history": self.conversation_history,
                "customer_query": self.customer_query,
            })

            # Stream the response
            for event in self.app.stream(
                {"messages": [system_message, human_message]},
                self.config,
                stream_mode="updates"
            ):
                ai_response = event['model']['messages'].content
                for chunk in ai_response:
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': 'Something went wrong. Please try again.'})}\n\n"

    def _build_main_chain(self):
        """Build the main processing chain."""
        return (
            RunnablePassthrough.assign(
                optimized_query_for_intent=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['create_optimized_query_for_intent'](
                        self.llm,
                        conversation_history=inputs["conversation_history"],
                    )
                )
            )
            | RunnablePassthrough.assign(
                customer_intent=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['extract_customer_intent'](
                        self.llm,
                        optimized_query=inputs["optimized_query_for_intent"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                optimized_query_for_search=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['create_optimized_query_for_search'](
                        self.llm,
                        conversation_history=inputs["conversation_history"],
                    )
                )
            )
            | RunnablePassthrough.assign(
                context=lambda x: self._retrieve_relevant_content(
                    x["optimized_query_for_search"],
                )
            )
            | RunnableBranch(
                (
                    # Check if customer intent is product-related
                    lambda x: x['customer_intent'] == CustomerIntentEnum.PRODUCTS_INFO,
                    self._build_jewelry_consultation_chain()
                ),
                # Default: general information
                self._build_general_info_chain()
            )
        )

    def _retrieve_relevant_content(self, query, k=TOP_N_RESULTS):
        print('optimized_qury', query)
        results = self.vector_store.similarity_search(
            query, k=k
        )
        context = '\n'.join(
            result.page_content for result in results
        )

        return context.strip()


