# import json

# from src.chatbot.config import TOP_N_RESULTS
# from src.chatbot.handlers import HANDLERS_MAPPER
# from src.chatbot.mixins import JewelryConsultationMixin, GeneralInfoMixin
# from src.chatbot.models import CustomerIntentEnum
# from src.chatbot.utils import build_conversation_history
# from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch


# class ChatbotService(GeneralInfoMixin, JewelryConsultationMixin):
#     """Core service for generating chatbot responses."""

#     def __init__(self, session_id, vector_store, memory, app, llm, customer_query):
#         self.session_id = session_id
#         self.vector_store = vector_store
#         self.conversation_memory = memory
#         self.app = app
#         self.llm = llm
#         self.customer_query = customer_query
#         self.config = {
#             'configurable': {'thread_id': session_id}
#         }
#         conversation_state = self.conversation_memory.get(
#             self.config
#         )
#         self.conversation_history = build_conversation_history(
#             customer_query, conversation_state
#         )


#     def generate_response_stream(self):
#         """Generate streaming response for the customer query."""
#         # Yield session_id first
#         yield f"data: {json.dumps({'session_id': self.session_id})}\n\n"

#         try:
#             # Build and execute the main chain
#             chain = self._build_main_chain()

#             system_message, human_message = chain.invoke({
#                 "conversation_history": self.conversation_history,
#                 "customer_query": self.customer_query,
#             })

#             # Stream the response
#             for event in self.app.stream(
#                 {"messages": [system_message, human_message]},
#                 self.config,
#                 stream_mode="updates"
#             ):
#                 ai_response = event['model']['messages'].content
#                 for chunk in ai_response:
#                     yield f"data: {json.dumps({'chunk': chunk})}\n\n"

#         except Exception as e:
#             yield f"data: {json.dumps({'error': 'Something went wrong. Please try again.'})}\n\n"

