from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Product
from .serializer import ProductSerializer
from django.http import JsonResponse


# ============================================
# API Views (for AJAX/JavaScript requests)
# ============================================


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        # IMPORTANT: Pass request context
        return {'request': self.request} 

# create a view to show html.
def home(request):
    return render(request, "store/home.html")



def products_page(request):
    return render(request, "store/products.html")

def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product-details.html', {'product_id': pk})


# def api_product_details(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return JsonResponse({
#         "id": product.id,
#         "name": product.name,
#         "size": product.size,
#         "price": product.price,
#         "description": product.description,
#         "images": product.images,
#       })