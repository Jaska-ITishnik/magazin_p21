from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.admin import DraggableMPTTAdmin

from apps.models import User, AdminUser, ModeratorUser, CustomerUser
from apps.models.products import ProductImage, Product, Category, Order, Cart, OrderItem, District, Country, Tag
from apps.models.proxies import AuthorUser


class ProductStackedInline(admin.StackedInline):
    model = ProductImage
    min_num = 0
    max_num = 5
    extra = 0


class ProductBaseModelAdmin(ModelAdmin):
    list_display_links = 'id', 'name'
    autocomplete_fields = 'category',
    inlines = [ProductStackedInline]

    @admin.display(description='photo')
    def photo(self, obj: Product):
        img_url = obj.images.last()
        if img_url:
            return mark_safe(f"<img src={img_url.photo.url} alt='img' width='120px' height='80px'")
        else:
            return 'None image'

    @admin.display(description='picture_amount')
    def amount_picture(self, obj: Product):
        amount = obj.images.count()
        return amount


@admin.register(Product)
class ProductModelAdmin(ProductBaseModelAdmin):
    list_display = 'id', 'name', 'quantity', 'category', 'created_at', 'updated_at', 'amount_picture', 'photo'


@admin.register(Category)
class CategoryModelAdmin(DraggableMPTTAdmin):
    search_fields = ['name']


@admin.register(User)
class UserModelAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).all()


@admin.register(AdminUser)
class AdminUserModelAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=AdminUser.Type.ADMIN)


@admin.register(ModeratorUser)
class ModeratorUserModelAdmin(UserAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=ModeratorUser.Type.MODERATOR)


@admin.register(CustomerUser)
class CustomerModelAdmin(UserAdmin):
    list_display = 'id', 'username', 'email', 'first_name', 'last_name', 'photo'
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'phone', 'billing_address', 'photo')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=CustomerUser.Type.CUSTOMER)


@admin.register(AuthorUser)
class AuthorModelAdmin(UserAdmin):
    list_display = 'id', 'first_name', 'last_name', 'email', 'phone', 'photo'
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", 'phone', 'photo')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(type=CustomerUser.Type.AUTHOR)


@admin.register(Order)
class OrderModelAdmin(ModelAdmin):
    list_display = 'id', 'user_id', 'created_at'


@admin.register(Cart)
class CartModelAdmin(ModelAdmin):
    list_display = 'id', 'user_id', 'product_id', 'created_at'


@admin.register(OrderItem)
class OrderItemModelAdmin(ModelAdmin):
    list_display = 'id', 'order_id', 'quantity'


@admin.register(District)
class DistrictModelAdmin(ModelAdmin):
    list_display = 'id', 'region_id', 'name'


@admin.register(Country)
class DistrictModelAdmin(ModelAdmin):
    list_display = 'id', 'name', 'code'


@admin.register(Tag)
class TagModelAdmin(ModelAdmin):
    list_display = 'id', 'name'
    list_display_links = 'name',
