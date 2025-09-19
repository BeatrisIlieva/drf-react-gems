from django.urls import path

from src.chatbot.views import AsyncChatBotView
# from .views import ChatBotAPIView

app_name = 'chatbot'

urlpatterns = [
    path('chat/', AsyncChatBotView.as_view(), name='chatbot-chat'),
    # path('chat/', ChatBotAPIView.as_view(), name='chatbot-chat'),
]

