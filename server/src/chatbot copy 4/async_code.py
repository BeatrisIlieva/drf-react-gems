# views.py - Async Chatbot View
import json
import uuid
import asyncio
from typing import AsyncGenerator

from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from asgiref.sync import sync_to_async, async_to_sync

from src.chatbot.factories import AsyncChatbotServiceFactory
from src.chatbot.constants import ERROR_RESPONSE_OBJECT
from src.chatbot.serializers import ChatRequestSerializer


class AsyncChatBotView(View):
    """Async chatbot view using Django's async support"""
    
    @method_decorator(csrf_exempt)
    async def post(self, request):
        try:
            # Parse JSON body asynchronously
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse(ERROR_RESPONSE_OBJECT, status=400)

            # Validate data using serializer (run in thread pool since it's sync)
            serializer = await sync_to_async(self._validate_data)(data)
            if not serializer.is_valid():
                return JsonResponse(ERROR_RESPONSE_OBJECT, status=400)

            customer_query = serializer.validated_data['message']
            session_id = self._get_or_create_session_id(data)

            # Create async chatbot service
            chatbot_service = await AsyncChatbotServiceFactory.create(
                session_id,
                customer_query,
            )

            # Create async generator for streaming response
            async def generate_response():
                try:
                    async for chunk in chatbot_service.generate_response_stream():
                        yield chunk
                except Exception as e:
                    yield f'data: {json.dumps({"error": str(e)})}\n\n'

            return StreamingHttpResponse(
                generate_response(),
                content_type='text/plain',
            )

        except Exception as e:
            return JsonResponse(
                {"error": str(e), "success": False},
                status=500
            )

    def _validate_data(self, data):
        """Synchronous validation helper"""
        return ChatRequestSerializer(data=data)

    def _get_or_create_session_id(self, data):
        session_id = data.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
        return session_id


# Alternative function-based async view
@csrf_exempt
async def async_chatbot_view(request):
    """Async function-based view for chatbot"""
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST requests only", "success": False},
            status=405
        )

    try:
        # Parse JSON body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(ERROR_RESPONSE_OBJECT, status=400)

        # Validate data
        serializer = await sync_to_async(ChatRequestSerializer)(data=data)
        is_valid = await sync_to_async(serializer.is_valid)()
        if not is_valid:
            return JsonResponse(ERROR_RESPONSE_OBJECT, status=400)

        customer_query = serializer.validated_data['message']
        session_id = _get_or_create_session_id(data)

        chatbot_service = await AsyncChatbotServiceFactory.create(
            session_id,
            customer_query,
        )

        async def generate_response():
            try:
                async for chunk in chatbot_service.generate_response_stream():
                    yield chunk
            except Exception as e:
                yield f'data: {json.dumps({"error": str(e)})}\n\n'

        return StreamingHttpResponse(
            generate_response(),
            content_type='text/plain',
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e), "success": False},
            status=500
        )


def _get_or_create_session_id(data):
    session_id = data.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


# factories.py - Async Factory
import asyncio
from typing import Optional

from src.chatbot.adapters import AsyncLLMAdapter, AsyncMemoryAdapter, AsyncVectorStoreAdapter
from src.chatbot.services import AsyncChatbotService


class AsyncChatbotServiceFactory:
    """Async factory for creating ChatbotService instances with proper dependencies."""

    @staticmethod
    async def create(session_id: str, customer_query: str) -> 'AsyncChatbotService':
        # Initialize all adapters concurrently
        vector_store_task = AsyncVectorStoreAdapter.get_vectorstore()
        memory_task = AsyncMemoryAdapter.get_memory()
        app_task = AsyncMemoryAdapter.get_app()
        llm_task = AsyncLLMAdapter.get_llm()

        # Wait for all adapters to be ready
        vector_store, memory, app, llm = await asyncio.gather(
            vector_store_task,
            memory_task,
            app_task,
            llm_task
        )

        return AsyncChatbotService(
            session_id=session_id,
            vector_store=vector_store,
            memory=memory,
            app=app,
            llm=llm,
            customer_query=customer_query,
        )


# adapters.py - Async Adapters
import asyncio
import os
from typing import Optional, Any
from asgiref.sync import sync_to_async

