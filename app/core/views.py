"""View for the core API"""
from rest_framework import (
    generics,
    authentication,
    permissions,status
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response

from core.serializers import (
    AuthTokenSerializer,
    UserSerializer, PINSerializer,
    PINGenerateRequestSerializer
)
from core import models
from core.utils import generate_unique_pin
from drf_spectacular.utils import extend_schema
from core.permisssions import IsAdminUser


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user."""

    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [
        authentication.TokenAuthentication
    ]
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user


class PINListCreateAPIVIew(generics.ListCreateAPIView):
    queryset = models.PIN.objects.all()
    permission_classes = [
        IsAdminUser
    ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PINSerializer
        else:
            return PINGenerateRequestSerializer

    @extend_schema(
        request=PINGenerateRequestSerializer,
        responses={201: PINSerializer(many=True)}
    )
    def post(self, request, format=None):
        pin_type = request.data.get('pin_type')
        pin_count = request.data.get('pin_count', 1)
        school = request.user.school
        if not pin_type:
            return Response(
                {"error": "pin_type is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pins = []
        for _ in range(pin_count):
            pin_code = generate_unique_pin()
            pin = models.PIN(
                pin_code=pin_code,
                pin_type=pin_type,
                school=school
            )
            pin.save()
            pins.append(pin)
        
        serializer = PINSerializer(pins, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
