from django.contrib import admin
from .models import  Product , CustomUser , ProductImages
# Register your models here.

class ProductImagesInline(admin.StackedInline):
    model = ProductImages
    extra = 3
    max_num = 10

admin.site.register(CustomUser)


class ProductImagesInline(admin.StackedInline):
    model = ProductImages
    extra = 3
    max_num = 10
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'size']
    list_filter = ['brand', 'size']
    search_fields = ['name', 'description']
    inlines = [ProductImagesInline]
admin.site.register(ProductImages)