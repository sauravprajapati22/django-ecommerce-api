from django.urls import path
from .views import AddToCartView,CartView,UpdateCartItemView,RemoveCartItemView

urlpatterns = [
    path("add/",AddToCartView.as_view()),
    path('',CartView.as_view()),
    path("item/<int:pk>/update/", UpdateCartItemView.as_view()),
    path("item/<int:pk>/delete/", RemoveCartItemView.as_view()),
]