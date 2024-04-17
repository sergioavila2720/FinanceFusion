from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Expense
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
        
        


    





