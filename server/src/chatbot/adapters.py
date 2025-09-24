import os

from pinecone import Pinecone as PineconeClient
from langchain_pinecone import Pinecone
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory

from src.chatbot.config import (
    DIMENSIONS,
    EMBEDDING_MODEL,
    LLM_MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    TOP_P,
    FREQUENCY_PENALTY,
    PRESENCE_PENALTY
)


class LLMAdapter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.llm = cls._initialize_llm()
            cls._instance.streaming_llm = cls._initialize_streaming_llm()

        return cls._instance

    @classmethod
    def get_llm(cls):
        return cls().llm

    @classmethod
    def get_streaming_llm(cls):
        return cls().streaming_llm

    @classmethod
    def _initialize_llm(cls):
        return ChatOpenAI(
            model=LLM_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
        )

    @classmethod
    def _initialize_streaming_llm(cls):
        return ChatOpenAI(
            model=LLM_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
            streaming=True,
        )


class MemoryAdapter:
    _sessions = {}

    @classmethod
    def get_memory(cls, session_id):
        if session_id not in cls._sessions:
            cls._sessions[session_id] = ConversationBufferMemory(
                memory_key="conversation_memory",
                return_messages=True,
                output_key="response"
            )
        return cls._sessions[session_id]


class VectorStoreAdapter:
    """Adapter to connect to existing Pinecone vector store."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.vectorstore = cls._initialize()
        return cls._instance

    @classmethod
    def get_vectorstore(cls):
        """Get the vector store instance."""
        return cls().vectorstore

    @classmethod
    def _initialize(cls):
        """Initialize connection to existing Pinecone index."""
        # Validate environment variables
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError(
                "PINECONE_API_KEY environment variable is required")

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

        # Initialize embedding model (same as used in management command)
        embedding_model = OpenAIEmbeddings(
            model=EMBEDDING_MODEL, dimensions=DIMENSIONS)

        # Connect to existing Pinecone vector store
        vectorstore = Pinecone.from_existing_index(
            index_name=index_name,
            embedding=embedding_model,
            text_key="text"
        )

        return vectorstore