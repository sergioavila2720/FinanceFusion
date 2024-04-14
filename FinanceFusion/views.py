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




