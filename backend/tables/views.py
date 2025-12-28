from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Table
from .serializers import TableSerializer
from users.permissions.role_permissions import IsManager


class TableListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tables = Table.objects.all().order_by("number")
        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTableView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = TableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UpdateTableStatusView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, table_id):
        try:
            table = Table.objects.get(id=table_id)
        except Table.DoesNotExist:
            return Response(
                {"error": "Table not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        is_available = request.data.get("is_available")
        if is_available is None:
            return Response(
                {"error": "is_available field required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        table.is_available = bool(is_available)
        table.save()

        return Response(
            {
                "message": "Table status updated",
                "is_available": table.is_available
            },
            status=status.HTTP_200_OK
        )
