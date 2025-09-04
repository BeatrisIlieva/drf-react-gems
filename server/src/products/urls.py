from django.urls import path, include
from rest_framework.routers import DefaultRouter

from src.products.views.product import (
    BraceletItemView,
    BraceletListView,
    CollectionRetrieveView,
    ColorRetrieveView,
    DropEarringItemView,
    DropEarringListView,
    MetalRetrieveView,
    NecklaceItemView,
    NecklaceListView,
    PendantItemView,
    PendantListView,
    RingItemView,
    RingListView,
    StoneRetrieveView,
    StudEarringItemView,
    StudEarringListView,
    WatchItemView,
    WatchListView,
    catalog_page,
    download_catalog,
    generate_catalog,
)
from src.products.views.product import (

    ProductAllReviewsView,
)
from src.products.views.review import ReviewViewSet

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('', include(router.urls)),
    path(
        'drop-earrings/',
        include(
            [
                path('', DropEarringListView.as_view(),
                     name='drop-earrings-list'),
                path(
                    '<int:pk>/', DropEarringItemView.as_view(), name='drop-earrings-item'
                ),
            ]
        ),
    ),
    path(
        'stud-earrings/',
        include(
            [
                path('', StudEarringListView.as_view(),
                     name='stud-earrings-list'),
                path(
                    '<int:pk>/', StudEarringItemView.as_view(), name='stud-earrings-item'
                ),
            ]
        ),
    ),
    path(
        'necklaces/',
        include(
            [
                path('', NecklaceListView.as_view(),
                     name='necklaces-list'),
                path(
                    '<int:pk>/', NecklaceItemView.as_view(), name='necklaces-item'
                ),
            ]
        ),
    ),
    path(
        'pendants/',
        include(
            [
                path('', PendantListView.as_view(),
                     name='pendants-list'),
                path(
                    '<int:pk>/', PendantItemView.as_view(), name='pendants-item'
                ),
            ]
        ),
    ),
    path(
        'bracelets/',
        include(
            [
                path('', BraceletListView.as_view(), name='bracelet-list'),
                path(
                    '<int:pk>/',
                    BraceletItemView.as_view(),
                    name='bracelet-item',
                ),
            ]
        ),
    ),
    path(
        'watches/',
        include(
            [
                path('', WatchListView.as_view(), name='watch-list'),
                path(
                    '<int:pk>/',
                    WatchItemView.as_view(),
                    name='watch-item',
                ),
            ]
        ),
    ),
    path(
        'rings/',
        include(
            [
                path('', RingListView.as_view(), name='ring-list'),
                path(
                    '<int:pk>/',
                    RingItemView.as_view(),
                    name='ring-item',
                ),
            ]
        ),
    ),
    path('stones/', StoneRetrieveView.as_view(), name='stone-retrieve'),
    path('colors/', ColorRetrieveView.as_view(), name='color-retrieve'),
    path(
        'collections/',
        CollectionRetrieveView.as_view(),
        name='collection-retrieve',
    ),
    path('metals/', MetalRetrieveView.as_view(), name='metal-retrieve'),
    path(
        '<str:category>/<int:pk>/all-reviews/',
        ProductAllReviewsView.as_view(),
        name='product-all-reviews',
    ),
    path('catalog/', catalog_page, name='catalog_page'),
    path('catalog/generate/', generate_catalog, name='generate_catalog'),
    path('download-catalog/', download_catalog, name='download_catalog'),
]
