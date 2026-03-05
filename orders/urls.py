from django.urls import path
from .views import CheckoutView,PaymentView

urlpatterns = [
    path("checkout/", CheckoutView.as_view()),
     path("payment/<int:order_id>/", PaymentView.as_view()),
]