#     def _build_main_chain(self):
#         """Build the main processing chain."""
#         return (
#             RunnablePassthrough.assign(
#                 optimized_query_for_intent=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['create_optimized_query_for_intent'](
#                         self.llm,
#                         conversation_history=inputs["conversation_history"],
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 customer_intent=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['extract_customer_intent'](
#                         self.llm,
#                         optimized_query=inputs["optimized_query_for_intent"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 optimized_query_for_search=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['create_optimized_query_for_search'](
#                         self.llm,
#                         conversation_history=inputs["conversation_history"],
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 context=lambda x: self._retrieve_relevant_content(
#                     x["optimized_query_for_search"],
#                 )
#             )
#             | RunnableBranch(
#                 (
#                     # Check if customer intent is product-related
#                     lambda x: x['customer_intent'] == CustomerIntentEnum.PRODUCTS_INFO,
#                     self._build_jewelry_consultation_chain()
#                 ),
#                 # Default: general information
#                 self._build_general_info_chain()
#             )
#         )

#     def _retrieve_relevant_content(self, query, k=TOP_N_RESULTS):
#         print('optimized_qury', query)
#         results = self.vector_store.similarity_search(
#             query, k=k
#         )
#         context = '\n'.join(
#             result.page_content for result in results
#         )

#         return context.strip()




# Custom async runnable classes


# services.py - Async Service
import asyncio
from typing import AsyncGenerator, Dict, Any
from asgiref.sync import sync_to_async

from src.chatbot.mixins import AsyncGeneralInfoMixin, AsyncJewelryConsultationMixin
from src.chatbot.utils import async_build_conversation_history
from src.chatbot.handlers import ASYNC_HANDLERS_MAPPER


class AsyncChatbotService(AsyncGeneralInfoMixin, AsyncJewelryConsultationMixin):
    """Async chatbot service for handling customer interactions."""

    def __init__(self, session_id: str, vector_store, memory, app, llm, customer_query: str):
        self.session_id = session_id
        self.vector_store = vector_store
        self.memory = memory
        self.app = app
        self.llm = llm
        self.customer_query = customer_query
        self.config = {"configurable": {"thread_id": session_id}}

    async def generate_response_stream(self) -> AsyncGenerator[str, None]:
        """Generate streaming response asynchronously"""
        try:
            # Get conversation state asynchronously
            conversation_state = await sync_to_async(
                self.memory.get, thread_sensitive=True
            )(self.config)
            
            conversation_history = await async_build_conversation_history(
                self.customer_query, conversation_state
            )

            # Create optimized query for intent
            optimized_query_for_intent = await self._create_optimized_query_for_intent(
                conversation_history
            )

            # Extract customer intent
            customer_intent = await self._extract_customer_intent(
                optimized_query_for_intent
            )

            # Determine processing path
            if customer_intent == 'JEWELRY_CONSULTATION':
                async for chunk in self._handle_jewelry_consultation(conversation_history):
                    yield chunk
            else:
                async for chunk in self._handle_general_info(customer_intent, conversation_history):
                    yield chunk

        except Exception as e:
            yield f'data: {{"error": "Service error: {str(e)}"}}\n\n'

    async def _create_optimized_query_for_intent(self, conversation_history: str) -> str:
        """Create optimized query for intent determination"""
        return await ASYNC_HANDLERS_MAPPER['create_optimized_query_for_intent'](
            self.llm,
            customer_query=self.customer_query,
            conversation_history=conversation_history
        )

    async def _extract_customer_intent(self, optimized_query: str) -> str:
        """Extract customer intent from query"""
        result = await ASYNC_HANDLERS_MAPPER['extract_customer_intent'](
            self.llm,
            optimized_query_for_intent=optimized_query
        )
        # Handle the result properly
        if isinstance(result, dict):
            return result.get('primary_intent', 'GENERAL')
        return result

    async def _handle_jewelry_consultation(self, conversation_history: str) -> AsyncGenerator[str, None]:
        """Handle jewelry consultation flow"""
        try:
            # Get relevant context from vector store
            context = await self._get_relevant_context()
            
            # Create optimized query for search
            optimized_query_for_search = await self._create_optimized_query_for_search(
                conversation_history
            )

            # Process jewelry consultation chain
            chain_inputs = {
                'customer_query': self.customer_query,
                'optimized_query_for_search': optimized_query_for_search,
                'context': context,
                'conversation_history': conversation_history
            }

            jewelry_chain = await self._build_jewelry_consultation_chain()
            result = await jewelry_chain.ainvoke(chain_inputs)
            
            # Stream the response
            yield f'data: {{"response": "{self._escape_json(str(result))}", "type": "jewelry_consultation"}}\n\n'
            
        except Exception as e:
            yield f'data: {{"error": "Jewelry consultation error: {str(e)}"}}\n\n'

    async def _handle_general_info(self, intent: str, conversation_history: str) -> AsyncGenerator[str, None]:
        """Handle general information requests"""
        try:
            context = await self._get_relevant_context()
            
            chain = await self._build_general_info_chain()
            result = await chain.ainvoke({
                'customer_intent': intent,
                'context': context,
                'customer_query': self.customer_query,
                'conversation_history': conversation_history
            })
            
            # Stream the response
            yield f'data: {{"response": "{self._escape_json(str(result))}", "type": "general_info"}}\n\n'
            
        except Exception as e:
            yield f'data: {{"error": "General info error: {str(e)}"}}\n\n'

    async def _get_relevant_context(self) -> str:
        """Get relevant context from vector store"""
        try:
            # Run similarity search in thread pool
            docs = await sync_to_async(
                self.vector_store.similarity_search, 
                thread_sensitive=True
            )(self.customer_query, k=5)
            
            return '\n'.join([doc.page_content for doc in docs])
        except Exception as e:
            print(f"Error getting relevant context: {e}")
            return ""

    async def _create_optimized_query_for_search(self, conversation_history: str) -> str:
        """Create optimized query for search"""
        return await ASYNC_HANDLERS_MAPPER['create_optimized_query_for_search'](
            self.llm,
            customer_query=self.customer_query,
            conversation_history=conversation_history
        )

    def _escape_json(self, text: str) -> str:
        """Escape text for JSON output"""
        return text.replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')