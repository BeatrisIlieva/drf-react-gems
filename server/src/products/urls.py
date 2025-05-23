from django.urls import path
from src.products.views import (
    EarwearListView,
    FingerwearListView,
    NeckwearListView,
    WristwearListView
)

urlpatterns = [
    path('earwear/', EarwearListView.as_view(), name='earwear-list'),
    path('fingerwear/', FingerwearListView.as_view(), name='fingerwear-list'),
    path('neckwear/', NeckwearListView.as_view(), name='neckwear-list'),
    path('wristwear/', WristwearListView.as_view(), name='wristwear-list'),
]
