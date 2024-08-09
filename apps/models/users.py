from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices, CharField, ImageField, EmailField, ManyToManyField, TextField


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'
        CUSTOMER = 'customer', 'Customer'
        AUTHOR = 'author', 'Author'
    address = TextField(blank=True, null=True)
    phone = CharField(max_length=20, blank=True, null=True)
    photo = ImageField(upload_to='customers/%Y/%m/%d/', default='customers/default.png', blank=True)
    backgroun_image = ImageField(upload_to='customers_bgi/%Y/%m/%d/', default='customers/images.jpeg', blank=True)
    billing_address = CharField(max_length=255, null=True, blank=True)
    profession = CharField(max_length=255, blank=True, null=True)
    type = CharField(max_length=20, choices=Type.choices, default=Type.CUSTOMER)
    email = EmailField(unique=True)
    carts = ManyToManyField('apps.Product', through='apps.Cart')
    intro = TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'
        unique_together = [
            ('email', 'is_active')
        ]