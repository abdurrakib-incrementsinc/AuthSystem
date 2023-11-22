from django.contrib import admin
from .models import Restaurant, Branch, Table, Floor
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Branch)
admin.site.register(Table)
admin.site.register(Floor)
