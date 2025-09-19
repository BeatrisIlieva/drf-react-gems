# import json
# import uuid

# from django.http import StreamingHttpResponse
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from rest_framework import status

# from src.chatbot.factories import ChatbotServiceFactory
# from src.chatbot.serializers import ChatRequestSerializer
# from src.chatbot.constants import ERROR_RESPONSE_OBJECT


# class ChatBotAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             serializer = ChatRequestSerializer(data=request.data)
#             if not serializer.is_valid():
#                 return Response(
#                     ERROR_RESPONSE_OBJECT,
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             customer_query = serializer.validated_data['message']
#             session_id = self._get_or_create_session_id(
#                 request
#             )

#             chatbot_service = ChatbotServiceFactory.create(
#                 session_id,
#                 customer_query,
#             )

#             def generate_response():
#                 try:
#                     for chunk in chatbot_service.generate_response_stream():
#                         yield chunk
#                 except Exception as e:
#                     yield f'data: {json.dumps({'error': str(e)})}\n\n'

#             return StreamingHttpResponse(
#                 generate_response(),
#                 content_type='text/plain',
#             )

#         except Exception as e:
#             return Response(
#                 {'error': str(e), 'success': False},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#     @staticmethod
#     def _get_or_create_session_id(request):
#         session_id = request.data.get('session_id')

#         if not session_id:
#             session_id = str(uuid.uuid4())

#         return session_id



# import json
# import uuid

# from django.http import StreamingHttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# from src.chatbot.factories import ChatbotServiceFactory
# from src.chatbot.constants import ERROR_RESPONSE_OBJECT

# # Optional: reuse DRF serializer manually
# from src.chatbot.serializers import ChatRequestSerializer


# @csrf_exempt  # only if you want to allow POST without CSRF token
# def chatbot_view(request):
#     if request.method != "POST":
#         return JsonResponse(
#             {"error": "POST requests only", "success": False},
#             status=405
#         )

#     try:
#         # parse JSON body
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse(ERROR_RESPONSE_OBJECT, status=400)

#         # Use DRF serializer manually (optional)
#         serializer = ChatRequestSerializer(data=data)
#         if not serializer.is_valid():
#             return JsonResponse(ERROR_RESPONSE_OBJECT, status=400)

#         customer_query = serializer.validated_data['message']
#         session_id = _get_or_create_session_id(data)

#         chatbot_service = ChatbotServiceFactory.create(
#             session_id,
#             customer_query,
#         )

#         def generate_response():
#             try:
#                 for chunk in chatbot_service.generate_response_stream():
#                     yield chunk
#             except Exception as e:
#                 yield f'data: {json.dumps({"error": str(e)})}\n\n'

#         return StreamingHttpResponse(
#             generate_response(),
#             content_type='text/plain',
#         )

#     except Exception as e:
#         return JsonResponse(
#             {"error": str(e), "success": False},
#             status=500
#         )


# def _get_or_create_session_id(data):
#     session_id = data.get('session_id')
#     if not session_id:
#         session_id = str(uuid.uuid4())
#     return session_id

# views.py - Async Chatbot View
import json
import uuid
from typing import AsyncGenerator

from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from asgiref.sync import sync_to_async

from src.chatbot.factories import AsyncChatbotServiceFactory
from src.chatbot.constants import ERROR_RESPONSE_OBJECT
from src.chatbot.serializers import ChatRequestSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AsyncChatBotView(View):
    """Async chatbot view using Django's async support"""
    
    async def post(self, request):
        try:
            # Parse JSON body
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse(ERROR_RESPONSE_OBJECT, status=400)

            # Validate data using serializer (run in thread pool since it's sync)
            serializer = await sync_to_async(ChatRequestSerializer)(data=data)
            is_valid = await sync_to_async(serializer.is_valid)()
            if not is_valid:
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

    def _get_or_create_session_id(self, data):
        session_id = data.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
        return session_id