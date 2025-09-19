from django.urls import path

from .views import ChatBotAPIView

app_name = 'chatbot'

urlpatterns = [
    path('chat/', ChatBotAPIView.as_view(), name='chatbot-chat'),
]
