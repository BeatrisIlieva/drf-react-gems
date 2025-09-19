







# constants.py - Constants
ERROR_RESPONSE_OBJECT = {
    "error": "Invalid request format",
    "success": False
}


# config.py - Configuration
# LLM Configuration
LLM_MODEL = "gpt-4"
MAX_TOKENS = 2000
TEMPERATURE = 0.7
TOP_P = 0.9
FREQUENCY_PENALTY = 0.1
PRESENCE_PENALTY = 0.1

# Embedding Configuration
EMBEDDING_MODEL = "text-embedding-3-small"
DIMENSIONS = 1536

# Vector Store Configuration
PINECONE_INDEX_NAME = "drf-react-gems-index"


# models.py - Pydantic Models (example structure)
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class CustomerIntentEnum(str, Enum):
    JEWELRY_CONSULTATION = "JEWELRY_CONSULTATION"
    SIZING_HELP = "SIZING_HELP"
    CARE_INSTRUCTIONS = "CARE_INSTRUCTIONS"
    PRICING = "PRICING"
    RETURN_POLICY = "RETURN_POLICY"
    SHIPPING_INFORMATION = "SHIPPING_INFORMATION"
    ORDER_PLACING = "ORDER_PLACING"
    BRAND_INFORMATION = "BRAND_INFORMATION"
    CONCERN_OR_HESITATION = "CONCERN_OR_HESITATION"
    OFF_TOPIC = "OFF_TOPIC"


class CustomerIntent(BaseModel):
    primary_intent: CustomerIntentEnum
    confidence: Optional[float] = None


class PurchaseType(BaseModel):
    purchase_type: str


class WearerGender(BaseModel):
    gender: str


class CategoryType(BaseModel):
    category: str


class MetalType(BaseModel):
    metal_type: str


class StoneType(BaseModel):
    stone_type: str


# urls.py - URL Configuration
from django.urls import path
from src.chatbot.views import AsyncChatBotView

urlpatterns = [
    path('api/chatbot/', AsyncChatBotView.as_view(), name='async_chatbot'),
]


# requirements.txt additions for async support
"""
# Add these to your requirements.txt for async support:

# Django async support
django>=4.1
asgiref>=3.6.0

# ASGI server for production
uvicorn[standard]>=0.20.0
# or
daphne>=4.0.0

# Existing dependencies
langchain>=0.1.0
langchain-openai>=0.1.0
langchain-pinecone>=0.1.0
langgraph>=0.1.0
pinecone-client>=3.0.0
djangorestframework>=3.14.0
pydantic>=2.0.0
"""


# settings.py additions for async support
"""
# Add to your Django settings.py:

# Enable async views
ASGI_APPLICATION = 'your_project.asgi.application'

# Optional: Configure async database support (if needed)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',  # or other async-compatible backend
#         'NAME': 'your_db_name',
#         'USER': 'your_db_user',
#         'PASSWORD': 'your_db_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'OPTIONS': {
#             'OPTIONS': '-c default_transaction_isolation=serializable'
#         }
#     }
# }
"""


# asgi.py - ASGI Configuration
"""
# Create or update your asgi.py file:

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Add websocket support if needed later
})
"""


# Example usage and testing
"""
# To test the async chatbot:

# 1. Start the server with uvicorn:
#    uvicorn your_project.asgi:application --reload --port 8000

# 2. Send POST request to /api/chatbot/ with JSON body:
{
    "message": "I'm looking for a diamond ring",
    "session_id": "optional-session-id"
}

# 3. The response will be streamed as Server-Sent Events:
data: {"response": "I'd be happy to help you find the perfect diamond ring!", "type": "jewelry_consultation"}

# 4. For JavaScript frontend integration:
const eventSource = new EventSource('/api/chatbot/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: 'Looking for earrings',
        session_id: 'session123'
    })
});

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Response:', data.response);
};
"""