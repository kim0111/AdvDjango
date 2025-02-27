from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
# UserRegistrationSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def valid_permission(self):
        if self.request.method == "GET":
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# class UserRegistrationView(APIView):
#     permission_classes = [permissions.AllowAny]  # Allow anyone to register
#
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             user.set_password(serializer.validated_data['password'])  # Hash the password
#             user.save()
#             return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
