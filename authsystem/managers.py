from django.db.models import Manager, QuerySet, Q
from django.db import models


# soft deletes
class AppQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class AppManager(Manager):
    def get_queryset(self):
        return AppQuerySet(self.model, using=self._db).exclude(is_deleted=True)


class Product(models.Model):
    # model fields and other methods ...
    objects = AppManager

