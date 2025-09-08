import os
import hashlib
import json
from django.conf import settings
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from src.chatbot.serializers import ChatRequestSerializer
from src.chatbot.constants import ERROR_RESPONSE_OBJECT
from src.chatbot.services import ChatbotService

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
os.environ["LANGSMITH_API_KEY"] = settings.LANGSMITH_API_KEY
os.environ["LANGSMITH_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY
os.environ["PINECONE_INDEX_NAME"] = settings.PINECONE_INDEX_NAME
os.environ["LANGSMITH_TRACING_V2"] = "true"


class ChatBotAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # Validate input
            serializer = ChatRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(ERROR_RESPONSE_OBJECT, status=status.HTTP_400_BAD_REQUEST)

            user_query = serializer.validated_data['message']
            session_id = self._get_or_create_session_id(request)
            
            
            def generate_response():
                try:
                    for chunk in ChatbotService.generate_response_stream(user_query, session_id):
                        yield chunk
                except Exception as e:
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"

            return StreamingHttpResponse(generate_response(), content_type='text/plain')

        except Exception as e:
            return Response({"error": str(e), "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def _get_or_create_session_id(request):
        session_id = request.data.get('session_id')
        if not session_id:
            session_data = f"{request.META.get('REMOTE_ADDR', 'unknown')}"
            session_id = hashlib.md5(session_data.encode()).hexdigest()[:12]
        return session_id
