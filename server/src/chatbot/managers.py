import os
from collections import defaultdict
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory

class ComponentManager:
    """Singleton-like manager for initializing and accessing shared components."""
    _instance = None
    _vectorstore = None
    _llm = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
            
        return cls._instance

    def _initialize(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(base_dir, "docs", "product_catalog.pdf")

        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " ", ""]
        )

        chunks = text_splitter.split_documents(pages)

        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

        self._vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=None
        )

        self._llm = ChatOpenAI(
            model="gpt-4o-mini",
            max_tokens=100,
            temperature=0.5,
            top_p=0.5,
            frequency_penalty=1.0,
            presence_penalty=1.0,
            streaming=True,
        )

    @property
    def vectorstore(self):
        return self._vectorstore

    @property
    def llm(self):
        return self._llm


class MemoryManager:
    """Manages conversation memories per session."""
    _memories = defaultdict(lambda: None)

    @classmethod
    def get_or_create_memory(cls, session_id):
        if cls._memories[session_id] is None:
            cls._memories[session_id] = ConversationBufferMemory(
                memory_key="chat_history",
                input_key="input",
                output_key="text",
                return_messages=False
            )
            
        return cls._memories[session_id]