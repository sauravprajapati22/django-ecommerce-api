from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = (
            ('pending' , 'Pending'),
            ('paid' , 'Paid'),
            ('shipped' , 'Shipped'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="orders")
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"

    def total_price(self):
        return sum(
            item.price * item.quantity
            for item in self.items.all()
        )
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE ,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} X {self.quantity}"
    
class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending' , 'Pending'),
        ('completed' , 'Completed'),
        ('failed' , 'Failed'),
    )

    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='payment')
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"

