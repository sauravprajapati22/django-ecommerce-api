from rest_framework import serializers
from .models import Product,Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug']

class ProductSerializer(serializers.ModelSerializer):
    vendor = serializers.StringRelatedField(read_only = True)
    category = CategorySerializer(read_only = True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),source = 'category', write_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id','name','description','price','stock','is_available','vendor','category','category_id','created_at'
        ]
        read_only_fields = ['id','vendor','created_at']