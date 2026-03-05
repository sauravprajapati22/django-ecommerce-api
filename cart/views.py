from django.shortcuts import render
from .serializers import CartSerializer,CartItemSerializer
from .models import Cart,CartItem
from rest_framework.generics import UpdateAPIView,DestroyAPIView,RetrieveAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Product
from rest_framework.views import APIView
# Create your views here.

class AddToCartView(CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)

        product = serializer.validated_data['product']
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity += serializer.validated_data.get('quantity', 1)
        item.save()

class CartView(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.prefetch_related('items__product').get_or_create(user=self.request.user)
        return cart

class UpdateCartItemView(UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self,serializer):
        serializer.save()  

    def get_queryset(self):
        # sirf apne cart items hi modify kar sakta hai
        return CartItem.objects.filter(cart__user=self.request.user)
    
class RemoveCartItemView(DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)