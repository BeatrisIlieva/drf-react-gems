from django.urls import path

from .views import ChatBotView

app_name = 'chatbot'

urlpatterns = [
    path('chat/', ChatBotView.as_view(), name='chatbot-chat'),
]
