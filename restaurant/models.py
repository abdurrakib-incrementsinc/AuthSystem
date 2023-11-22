from django.contrib.sites.models import Site
from django.db import models
from authsystem.models import BaseModel
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from utils.helper import unique_slugify, image_compress, qr_code_generate
from django.core.files import File
User = get_user_model()
# Create your models here.

PAYMENT_TYPE = [
    ('PAY_FIRST', 'Pay First'),
    ('PAY_LATER', 'Pay Later')
]


class Restaurant(BaseModel):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="restaurant_owner")
    name = models.CharField(_("Restaurant Name"), max_length=150)
    slug = models.SlugField(unique=True, null=True)
    logo = models.ImageField(upload_to='restaurant_logos', null=True, blank=True)
    address = models.CharField(_("Address"), max_length=350)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(_("Phone Number"), max_length=15)
    payment_type = models.CharField(_("Payment Type"), choices=PAYMENT_TYPE)
    bin_number = models.CharField(_("Bin Number"), max_length=40)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.name)
        self.logo = image_compress(self.logo, 90)
        super().save(*args, **kwargs)


class Branch(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_branch')
    name = models.CharField(_('Branch Name'), max_length=250)
    slug = models.SlugField(unique=True, null=True)
    manager = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='branch_manager', null=True, blank=True)
    address = models.CharField(max_length=355, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    qr_image = models.ImageField(upload_to='branch_qr_image', null=True, blank=True)
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.restaurant.name}-{self.name}"

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, f"{self.restaurant.name}{self.name}")
        current_site = Site.objects.get_current()
        # url = f"http://{current_site.domain}/api/customer/my-menu/{instance.restaurant.slug}/{instance.slug}/"
        url = f"http://{current_site.domain}/mobile-menu/{self.slug}"
        # qr = qr_generate(url, logo_link=self.restaurant.logo)
        if logo := self.restaurant.logo:
            qr = qr_code_generate(url, logo_link=logo)
        else:
            qr = qr_code_generate(url)
        self.qr_image = File(qr, name=f"branch{self.id}.png")
        # self.qr_image = image_compress(self.qr_image, 90)
        super().save(*args, **kwargs)

    class Meta:
        ordering = (
            "-id",
            "restaurant",
        )
        verbose_name_plural = 'branches'


class Floor(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_floor')
    name = models.CharField(_('Floor Name'), max_length=150)
    description = models.CharField(max_length=400, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return f"{self.branch.name}-{self.name}"

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-id', 'branch')

    def total_capacity(self):
        chair = self.floor_table.all().aggregate(table=models.Sum('no_of_chairs'))['table']
        return 0 if chair is None else chair

    def total_table(self):
        return self.floor_table.count()


class Table(BaseModel):
    TABLE_STATUS = [
        ('AVAILABLE', 'Available'),
        ('RESERVED', 'Reserved'),
        ('OCCUPIED', 'Occupied'),
    ]
    TABLE_TYPE = [
        ('RECTANGLE', 'Rectangle'),
        ('CIRCLE', 'Circle'),
    ]
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='floor_table')
    name = models.CharField(_("Floor Name"), max_length=200)
    table_type = models.CharField(max_length=200, choices=TABLE_TYPE, null=True, blank=True)
    status = models.CharField(max_length=120, choices=TABLE_STATUS, null=True, blank=True)
    no_of_chairs = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return f"{self.floor.branch.name}-{self.floor.name}-{self.name}"

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('floor',)


