from django.contrib import admin
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ("id", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username",)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ("id", "order", "product", "price", "quantity")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = ("id", "order", "amount", "status", "created_at")
    list_filter = ("status",)   