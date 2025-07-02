from rest_framework.routers import DefaultRouter
from src.wishlist.views import WishlistViewSet

router = DefaultRouter()
router.register(r'', WishlistViewSet, basename='wishlist')

urlpatterns = router.urls
