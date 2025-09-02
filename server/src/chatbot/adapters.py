import os
import re

from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings


class LLMAdapter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.llm = cls._initialize()

        return cls._instance

    @classmethod
    def get_llm(cls):
        return cls().llm

    @classmethod
    def _initialize(cls):
        return ChatOpenAI(
            model="gpt-4o-mini",
            max_tokens=120,
            temperature=0,
            top_p=0,
            frequency_penalty=1.0,
            presence_penalty=1.0,
            streaming=True,
        )


class MemoryAdapter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._initialize()

        return cls._instance

    @classmethod
    def _initialize(cls):
        cls._instance.memory = MemorySaver()
        cls._instance.workflow = StateGraph(state_schema=MessagesState)
        cls._instance.workflow.add_edge(START, "model")
        cls._instance.workflow.add_node("model", cls._instance._call_model)
        cls._instance.app = cls._instance.workflow.compile(
            checkpointer=cls._instance.memory)

    @classmethod
    def get_memory(cls):
        return cls().memory

    @classmethod
    def get_app(cls):
        return cls().app

    @classmethod
    def _call_model(cls, state: MessagesState):

        llm = LLMAdapter.get_llm()
        response = llm.invoke(state["messages"])

        return {"messages": response}


# class VectorStoreAdapter:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)

#             cls._instance.vectorstore = cls._initialize()

#         return cls._instance

#     @classmethod
#     def get_vectorstore(cls):
#         return cls().vectorstore

#     @classmethod
#     def _initialize(cls):
#         embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

#         product_data_pages = cls._create_pages_from_pdf('product_data.pdf')
#         product_data_chunks = cls._create_chunks_using_regex(
#             product_data_pages)

#         all_chunks = product_data_chunks

#         return cls._create_vector_store(all_chunks, embedding_model)

#     @classmethod
#     def _create_pages_from_pdf(cls, document_name):
#         base_dir = os.path.dirname(os.path.abspath(__file__))
#         pdf_path = os.path.join(base_dir, "docs", document_name)

#         loader = PyPDFLoader(pdf_path)
#         pages = loader.load()

#         return pages

#     @classmethod
#     def _create_chunks_using_regex(cls, pages):
#         full_text = "\n".join([p.page_content for p in pages])

#         product_blocks = re.findall(
#             r"Collection:.*?stars;", full_text, re.DOTALL)

#         chunks = [Document(page_content=block)
#                   for block in product_blocks]

#         return chunks

#     @classmethod
#     def _create_vector_store(cls, chunks, embedding_model):
#         vectorstore = Chroma.from_documents(
#             documents=chunks,
#             embedding=embedding_model,
#             persist_directory=None
#         )

#         return vectorstore


import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from pinecone import Pinecone as PineconeClient


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
            raise ValueError("PINECONE_API_KEY environment variable is required")
        
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Get index name
        index_name = os.getenv("PINECONE_INDEX_NAME", "chatbot-index")
        
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
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Connect to existing Pinecone vector store
        vectorstore = Pinecone(
            index=pc.Index(index_name),
            embedding=embedding_model,
            text_key="text"
        )
        
        return vectorstore