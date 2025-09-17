import json
from abc import ABC
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch

from src.chatbot.adapters import LLMAdapter, MemoryAdapter, VectorStoreAdapter
from src.chatbot.handlers import HANDLERS_MAPPER, build_conversation_history
from src.chatbot.models import BudgetRange, CategoryType, CustomerIntentEnum, MetalType, PurchaseType, StoneType, WearerGender
from src.chatbot.strategies import PreferenceDiscoveryStrategy
from src.chatbot.utils import all_preferences_collected, retrieve_relevant_content


class PreferenceExtractionMixin:
    """Mixin for extracting customer preferences."""
    
    def _build_preference_extraction_chain(self):
        """Build chain for extracting customer preferences."""
        return (
            RunnablePassthrough.assign(
                purchase_type=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        self.llm,
                        PurchaseType,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                gender=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        self.llm,
                        WearerGender,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                category=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        self.llm,
                        CategoryType,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                metal_type=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        self.llm,
                        MetalType,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                stone_type=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        self.llm,
                        StoneType,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
            | RunnablePassthrough.assign(
                budget_range=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_preferences'](
                        self.llm,
                        BudgetRange,
                        conversation_history=inputs["conversation_history"]
                    )
                )
            )
        )


class ProductDiscoveryMixin:
    """Mixin for product discovery functionality."""
    
    def _build_continue_discovery_chain(self):
        """Build chain for continuing preference discovery."""
        return (
            RunnablePassthrough.assign(
                next_discovery_question=RunnableLambda(
                    lambda inputs: PreferenceDiscoveryStrategy.get_next_question(
                        inputs['purchase_type'] | inputs['gender'] | inputs['category'] |
                        inputs['metal_type'] | inputs['stone_type'] | inputs['budget_range']
                    )
                )
            )
            | RunnableLambda(
                lambda inputs: HANDLERS_MAPPER['investigate'](
                    self.llm,
                    context=inputs["context"],
                    customer_query=inputs["customer_query"],
                    next_discovery_question=inputs['next_discovery_question'],
                    **self._extract_safe_preferences(inputs),
                    conversation_memory=inputs["conversation_memory"]
                )
            )
        )

    def _build_recommend_product_chain(self):
        """Build chain for product recommendations."""
        return RunnableLambda(
            lambda inputs: HANDLERS_MAPPER['recommend_product'](
                self.llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
                **self._extract_preferences(inputs),
                conversation_memory=inputs["conversation_memory"]
            )
        )

    def _build_available_options_navigator_chain(self):
        """Build chain for navigating available options."""
        return RunnableLambda(
            lambda inputs: HANDLERS_MAPPER['available_options_navigator'](
                self.llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
                **self._extract_safe_preferences(inputs),
                conversation_memory=inputs["conversation_memory"]
            )
        )

    def _extract_preferences(self, inputs):
        """Extract preferences assuming they're all present."""
        return {
            'purchase_type': inputs["purchase_type"]["purchase_type"],
            'gender': inputs["gender"]["gender"],
            'category': inputs["category"]["category"],
            'metal_type': inputs["metal_type"]["metal_type"],
            'stone_type': inputs["stone_type"]["stone_type"],
            'budget_range': inputs["budget_range"]["budget_range"],
        }

    def _extract_safe_preferences(self, inputs):
        """Extract preferences with safe dictionary access."""
        return {
            'purchase_type': inputs.get("purchase_type", {}).get("purchase_type", ""),
            'gender': inputs.get("gender", {}).get("gender", ""),
            'category': inputs.get("category", {}).get("category", ""),
            'metal_type': inputs.get("metal_type", {}).get("metal_type", ""),
            'stone_type': inputs.get("stone_type", {}).get("stone_type", ""),
            'budget_range': inputs.get("budget_range", {}).get("budget_range", ""),
        }


class GeneralInfoMixin:
    """Mixin for general information handling."""
    
    def _build_general_info_chain(self):
        """Build chain for general information responses."""
        return RunnableLambda(
            lambda inputs: HANDLERS_MAPPER['general-info'](
                self.llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
                conversation_memory=inputs["conversation_memory"]
            )
        )


class ConditionalChainMixin:
    """Mixin for building conditional chains."""
    
    def _build_discovery_or_recommend_chain(self):
        """Build conditional chain for discovery vs recommendation."""
        return RunnableBranch(
            (
                # If all preferences are collected, recommend products
                lambda x: all_preferences_collected(x),
                self._build_recommend_product_chain()
            ),
            # Otherwise, continue discovery
            self._build_continue_discovery_chain()
        )

    def _build_jewelry_consultation_chain(self):
        """Build the complete jewelry consultation process chain."""
        return (
            self._build_preference_extraction_chain()
            | RunnablePassthrough.assign(
                product_that_meets_current_preferences=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['product_that_meets_current_preferences'](
                        self.llm,
                        context=inputs["context"],
                        customer_query=inputs["customer_query"],
                        **self._extract_safe_preferences(inputs),
                        conversation_memory=inputs["conversation_memory"]
                    )
                )
            )
            | RunnableBranch(
                (
                    lambda x: x['product_that_meets_current_preferences'] == 'MATCH',
                    self._build_discovery_or_recommend_chain()
                ),
                self._build_available_options_navigator_chain()
            )
        )


class ChatbotService(
    PreferenceExtractionMixin,
    ProductDiscoveryMixin,
    GeneralInfoMixin,
    ConditionalChainMixin
):
    """Core service for generating chatbot responses."""

    def __init__(self, session_id: str, customer_query: str):
        """Initialize the chatbot service with session-specific data."""
        self.session_id = session_id
        self.customer_query = customer_query
        
        # Initialize adapters
        self.vector_store = VectorStoreAdapter.get_vectorstore()
        self.conversation_memory = MemoryAdapter.get_memory()
        self.llm = LLMAdapter.get_llm()
        self.app = MemoryAdapter.get_app()
        
        # Session configuration
        self.config = {"configurable": {"thread_id": session_id}}
        
        # Build conversation context
        conversation_state = self.conversation_memory.get(self.config)
        self.conversation_history = build_conversation_history(
            customer_query, conversation_state
        )

    def _build_main_chain(self):
        """Build the main processing chain."""
        return (
            RunnablePassthrough.assign(
                optimized_query=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['optimized_query'](
                        self.llm,
                        conversation_history=inputs["conversation_history"],
                    )
                )
            )
            | RunnablePassthrough.assign(
                context=lambda x: retrieve_relevant_content(
                    self.vector_store,
                    x["optimized_query"],
                )
            )
            | RunnablePassthrough.assign(
                customer_intent=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['customer_intent'](
                        self.llm,
                        conversation_history=inputs["conversation_history"]
                    )
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

    def generate_response_stream(self):
        """Generate streaming response for the customer query."""
        # Yield session_id first
        yield f"data: {json.dumps({'session_id': self.session_id})}\n\n"

        try:
            # Build and execute the main chain
            chain = self._build_main_chain()
            
            system_message, human_message = chain.invoke({
                "conversation_history": self.conversation_history,
                "conversation_memory": self.conversation_memory,
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
            # Log the error and return a fallback response
            yield f"data: {json.dumps({'error': 'Something went wrong. Please try again.'})}\n\n"

    @staticmethod
    def create_and_stream(customer_query: str, session_id: str):
        """Factory method to create service instance and generate stream."""
        service = ChatbotService(session_id, customer_query)
        return service.generate_response_stream()


# Usage remains simple:
# for chunk in ChatbotService.create_and_stream(customer_query, session_id):
#     # Process chunk