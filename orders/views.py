from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cart.models import Cart
from products.models import Product
from .models import Order, OrderItem,Payment
from .serializers import OrderSerializer,PaymentSerializer
from rest_framework import status,serializers

# Create your views here.

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        if not cart.items.exists():
            return Response({'error':'Cart is Empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            order = Order.objects.create(user=request.user)

            for item in cart.items.all():
                product = item.product

                if product.stock < item.quantity:
                    raise serializers.ValidationError({
                        "error": f"{product.name} only {product.stock} in stock"
                    })
                
                OrderItem.objects.create(order=order,product=product,price=product.price,quantity=item.quantity)
                product.stock -=  item.quantity
                product.save()

            cart.items.all().delete()

        return Response({
            "order_id": order.id,
            "total_price": order.total_price,
            "message": "Order placed successfully"
        })

class PaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request,order_id):
        order = Order.objects.get(id=order_id,user=request.user)
        payment = Payment.objects.create(
            order=order,
            amount=order.total_price(),
            status="completed"
        )
        order.status = 'paid'
        order.save()

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)