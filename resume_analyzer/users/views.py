import base64

from djoser.views import UserViewSet
from rest_framework import generics, status, permissions
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.test import APIRequestFactory
from analytics.utils import log_event

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        log_event('REGISTER', f'New user registered: {user.email}', user=user)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        log_event('LOGIN', f'User logged in: {user.email}', user=user)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


@api_view(['GET'])
def activate_account(request, uid, token):
    try:
        decoded_uid = base64.urlsafe_b64decode(uid + '==').decode()
        print(f"🔍 Decoded UID: {decoded_uid}")
    except Exception as e:
        return Response({"detail": f"Invalid UID encoding: {e}"}, status=status.HTTP_400_BAD_REQUEST)

    factory = APIRequestFactory()
    post_request = factory.post("/auth/users/activation/", {"uid": uid, "token": token})
    view = UserViewSet.as_view({'post': 'activation'})
    response = view(post_request)
    if response.status_code == 204:
        return Response({"detail": "✅ Account activated successfully!"})
    return Response({"detail": "❌ Activation failed", "info": response.data}, status=response.status_code)
