from django.urls import path, include   
from .views import ProductViewSet, products_page
from rest_framework.routers  import DefaultRouter   
from . import views

app_name = 'store'

router = DefaultRouter()
router.register(r'api/products', ProductViewSet)

urlpatterns = [
    path('products/', products_page, name="products-page" ),
    path('', include(router.urls)),
    path('product/<int:pk>', views.product_details, name="product_details"),


    # ============================================
    # API Endpoints (return JSON)
    # ============================================
    # List all products: GET /api/products/
   
   path('api/products/<int:pk>/', views.ProductViewSet.as_view({'get', 'retriever'}),
        name='api_product_details'
        )
]

# from .views import home
# urlpatterns = [
#     path('', home, name='home')
# ]