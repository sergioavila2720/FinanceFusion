from rest_framework import serializers
from .models import *
from common.serializers import UserSearialier


class CategorySearialier(serializers.ModelSerializer):
    user = UserSearialier()
    class Meta:
        model = Category
        fields = '__all__'


class ExpenseSearialier(serializers.ModelSerializer):
    category = CategorySearialier()
    user = User
    class Meta:
        model = Expense
        fields = '__all__'