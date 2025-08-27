import os
import re

from pdfminer.high_level import extract_text

from django.http import StreamingHttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


from src.chatbot.adapters import ClientAdapter
from src.chatbot.serializers import ChatRequestSerializer
from src.chatbot.services import AIResponseService, QueryEmbeddingService, VectorSearchService

from src.chatbot.constants import ERROR_RESPONSE_OBJECT
from src.chatbot.config import SYSTEM_MESSAGE, TOOLS


class ChatBotAPIView(APIView):
    permission_classes = [AllowAny]
    """
    Main chatbot API endpoint that handles user queries and returns AI responses.
    """

    def post(self, request):
        """
        Handle POST requests for chatbot interactions

        Expected payload:
        {
            "message": "User's question"
        }

        Returns:
        {
            "response": "AI response",
            "success": true/false,
        }
        """
        try:
            # Validate input
            serializer = ChatRequestSerializer(data=request.data)

            if not serializer.is_valid():
                return Response(
                    ERROR_RESPONSE_OBJECT,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user_message = serializer.validated_data['message']

            ai_response = self._get_ai_response(user_message)

            streaming_response = StreamingHttpResponse(
                AIResponseService.generate_event_stream(ai_response),
                content_type='text/event-stream'
            )

            if not streaming_response:
                return Response(
                    ERROR_RESPONSE_OBJECT,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            streaming_response['Cache-Control'] = 'no-cache'
            # Disable buffering in proxies like Nginx
            streaming_response['X-Accel-Buffering'] = 'no'

            return streaming_response

        except Exception:
            return Response(
                ERROR_RESPONSE_OBJECT,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _get_ai_response(self, user_message):
        client = ClientAdapter.get_client()
        collection = ClientAdapter.get_collection()

        self.store_embeddings_and_chunks_into_db(client, collection)

        query_embedding = QueryEmbeddingService.generate_query_embedding(
            user_message,
            client,
        )

        if not query_embedding:
            return None

        search_results = VectorSearchService.perform_vector_search(
            query_embedding,
            collection,
        )

        ai_response = AIResponseService.generate_ai_response(
            TOOLS,
            SYSTEM_MESSAGE,
            user_message,
            search_results,
            client,
        )

        return ai_response

    def store_embeddings_and_chunks_into_db(self, client, collection):
        raw_text = self.load_pdf_text()
        punctual_chunks = self.generate_chunks(
            raw_text, chunk_size=600, overlap=100)
        embeddings = self.generate_embeddings(punctual_chunks, client)

        ids = [f"chunk_{i}" for i in range(len(embeddings))]
        documents = list(embeddings.keys())
        embedding_vectors = list(embeddings.values())

        collection.add(
            embeddings=embedding_vectors,
            documents=documents,
            ids=ids
        )

    @staticmethod
    def generate_chunks(text, chunk_size=500, overlap=100):
        split_points = r'(?<=[.!?;\n])\s*'
        sentences = re.split(split_points, text)

        chunks = []
        current_chunk = ""
        i = 0
        while i < len(sentences):
            sentence = sentences[i]

            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence
                i += 1
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    overlap_start = max(0, len(current_chunk) - overlap)
                    current_chunk = current_chunk[overlap_start:] + sentence
                    i += 1
                else:
                    chunks.append(sentence[:chunk_size].strip())
                    sentences[i] = sentence[chunk_size:]
                    if not sentences[i]:
                        i += 1

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    @staticmethod
    def generate_embeddings(chunks, client, model="text-embedding-ada-002"):
        chunk_embeddings = {}

        try:
            response = client.embeddings.create(
                input=chunks,
                model=model
            )
            for i, chunk in enumerate(chunks):
                if i < len(response.data):
                    chunk_embeddings[chunk] = response.data[i].embedding
                else:
                    print(f"Warning: No embedding returned for chunk {i+1}.")

            return chunk_embeddings
        except Exception as e:
            print(f"An error occurred during embedding generation: {e}")
            return None

    @staticmethod
    def load_pdf_text(filename="product_catalog.pdf"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(base_dir, "docs", filename)

        return extract_text(pdf_path)
