from django.conf import settings

import openai
import chromadb


class ClientAdapter:
    """Singleton adapter that provides access to the OpenAI client and a ChromaDB collection."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY,
            )
            cls._instance.chroma_client = chromadb.Client()
            cls._instance.collection = cls._instance.chroma_client.get_or_create_collection(
                "new_db",
            )

        return cls._instance

    @classmethod
    def get_client(cls):
        """Return the initialized OpenAI client instance."""
        return cls().client

    @classmethod
    def get_collection(cls):
        """Return the ChromaDB collection instance for vector storage and queries."""
        return cls().collection
