from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'phone_number', 'is_staff', 'is_active', 'date_joined')
    list_filter = ( 'is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'username', 'phone_number')
    readonly_fields = ('date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('phone_number', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'password1', 'password2',  'is_staff', 'is_active','profile_photo',)}
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from .models import Category, Product, ProductImage, ProductFeature

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "slug"]

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "get_categories", "price", "stock", "is_active"]
    list_filter = ["categories", "is_active", "created_at"]
    inlines = [ProductImageInline, ProductFeatureInline]
    filter_horizontal = ('categories',)

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

# Register the ProductFeature model if you want to manage it separately
admin.site.register(ProductFeature)

from django.contrib import admin
from .models import Order, OrderItem
from django.db.models import Sum


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity', 'subtotal']  # Remove 'price' from fields
    readonly_fields = ['subtotal']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        return list(readonly_fields) + ['subtotal']

    def save_model(self, request, obj, form, change):
        obj.subtotal = obj.price * obj.quantity
        obj.save()



class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'view_order_items', 'total_price', 'updated_at']
    search_fields = ['user__email', 'status']
    list_filter = ['status', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    def view_order_items(self, obj):
        # Display product names and quantities in a comma-separated string
        return ", ".join([f"{item.product.name} x {item.quantity}" for item in obj.items.all()])
    view_order_items.short_description = "Order Items"

    def save_model(self, request, obj, form, change):
        obj.save()
        total_price = sum(item.subtotal for item in obj.items.all())
        obj.total_price = total_price
        obj.save()



admin.site.register(Order, OrderAdmin)