from pinecone import Pinecone as PineconeClient
from langchain_pinecone import Pinecone
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from src.chatbot.config import (
    DIMENSIONS, EMBEDDING_MODEL, LLM_MODEL, MAX_TOKENS, 
    TEMPERATURE, TOP_P, FREQUENCY_PENALTY, PRESENCE_PENALTY
)


class AsyncLLMAdapter:
    _instance: Optional['AsyncLLMAdapter'] = None
    _lock = asyncio.Lock()

    def __init__(self):
        self.llm: Optional[ChatOpenAI] = None

    @classmethod
    async def get_llm(cls) -> ChatOpenAI:
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
                    await cls._instance._initialize()
        
        if cls._instance.llm is None:
            await cls._instance._initialize()
            
        return cls._instance.llm

    async def _initialize(self):
        """Initialize LLM asynchronously"""
        # Run LLM initialization in thread pool since it might involve I/O
        self.llm = await sync_to_async(self._create_llm)()

    def _create_llm(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=LLM_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
        )


class AsyncMemoryAdapter:
    _instance: Optional['AsyncMemoryAdapter'] = None
    _lock = asyncio.Lock()

    def __init__(self):
        self.memory: Optional[MemorySaver] = None
        self.app: Optional[Any] = None
        self.workflow: Optional[StateGraph] = None

    @classmethod
    async def get_memory(cls) -> MemorySaver:
        await cls._ensure_initialized()
        return cls._instance.memory

    @classmethod
    async def get_app(cls) -> Any:
        await cls._ensure_initialized()
        return cls._instance.app

    @classmethod
    async def _ensure_initialized(cls):
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
                    await cls._instance._initialize()

    async def _initialize(self):
        """Initialize memory and workflow asynchronously"""
        await sync_to_async(self._setup_memory_and_workflow)()

    def _setup_memory_and_workflow(self):
        self.memory = MemorySaver()
        self.workflow = StateGraph(state_schema=MessagesState)
        self.workflow.add_edge(START, "model")
        self.workflow.add_node("model", self._call_model)
        self.app = self.workflow.compile(checkpointer=self.memory)

    async def _call_model(self, state: MessagesState):
        """Async model calling"""
        llm = await AsyncLLMAdapter.get_llm()
        # Make the LLM call async
        response = await sync_to_async(llm.invoke)(state["messages"])
        return {"messages": response}


class AsyncVectorStoreAdapter:
    _instance: Optional['AsyncVectorStoreAdapter'] = None
    _lock = asyncio.Lock()

    def __init__(self):
        self.vectorstore: Optional[Pinecone] = None

    @classmethod
    async def get_vectorstore(cls) -> Pinecone:
        if cls._instance is None:
            async with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
                    await cls._instance._initialize()
        
        if cls._instance.vectorstore is None:
            await cls._instance._initialize()
            
        return cls._instance.vectorstore

    async def _initialize(self):
        """Initialize vector store asynchronously"""
        self.vectorstore = await sync_to_async(self._create_vectorstore)()

    def _create_vectorstore(self) -> Pinecone:
        """Create vectorstore synchronously (called in thread pool)"""
        # Validate environment variables
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable is required")

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # Get index name
        index_name = os.getenv("PINECONE_INDEX_NAME", "drf-react-gems-index")

        # Initialize Pinecone client and check if index exists
        pc = PineconeClient(api_key=api_key)
        existing_indexes = pc.list_indexes().names()

        if index_name not in existing_indexes:
            raise ValueError(
                f"Pinecone index '{index_name}' not found. "
                f"Available indexes: {', '.join(existing_indexes) if existing_indexes else 'None'}. "
                f"Please run 'python manage.py setup_vectorstore' first."
            )

        # Initialize embedding model
        embedding_model = OpenAIEmbeddings(
            model=EMBEDDING_MODEL, 
            dimensions=DIMENSIONS
        )

        # Connect to existing Pinecone vector store
        vectorstore = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=embedding_model,
            text_key="text"
        )

        return vectorstore


# services.py - Async Service
import asyncio
from typing import AsyncGenerator, Dict, Any, Optional
from asgiref.sync import sync_to_async

