from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials"}, status=400)

        login(request, user)

        return Response({
            "message": "Login successful",
            "role": user.groups.first().name if user.groups.exists() else None
        })


class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})


class RegisterView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role")

        if not username or not password or not role:
            return Response({"error": "All fields required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        if role not in ["Waiter", "Cashier", "Manager"]:
            return Response({"error": "Invalid role"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        group = Group.objects.get(name=role)
        user.groups.add(group)

        login(request, user)

        return Response({
            "message": "User registered and logged in",
            "role": role
        })
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "role": request.user.groups.first().name
        })
