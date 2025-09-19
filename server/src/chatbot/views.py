import json
import uuid

from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from src.chatbot.factories import ChatbotServiceFactory
from src.chatbot.serializers import ChatRequestSerializer
from src.chatbot.constants import ERROR_RESPONSE_OBJECT


class ChatBotAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = ChatRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    ERROR_RESPONSE_OBJECT,
                    status=status.HTTP_400_BAD_REQUEST
                )

            customer_query = serializer.validated_data['message']
            session_id = self._get_or_create_session_id(
                request
            )

            chatbot_service = ChatbotServiceFactory.create(
                session_id,
                customer_query,
            )

            def generate_response():
                try:
                    for chunk in chatbot_service.generate_response_stream():
                        yield chunk
                except Exception as e:
                    yield f'data: {json.dumps({'error': str(e)})}\n\n'

            return StreamingHttpResponse(
                generate_response(),
                content_type='text/plain',
            )

        except Exception as e:
            return Response(
                {'error': str(e), 'success': False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    def _get_or_create_session_id(request):
        session_id = request.data.get('session_id')

        if not session_id:
            session_id = str(uuid.uuid4())

        return session_id
