import string

from django.core.validators import FileExtensionValidator
from django.db.models import Model, CharField, DateTimeField, JSONField, CASCADE, ForeignKey, ImageField, BooleanField, \
    ManyToManyField, PositiveIntegerField, IntegerField, \
    SmallIntegerField, TextField, SlugField
from django.db.models import Q, CheckConstraint
from django.db.models.functions import Now
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    name = CharField(max_length=50, unique=True)
    slug = SlugField(editable=False)
    parent = TreeForeignKey('self', CASCADE, null=True, blank=True, related_name='children')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        while self.__class__.objects.filter(slug=self.slug).exists():
            letters = string.ascii_lowercase
            self.slug += f"{len(Category.objects.all())}"  # 2 - logic
        super().save(force_insert, force_update, using, update_fields)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255)
    author = ForeignKey('apps.User', CASCADE)
    price = IntegerField(verbose_name='Price', help_text="Price of product in $")
    shipping_cost = IntegerField(verbose_name='Shipping cost', default=50, help_text="Pay for delivery $")
    discount = IntegerField(verbose_name='Discount', default=0, help_text="discount in % ")
    stock = BooleanField(verbose_name="Is exists", default=False)
    quantity = IntegerField(verbose_name='Amount', default=0)
    properties = JSONField(verbose_name='Properties', blank=True, default=dict)
    description = CKEditor5Field(verbose_name='Description', null=True, blank=True)
    category = ForeignKey('apps.Category', on_delete=CASCADE)
    tags = ManyToManyField('apps.Tag', blank=True)
    updated_at = DateTimeField(verbose_name='Updated at', auto_now_add=True, db_default=Now())
    created_at = DateTimeField(verbose_name='Created at', auto_now=True, db_default=Now())

    @property
    def current_price(self):
        return self.price - (self.price * self.discount) // 100

    class Meta:
        db_table = 'product'


class ProductImage(Model):
    photo = ImageField(upload_to='products/%Y/%m/%d/',
                       validators=[FileExtensionValidator(['png', 'jpeg', 'jpg', 'webp'])])
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
    updated_at = DateTimeField(auto_now_add=True, db_default=Now())
    created_at = DateTimeField(auto_now=True, db_default=Now())

    def delete(self, using=None, keep_parents=False):
        self.photo.delete(False)
        return super().delete(using, keep_parents)

    class Meta:
        db_table = 'productimage'


class Tag(Model):
    name = CharField(max_length=255)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return self.name


class Review(Model):
    review_text = TextField(null=True, blank=True)
    review_title = CharField(max_length=255, null=True, blank=True)
    product = ForeignKey('apps.Product', on_delete=CASCADE)
    author = ForeignKey('apps.User', on_delete=CASCADE)
    rating = SmallIntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            CheckConstraint(check=Q(rating__gte=0) & Q(rating__lte=10), name="rating_between_0_and_10"),
        ]

        db_table = 'review'


class Order(Model):
    user = ForeignKey('apps.User', on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order'


class Cart(Model):
    user = ForeignKey('apps.User', on_delete=CASCADE)
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='product_id')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'


class OrderItem(Model):
    order = ForeignKey('apps.Order', on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1, db_default=1)

    class Meta:
        db_table = 'orderitem'


class Region(Model):
    name = CharField(max_length=255)

    class Meta:
        db_table = 'region'


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', CASCADE)

    class Meta:
        db_table = 'district'


class Country(Model):
    name = CharField(max_length=255)
    code = CharField(max_length=5)

    class Meta:
        db_table = 'country'