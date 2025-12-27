from rest_framework import serializers
from .models import Product, ProductImages



class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImages
        fields =['id', 'image_url']


    def get_image_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id',
            'name',
            'size',
            'price',
            'description',
            'images',
            ]






# # If using DRF serializer
# class ProductSerializer(serializers.ModelSerializer):
#     image_url = serializers.SerializerMethodField()
    
#     def get_image_url(self, obj):
#         first_image = obj.images.first()
#         if first_image:
#             return self.context['request'].build_absolute_uri(first_image.image.url)
#         return None