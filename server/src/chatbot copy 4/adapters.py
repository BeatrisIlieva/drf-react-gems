# from pinecone import Pinecone as PineconeClient
# from langchain_pinecone import Pinecone
# import os

# from langchain_openai import ChatOpenAI
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import START, MessagesState, StateGraph
# from langchain_openai import OpenAIEmbeddings

# from src.chatbot.config import DIMENSIONS, EMBEDDING_MODEL, LLM_MODEL, MAX_TOKENS, TEMPERATURE, TOP_P, FREQUENCY_PENALTY, PRESENCE_PENALTY


# class LLMAdapter:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)

#             cls._instance.llm = cls._initialize()

#         return cls._instance

#     @classmethod
#     def get_llm(cls):
#         return cls().llm

#     @classmethod
#     def _initialize(cls):
#         return ChatOpenAI(
#             model=LLM_MODEL,
#             max_tokens=MAX_TOKENS,
#             temperature=TEMPERATURE,
#             top_p=TOP_P,
#             frequency_penalty=FREQUENCY_PENALTY,
#             presence_penalty=PRESENCE_PENALTY,
#         )


# class MemoryAdapter:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)

#             cls._initialize()

#         return cls._instance

#     @classmethod
#     def _initialize(cls):
#         cls._instance.memory = MemorySaver()
#         cls._instance.workflow = StateGraph(state_schema=MessagesState)
#         cls._instance.workflow.add_edge(START, "model")
#         cls._instance.workflow.add_node("model", cls._instance._call_model)
#         cls._instance.app = cls._instance.workflow.compile(
#             checkpointer=cls._instance.memory)

#     @classmethod
#     def get_memory(cls):
#         return cls().memory

#     @classmethod
#     def get_app(cls):
#         return cls().app

#     @classmethod
#     def _call_model(cls, state: MessagesState):

#         llm = LLMAdapter.get_llm()
#         response = llm.invoke(state["messages"])

#         return {"messages": response}


# class VectorStoreAdapter:
#     """Adapter to connect to existing Pinecone vector store."""
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             cls._instance.vectorstore = cls._initialize()
#         return cls._instance

#     @classmethod
#     def get_vectorstore(cls):
#         """Get the vector store instance."""
#         return cls().vectorstore

#     @classmethod
#     def _initialize(cls):
#         """Initialize connection to existing Pinecone index."""
#         # Validate environment variables
#         api_key = os.getenv("PINECONE_API_KEY")
#         if not api_key:
#             raise ValueError(
#                 "PINECONE_API_KEY environment variable is required")

#         openai_api_key = os.getenv("OPENAI_API_KEY")
#         if not openai_api_key:
#             raise ValueError("OPENAI_API_KEY environment variable is required")

#         # Get index name
#         index_name = os.getenv("PINECONE_INDEX_NAME", "drf-react-gems-index")

#         # Initialize Pinecone client and check if index exists
#         pc = PineconeClient(api_key=api_key)
#         existing_indexes = pc.list_indexes().names()

#         if index_name not in existing_indexes:
#             raise ValueError(
#                 f"Pinecone index '{index_name}' not found. "
#                 f"Available indexes: {', '.join(existing_indexes) if existing_indexes else 'None'}. "
#                 f"Please run 'python manage.py setup_vectorstore' first."
#             )

#         # Initialize embedding model (same as used in management command)
#         embedding_model = OpenAIEmbeddings(
#             model=EMBEDDING_MODEL, dimensions=DIMENSIONS)

#         # Connect to existing Pinecone vector store
#         vectorstore = Pinecone.from_existing_index(
#             index_name=index_name,
#             embedding=embedding_model,
#             text_key="text"
#         )

#         return vectorstore









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
