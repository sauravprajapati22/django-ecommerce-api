from django.contrib import admin
from .models import Category,Product

# Register your models here.
@admin.register(Category)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','slug')
    search_fields = ('name',)

@admin.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','vendor','price','stock','is_available')
    list_filter = ('is_available','category')
    search_fields = ('name',)