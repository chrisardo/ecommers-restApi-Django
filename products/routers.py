from rest_framework.routers import DefaultRouter
from .views.product_viewsets import ProductViewSet
from .views.general_views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'measure-units', MeasureUnitViewSet, basename='measure-units')
router.register(r'indicators', IndicatorViewSet, basename='indicators')
router.register(r'category-products', CategoryProductViewSet, basename='category-products')
urlpatterns = router.urls