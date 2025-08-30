import os

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph


class LLMAdapter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.llm = ChatOpenAI(
                model="gpt-4o-mini",
                max_tokens=100,
                temperature=0,
                top_p=0,
                frequency_penalty=1.0,
                presence_penalty=1.0,
                streaming=True,
            )

        return cls._instance

    @classmethod
    def get_llm(cls):
        return cls().llm


class VectorstoreAdapter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            base_dir = os.path.dirname(os.path.abspath(__file__))
            pdf_path = os.path.join(base_dir, "docs", "product_catalog.pdf")

            loader = PyPDFLoader(pdf_path)
            pages = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=540,
                chunk_overlap=0,
                separators=["\n\n", ". ", "!", '\n']
            )

            chunks = text_splitter.split_documents(pages)

            embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

            cls._instance.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=embedding_model,
                persist_directory=None
            )

        return cls._instance

    @classmethod
    def get_vectorstore(cls):
        return cls().vectorstore


class MemoryAdapter:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.memory = MemorySaver()
            cls._instance.workflow = StateGraph(state_schema=MessagesState)
            cls._instance.workflow.add_edge(START, "model")
            cls._instance.workflow.add_node("model", cls._instance._call_model)
            cls._instance.app = cls._instance.workflow.compile(
                checkpointer=cls._instance.memory)

        return cls._instance

    @classmethod
    def get_memory(cls):
        return cls().memory

    @classmethod
    def get_app(cls):
        return cls().app

    def _call_model(self, state: MessagesState):
        """
        For streaming within nodes, you need to accumulate the response
        and return the complete message
        """
        llm = LLMAdapter.get_llm()
        response = llm.invoke(state["messages"])

        return {"messages": response}
