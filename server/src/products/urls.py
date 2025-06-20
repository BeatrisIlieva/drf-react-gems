from django.urls import path

from src.products.views.attributtes import StoneRetrieveView
from src.products.views.product import (
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
    path('stones/', StoneRetrieveView.as_view(), name='stone-retrieve')
]
