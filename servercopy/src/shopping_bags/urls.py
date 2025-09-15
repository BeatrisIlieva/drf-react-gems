from rest_framework.routers import DefaultRouter
from src.shopping_bags.views import ShoppingBagViewSet


router = DefaultRouter()
router.register(r'', ShoppingBagViewSet, basename='shopping-bag')

urlpatterns = router.urls
