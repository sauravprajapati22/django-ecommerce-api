from django.shortcuts import render
from .serializers import CartSerializer,CartItemSerializer
from .models import Cart,CartItem
from rest_framework.generics import UpdateAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Product
from rest_framework.views import APIView
# Create your views here.

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity',1))
        product = Product.objects.get(id = product_id)
        cart, created = Cart.objects.get_or_create(user = request.user)
        cart_item ,created = CartItem.objects.get_or_create(cart=cart , product=product)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        serializer = CartSerializer(cart)

        return Response(serializer.data)

class CartView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart, created = Cart.objects.get_or_create(user=request.user)

        serializer = CartSerializer(cart)

        return Response(serializer.data)

class UpdateCartItemView(UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_class = [IsAuthenticated]

    def perform_update(self,serializer):
        serializer.save()  

class RemoveCartItemView(DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]

