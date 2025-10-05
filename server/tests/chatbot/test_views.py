import json
import uuid
from unittest.mock import Mock, patch, MagicMock
from django.test import TestCase, RequestFactory
from rest_framework import status

from src.chatbot.views import ChatBotView
from src.chatbot.constants import ERROR_RESPONSE_OBJECT


class ChatBotViewTestCase(TestCase):
    """Test suite for ChatBotView"""

    def setUp(self):
        self.factory = RequestFactory()
        self.view = ChatBotView.as_view()
        self.url = '/api/chatbot/chat/'

    def test_post_with_valid_data_and_existing_session_id(self):
        """Test successful chat request with existing session_id"""
        session_id = str(uuid.uuid4())
        data = {
            'message': 'Show me gold necklaces',
            'session_id': session_id
        }

        mock_service = Mock()
        mock_service.generate_response_stream.return_value = [
            f'data: {json.dumps({"session_id": session_id})}\n\n',
            f'data: {json.dumps({"chunk": "Here are "})}\n\n',
            f'data: {json.dumps({"chunk": "some gold necklaces"})}\n\n',
        ]

        with patch('src.chatbot.views.ChatbotServiceFactory.create', return_value=mock_service):
            request = self.factory.post(
                self.url,
                data=json.dumps(data),
                content_type='application/json'
            )
            response = self.view(request)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response['Content-Type'], 'text/plain')
            
            # Verify the response is streaming
            self.assertTrue(response.streaming)
            
            # Collect streamed content
            content = b''.join(response.streaming_content).decode('utf-8')
            self.assertIn('session_id', content)
            self.assertIn('chunk', content)
            self.assertIn('Here are', content)
            self.assertIn('some gold necklaces', content)

    def test_post_with_valid_data_without_session_id(self):
        """Test chat request without session_id - should generate new one"""
        data = {
            'message': 'Show me silver rings'
        }

        mock_service = Mock()
        mock_service.generate_response_stream.return_value = [
            f'data: {json.dumps({"session_id": "generated-uuid"})}\n\n',
            f'data: {json.dumps({"chunk": "Response"})}\n\n',
        ]

        with patch('src.chatbot.views.ChatbotServiceFactory.create', return_value=mock_service), \
             patch('uuid.uuid4', return_value=MagicMock(hex='generated-uuid')):
            
            request = self.factory.post(
                self.url,
                data=json.dumps(data),
                content_type='application/json'
            )
            response = self.view(request)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            # Verify new session_id was generated
            content = b''.join(response.streaming_content).decode('utf-8')
            self.assertIn('session_id', content)

    def test_post_with_invalid_serializer_data(self):
        """Test chat request with invalid data"""
        data = {
            'invalid_field': 'value'
            # Missing 'message' field
        }

        request = self.factory.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, ERROR_RESPONSE_OBJECT)

    def test_post_with_empty_message(self):
        """Test chat request with empty message"""
        data = {
            'message': ''
        }

        request = self.factory.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_with_chatbot_service_exception(self):
        """Test handling of exception during response generation"""
        data = {
            'message': 'Test message'
        }

        mock_service = Mock()
        mock_service.generate_response_stream.side_effect = Exception('Service error')

        with patch('src.chatbot.views.ChatbotServiceFactory.create', return_value=mock_service):
            request = self.factory.post(
                self.url,
                data=json.dumps(data),
                content_type='application/json'
            )
            response = self.view(request)

            # Should still return streaming response with error
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            content = b''.join(response.streaming_content).decode('utf-8')
            self.assertIn('error', content)

    def test_post_with_factory_creation_exception(self):
        """Test handling of exception during factory creation"""
        data = {
            'message': 'Test message'
        }

        with patch('src.chatbot.views.ChatbotServiceFactory.create', side_effect=Exception('Factory error')):
            request = self.factory.post(
                self.url,
                data=json.dumps(data),
                content_type='application/json'
            )
            response = self.view(request)

            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertIn('error', response.data)
            self.assertFalse(response.data['success'])
            self.assertEqual(response.data['error'], 'Factory error')

    def test_get_or_create_session_id_with_existing_id(self):
        """Test _get_or_create_session_id with existing session_id"""
        existing_session_id = str(uuid.uuid4())
        request = Mock()
        request.data = {'session_id': existing_session_id}

        result = ChatBotView._get_or_create_session_id(request)

        self.assertEqual(result, existing_session_id)

    def test_get_or_create_session_id_without_id(self):
        """Test _get_or_create_session_id generates new UUID"""
        request = Mock()
        request.data = {}

        result = ChatBotView._get_or_create_session_id(request)

        # Verify it's a valid UUID
        try:
            uuid.UUID(result)
            is_valid_uuid = True
        except ValueError:
            is_valid_uuid = False

        self.assertTrue(is_valid_uuid)

    def test_post_streaming_response_chunks(self):
        """Test that streaming response properly yields chunks"""
        data = {
            'message': 'Tell me about diamonds'
        }

        chunks = [
            f'data: {json.dumps({"session_id": "test-id"})}\n\n',
            f'data: {json.dumps({"chunk": "Diamonds "})}\n\n',
            f'data: {json.dumps({"chunk": "are precious"})}\n\n',
        ]

        mock_service = Mock()
        mock_service.generate_response_stream.return_value = iter(chunks)

        with patch('src.chatbot.views.ChatbotServiceFactory.create', return_value=mock_service):
            request = self.factory.post(
                self.url,
                data=json.dumps(data),
                content_type='application/json'
            )
            response = self.view(request)

            streamed_chunks = list(response.streaming_content)
            
            self.assertEqual(len(streamed_chunks), 3)
            
            full_content = b''.join(streamed_chunks).decode('utf-8')
            self.assertIn('session_id', full_content)
            self.assertIn('Diamonds', full_content)
            self.assertIn('are precious', full_content)

    def test_chatbot_service_factory_called_with_correct_params(self):
        """Test that ChatbotServiceFactory is called with correct parameters"""
        session_id = str(uuid.uuid4())
        customer_query = 'Show me rings'
        data = {
            'message': customer_query,
            'session_id': session_id
        }

        mock_service = Mock()
        mock_service.generate_response_stream.return_value = [
            f'data: {json.dumps({"session_id": session_id})}\n\n'
        ]

        with patch('src.chatbot.views.ChatbotServiceFactory.create', return_value=mock_service) as mock_factory:
            request = self.factory.post(
                self.url,
                data=json.dumps(data),
                content_type='application/json'
            )
            response = self.view(request)

            # Verify factory was called with correct arguments
            mock_factory.assert_called_once_with(session_id, customer_query)

    def test_permission_classes(self):
        """Test that view has AllowAny permission"""
        from rest_framework.permissions import AllowAny
        
        view_instance = ChatBotView()
        self.assertEqual(view_instance.permission_classes, [AllowAny])

    def test_post_with_malformed_json(self):
        """Test handling of malformed JSON"""
        request = self.factory.post(
            self.url,
            data='{"message": invalid json}',
            content_type='application/json'
        )
        
        response = self.view(request)
        
        # Should return 400 or 500 depending on where parsing fails
        self.assertIn(response.status_code, [
            status.HTTP_400_BAD_REQUEST,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        ])

    def test_post_with_none_message(self):
        """Test chat request with None as message"""
        data = {
            'message': None
        }

        request = self.factory.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_concurrent_requests_generate_different_session_ids(self):
        """Test that multiple requests without session_id get unique IDs"""
        data = {
            'message': 'Test message'
        }

        session_ids = set()
        
        mock_service = Mock()
        mock_service.generate_response_stream.return_value = [
            f'data: {json.dumps({"session_id": "test"})}\n\n'
        ]

        with patch('src.chatbot.views.ChatbotServiceFactory.create', return_value=mock_service):
            for _ in range(5):
                request = self.factory.post(
                    self.url,
                    data=json.dumps(data),
                    content_type='application/json'
                )
                # Simulate different requests
                request.data = json.loads(json.dumps(data))
                session_id = ChatBotView._get_or_create_session_id(request)
                session_ids.add(session_id)

        # All session IDs should be unique
        self.assertEqual(len(session_ids), 5)