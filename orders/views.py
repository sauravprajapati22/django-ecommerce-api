from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cart.models import Cart
from products.models import Product
from .models import Order, OrderItem,Payment
from .serializers import OrderSerializer,PaymentSerializer

# Create your views here.

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        cart = Cart.objects.get(user = request.user)

        if not cart.items.exists():
            return Response({'error':'Cart is Empty'})
        
        with transaction.atomic():
            order = Order.objects.create(user=request.user)

            for item in cart.items.all():
                product = item.product

                if product.stock < item.quantity:
                    return Response({
                        "error":f'{product.name} Out of stock'})
                
                OrderItem.objects.create(order=order,product=product,price=product.price,quantity=item.quantity)
                product.stock -=  item.quantity
                product.save()

            cart.items.all().delete()

        serializer = OrderSerializer(order)

        return Response(serializer.data) 

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