from src.chatbot.mixins import AsyncGeneralInfoMixin, AsyncJewelryConsultationMixin
from src.chatbot.utils import build_conversation_history


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
            
            conversation_history = await sync_to_async(build_conversation_history)(
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
        from src.chatbot.handlers import ASYNC_HANDLERS_MAPPER
        
        return await ASYNC_HANDLERS_MAPPER['create_optimized_query_for_intent'](
            self.llm,
            customer_query=self.customer_query,
            conversation_history=conversation_history
        )

    async def _extract_customer_intent(self, optimized_query: str) -> str:
        """Extract customer intent from query"""
        from src.chatbot.handlers import ASYNC_HANDLERS_MAPPER
        
        return await ASYNC_HANDLERS_MAPPER['extract_customer_intent'](
            self.llm,
            optimized_query_for_intent=optimized_query
        )

    async def _handle_jewelry_consultation(self, conversation_history: str) -> AsyncGenerator[str, None]:
        """Handle jewelry consultation flow"""
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
        if hasattr(result, '__iter__'):
            for chunk in result:
                yield f'data: {{"response": "{chunk}"}}\n\n'
        else:
            yield f'data: {{"response": "{result}"}}\n\n'

    async def _handle_general_info(self, intent: str, conversation_history: str) -> AsyncGenerator[str, None]:
        """Handle general information requests"""
        context = await self._get_relevant_context()
        
        chain = await self._build_general_info_chain()
        result = await chain.ainvoke({
            'customer_intent': intent,
            'context': context,
            'customer_query': self.customer_query,
            'conversation_history': conversation_history
        })
        
        # Stream the response
        if hasattr(result, '__iter__'):
            for chunk in result:
                yield f'data: {{"response": "{chunk}"}}\n\n'
        else:
            yield f'data: {{"response": "{result}"}}\n\n'

    async def _get_relevant_context(self) -> str:
        """Get relevant context from vector store"""
        # Run similarity search in thread pool
        docs = await sync_to_async(
            self.vector_store.similarity_search, 
            thread_sensitive=True
        )(self.customer_query, k=5)
        
        return '\n'.join([doc.page_content for doc in docs])

    async def _create_optimized_query_for_search(self, conversation_history: str) -> str:
        """Create optimized query for search"""
        from src.chatbot.handlers import ASYNC_HANDLERS_MAPPER
        
        return await ASYNC_HANDLERS_MAPPER['create_optimized_query_for_search'](
            self.llm,
            customer_query=self.customer_query,
            conversation_history=conversation_history
        )


# mixins.py - Async Mixins (partial example)
import asyncio
from typing import Any
from asgiref.sync import sync_to_async

from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch


class AsyncGeneralInfoMixin:
    """Async mixin for general information handling."""
    PRODUCT_TO_RECOMMEND = None

    async def _build_general_info_chain(self):
        """Build chain for general information responses."""
        from src.chatbot.handlers import ASYNC_HANDLERS_MAPPER
        
        async def handle_general_info(inputs):
            return await ASYNC_HANDLERS_MAPPER[inputs['customer_intent']](
                self.llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
            )
        
        return RunnableLambda(handle_general_info)


class AsyncJewelryConsultationMixin:
    """Async mixin for building conditional chains."""

    async def _build_jewelry_consultation_chain(self):
        """Build the complete jewelry consultation process chain."""
        preference_chain = await self._build_preference_extraction_chain()
        
        async def process_jewelry_consultation(inputs):
            # Extract preferences
            inputs_with_prefs = await preference_chain.ainvoke(inputs)
            
            # Check product match status
            product_match_status = await self._check_products_individually(inputs_with_prefs)
            inputs_with_prefs['product_match_status'] = product_match_status
            
            # Branch based on match status
            if product_match_status.startswith('FOUND'):
                chain = await self._build_discovery_or_recommend_chain()
            else:
                chain = await self._build_available_options_navigator_chain()
            
            return await chain.ainvoke(inputs_with_prefs)
        
        return RunnableLambda(process_jewelry_consultation)

    async def _build_preference_extraction_chain(self):
        """Build chain for extracting customer preferences."""
        from src.chatbot.strategies import PreferenceDiscoveryStrategy
        from src.chatbot.handlers import ASYNC_HANDLERS_MAPPER
        
        async def extract_preferences(inputs):
            result = dict(inputs)
            
            # Extract preferences concurrently
            tasks = []
            for preference_key, config in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE.items():
                task = ASYNC_HANDLERS_MAPPER['extract_customer_preferences'](
                    self.llm,
                    config['model'],
                    optimized_query=inputs['optimized_query_for_search']
                )
                tasks.append((preference_key, task))
            
            # Wait for all preference extractions
            for preference_key, task in tasks:
                result[preference_key] = await task
                
            return result
        
        return RunnableLambda(extract_preferences)

    async def _check_products_individually(self, inputs):
        """Check each product individually until a match is found."""
        context = inputs["context"]
        preferences = {k: v for k, v in self._extract_safe_preferences(inputs).items() 
                      if k != 'purchase_type'}

        # Extract individual products
        individual_products = await sync_to_async(self._extract_individual_products)(context)
        
        if not individual_products:
            return "NOT_FOUND: No products found in context"

        # Check products concurrently (with limit to avoid overwhelming the API)
        semaphore = asyncio.Semaphore(3)  # Limit concurrent requests
        
        async def check_single_product(i, product):
            async with semaphore:
                try:
                    from src.chatbot.handlers import ASYNC_HANDLERS_MAPPER
                    result = await ASYNC_HANDLERS_MAPPER['check_for_products_matching_customer_preferences'](
                        self.llm,
                        context=product,
                        **preferences
                    )
                    return i, product, result
                except Exception as e:
                    print(f"Error checking product {i}: {e}")
                    return i, product, None

        # Create tasks for all products
        tasks = [
            check_single_product(i, product) 
            for i, product in enumerate(individual_products, 1)
        ]
        
        # Process results as they complete
        for task in asyncio.as_completed(tasks):
            i, product, result = await task
            
            if result and not result.startswith('NOT_FOUND'):
                AsyncJewelryConsultationMixin.PRODUCT_TO_RECOMMEND = product
                return f"FOUND: Match found in product {i}"
        
        return "NOT_FOUND: No matching products found"

    # ... other methods remain similar but with async/await patterns


# handlers.py - Async Handlers (partial example)
import asyncio
from typing import Dict, Any, Callable
from asgiref.sync import sync_to_async

from src.chatbot.utils import generate_formatted_response
from src.chatbot.models import CustomerIntent, CustomerIntentEnum


async def async_generate_formatted_response(llm, system_message, human_message, 
                                          response_format, response_model=None, **kwargs):
    """Async version of generate_formatted_response"""
    return await sync_to_async(generate_formatted_response, thread_sensitive=True)(
        llm, system_message, human_message, response_format, response_model, **kwargs
    )


ASYNC_HANDLERS_MAPPER: Dict[str, Callable] = {
    'create_optimized_query_for_intent': lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_QUERY_FOR_INTENT_OPTIMIZER,
        HUMAN_MESSAGE_QUERY_FOR_INTENT_OPTIMIZER,
        'extract_ai_response_content',
        **kwargs
    ),

    'create_optimized_query_for_search': lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER,
        HUMAN_MESSAGE_QUERY_FOR_SEARCH_OPTIMIZER,
        'extract_ai_response_content',
        **kwargs
    ),

    'extract_customer_intent': lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_INTENT_DETERMINER,
        HUMAN_MESSAGE_INTENT_DETERMINER,
        'extract_and_strip_ai_response_content',
        CustomerIntent,
        **kwargs
    ).then(lambda result: result['primary_intent']),

    # Add other handlers following the same pattern...
    
    CustomerIntentEnum.SIZING_HELP: lambda llm, **kwargs: async_generate_formatted_response(
        llm,
        SYSTEM_MESSAGE_COMPANY_SIZE_HELP_HANDLER,
        HUMAN_MESSAGE_COMPANY_SIZE_HELP_HANDLER,
        'destructure_messages',
        **kwargs
    ),

    # ... continue with other handlers
}


# urls.py - URL Configuration
from django.urls import path
from . import views

urlpatterns = [
    # Async class-based view
    path('chatbot/', views.AsyncChatBotView.as_view(), name='async_chatbot'),
    
    # Or async function-based view
    path('chatbot-func/', views.async_chatbot_view, name='async_chatbot_func'),
]