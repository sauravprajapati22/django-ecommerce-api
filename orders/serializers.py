from rest_framework import serializers
from .models import Order,OrderItem,Payment

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source = "product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id','product','product_name','price','quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id","status","created_at","items"]

        def get_total_price(self,obj):
            return obj.total_price
        
class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ["id","order","amount","status","created_at"]
        read_only_fields = ["status"]