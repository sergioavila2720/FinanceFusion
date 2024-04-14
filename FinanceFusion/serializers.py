from rest_framework import serializers
from .models import *
from members.serializers import UserSerializer


class CategorySearialier(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Category
        fields = '__all__'


class ExpenseSearialier(serializers.ModelSerializer):
    category = CategorySearialier()
    user = User
    class Meta:
        model = Expense
        fields = '__all__'