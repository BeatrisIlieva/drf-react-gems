from django.urls import path
from src.products.views import (
    EarwearListView,
    FingerwearListView,
    NeckwearListView,
    WristwearListView,
    EarwearItemView,
    FingerwearItemView,
    NeckwearItemView,
    WristwearItemView,
)

urlpatterns = [
    path('earwears/', EarwearListView.as_view(), name='earwear-list'),
    path('fingerwears/', FingerwearListView.as_view(), name='fingerwear-list'),
    path('neckwears/', NeckwearListView.as_view(), name='neckwear-list'),
    path('wristwears/', WristwearListView.as_view(), name='wristwear-list'),
    path('earwears/<int:pk>', EarwearItemView.as_view(), name='earwear-item'),
    path('fingerwears/<int:pk>', FingerwearItemView.as_view(),
         name='fingerwear-item'),
    path('neckwears/<int:pk>', NeckwearItemView.as_view(), name='neckwear-item'),
    path('wristwears/<int:pk>', WristwearItemView.as_view(), name='wristwear-item'),
]
