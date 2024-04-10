from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_shared = models.BooleanField(default=False)
    event_date = models.DateField(default=date.today)

    def __str__(self):
        return self.name + ' is shared = ' + str(self.is_shared)

    class Meta:
        verbose_name_plural = 'Categories'

class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' is $' + str(self.amount)