from django.urls import path
from products.views.general_views import MeasureUnitListAPIView, IndicatorListAPIView, CategoryProductListAPIView
from products.views.product_viewsets import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView
urlpatterns = [
    path('measure_unit/', MeasureUnitListAPIView.as_view(), name='measure_unit'),
    path('indicator/', IndicatorListAPIView.as_view(), name='indicator'),
    path('category_product/', CategoryProductListAPIView.as_view(),
         name='category_product'),

]
