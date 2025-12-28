from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import MenuItem
from .serializers import MenuItemSerializer
from users.permissions.role_permissions import IsManager


class MenuListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Managers see all items
        if user.groups.filter(name="MANAGER").exists():
            items = MenuItem.objects.all().order_by("name")
        else:
            # Waiter / Cashier see only active items
            items = MenuItem.objects.filter(is_active=True).order_by("name")

        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateMenuItemView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        serializer = MenuItemSerializer(data=request.data)
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


class ToggleMenuItemStatusView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, item_id):
        try:
            item = MenuItem.objects.get(id=item_id)
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Menu item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.is_active = not item.is_active
        item.save()

        return Response(
            {
                "message": "Menu item status updated",
                "is_active": item.is_active
            },
            status=status.HTTP_200_OK
        )
