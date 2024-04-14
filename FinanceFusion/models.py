from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='categories')
    is_shared = models.BooleanField(default=False)
    event_date = models.DateField(default=date.today)

    def __str__(self):
        return self.name + ' is shared = ' + str(self.is_shared)

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ('name', 'user')

class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')

    def __str__(self):
        return self.name + ' is $' + str(self.amount)