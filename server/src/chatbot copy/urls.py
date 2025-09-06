from django.urls import path
from .views import ChatBotAPIView

app_name = 'chatbot'

urlpatterns = [
    # Main chatbot endpoint
    path('chat/', ChatBotAPIView.as_view(), name='chatbot-chat'),
]

