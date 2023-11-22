from django.db import models
from restaurant.models import Restaurant
from django.contrib.auth import get_user_model
from authsystem.models import BaseModel
from utils.helper import unique_slugify
User = get_user_model()
# Create your models here.

STATUS = [
    ("AVAILABLE", "Available"),
    ("NOT_AVAILABLE", "Not Available"),
]


class Category(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_category')
    name = models.CharField(max_length=123)
    slug = models.SlugField(unique=True, null=True)
    icon = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-id', 'name')


class Item(BaseModel):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items_user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_items')
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, null=True)
    description = models.CharField(max_length=350, null=True, blank=True)
    price = models.FloatField(default=0.0)
    status = models.CharField(max_length=60, choices=STATUS, default='AVAILABLE', blank=True, null=True)
    video_url = models.CharField(max_length=250, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='item_thumbnail', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    @property
    def item_variants(self):
        return self.item_variants().exists()


class Variant(BaseModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_variants')
    title = models.CharField(max_length=130)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.title


