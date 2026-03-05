from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User

    list_display=('id','username','email','is_vendor','is_staff')
    list_filter = ('is_vendor','is_staff','is_superuser')
    search_fields = ('username','email')
    ordering = ('id',)

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("is_vendor",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("is_vendor",)}),
    )


admin.site.register(User, CustomUserAdmin)