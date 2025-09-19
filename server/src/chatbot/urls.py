from django.urls import path

from src.chatbot.views import chatbot_view
# from .views import ChatBotAPIView

app_name = 'chatbot'

urlpatterns = [
    path('chat/', chatbot_view, name='chatbot-chat'),
    # path('chat/', ChatBotAPIView.as_view(), name='chatbot-chat'),
]

