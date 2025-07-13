from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.products.views.product import (
    CollectionRetrieveView,
    ColorRetrieveView,
    MetalRetrieveView,
    StoneRetrieveView,
    # Async views for improved performance
    AsyncCollectionRetrieveView,
    AsyncColorRetrieveView,
    AsyncMetalRetrieveView,
    AsyncStoneRetrieveView
)
from src.products.views.product import (
    EarwearItemView,
    EarwearListView,
    FingerwearItemView,
    FingerwearListView,
    NeckwearItemView,
    NeckwearListView,
    WristwearItemView,
    WristwearListView
)
from src.products.views.review import ReviewViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path(
        '', include(router.urls)
    ),
    path(
        'earwears/', include([
            path('', EarwearListView.as_view(), name='earwear-list'),
            path('<int:pk>/', EarwearItemView.as_view(), name='earwear-item'),
        ])
    ),
    path(
        'fingerwears/', include([
            path('', FingerwearListView.as_view(), name='fingerwear-list'),
            path('<int:pk>/',
                 FingerwearItemView.as_view(), name='fingerwear-item'),
        ])
    ),
    path(
        'neckwears/', include([
            path('', NeckwearListView.as_view(), name='neckwear-list'),
            path('<int:pk>/', NeckwearItemView.as_view(), name='neckwear-item'),
        ])
    ),
    path(
        'wristwears/', include([
            path('', WristwearListView.as_view(), name='wristwear-list'),
            path('<int:pk>/',
                 WristwearItemView.as_view(), name='wristwear-item'),
        ])
    ),
    # Synchronous attribute views (existing)
    path(
        'stones/', StoneRetrieveView.as_view(), name='stone-retrieve'
    ),
    path(
        'colors/', ColorRetrieveView.as_view(), name='color-retrieve'
    ),
    path(
        'collections/', CollectionRetrieveView.as_view(), name='collection-retrieve'
    ),
    path(
        'metals/', MetalRetrieveView.as_view(), name='metal-retrieve'
    ),
    # Asynchronous attribute views for improved performance
    path(
        'stones/async/', AsyncStoneRetrieveView.as_view(), name='stone-retrieve-async'
    ),
    path(
        'colors/async/', AsyncColorRetrieveView.as_view(), name='color-retrieve-async'
    ),
    path(
        'collections/async/', AsyncCollectionRetrieveView.as_view(), name='collection-retrieve-async'
    ),
    path(
        'metals/async/', AsyncMetalRetrieveView.as_view(), name='metal-retrieve-async'
    ),
]
