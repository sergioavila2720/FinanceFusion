from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Expense, Category
from .serializers import ExpenseSearialier, CategorySearialier
from rest_framework.permissions import IsAuthenticated



class ExpenseCRUDAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request, id=None):
        if id:
            try:
                expense = Expense.objects.get(pk=id)
            except Expense.DoesNotExist:
                return Response({"message": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)
            
            if expense.user != request.user:
                return Response({"message": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = ExpenseSearialier(expense)
            return Response(serializer.data)
            
        else:
            expenses = Expense.objects.filter(user=request.user)
            if not expenses.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ExpenseSearialier(expenses, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = ExpenseSearialier(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            expense = Expense.objects.get(pk=pk, user=request.user)
        except Expense.DoesNotExist:
            return Response({"message": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseSearialier(expense, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            expense = Expense.objects.get(pk=pk, user=request.user)
        except Expense.DoesNotExist:
            return Response({"message": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseSearialier(expense, data=request.data, partial=True, context={'request': request})  # Notice partial=True
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            expense = Expense.objects.get(pk=pk, user=request.user)
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Expense.DoesNotExist:
            return Response({"message": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)
        

class ExpenseSumAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        category_id = request.query_params.get('category_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        expenses = Expense.objects.filter(user=request.user)
        
        if category_id:
            expenses = expenses.filter(category_id=category_id)
        
        if start_date and end_date:
            expenses = expenses.filter(date__range=[start_date, end_date])
        
        total = 0
        for expense in expenses:
            total += expense.amount
        
        return Response({"total": total})
    

class CategoryCRUDAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request, id=None):
        if id:
            try:
                category = Category.objects.get(pk=id)
            except Category.DoesNotExist:
                return Response({"message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
            
            if category.user != request.user:
                return Response({"message": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer = CategorySearialier(category)
            return Response(serializer.data)
            
        else:
            shared_categories = Category.objects.filter(is_shared=True)
            user_categories = Category.objects.filter(user=request.user)
            
            categories = shared_categories | user_categories #what is this?

            
            if not categories.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = CategorySearialier(categories, many=True)

            return Response(serializer.data)

        return Response({"total": total})

    def post(self, request):
        serializer = CategorySearialier(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk, user=request.user)
        except Category.DoesNotExist:
            return Response({"message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySearialier(category, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            category = Category.objects.get(pk=pk, user=request.user)
        except Category.DoesNotExist:
            return Response({"message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySearialier(category, data=request.data, partial=True, context={'request': request})  # Notice partial=True
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk, user=request.user)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"message": "Category not found."}, status=status)
    