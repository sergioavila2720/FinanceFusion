from rest_framework import serializers
from .models import *
from members.serializers import UserSerializer


class CategorySearialier(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'user', 'description']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['is_shared'] = False

        category = Category.objects.create(**validated_data)
        return category
    
# I need to add a method to update the category. This method has to validate name, description, user and is_shared = false
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        return instance



class ExpenseSearialier(serializers.ModelSerializer):
    category = CategorySearialier(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'name' ,'description', 'amount', 'is_shared', 'user', 'category', 'category_id']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Expense.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
