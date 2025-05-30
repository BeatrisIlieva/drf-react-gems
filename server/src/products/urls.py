from django.urls import path

from src.products.views.type_list import (
    EarwearListView,
    FingerwearListView,
    NeckwearListView,
    WristwearListView
)


urlpatterns = [
    path('earwears/', EarwearListView.as_view(), name='earwear-list'),
    path('fingerwears/', FingerwearListView.as_view(), name='fingerwear-list'),
    path('neckwears/', NeckwearListView.as_view(), name='neckwear-list'),
    path('wristwears/', WristwearListView.as_view(), name='wristwear-list'),
]
