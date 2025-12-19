from django.shortcuts import render
# Create your views here.
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied # For ownership verification

from .serializers import (
    ProductSerializer, SolutionSerializer, PostSerializer,
    UserDeviceSerializer, DeviceReadingSerializer, UserSerializer
)
from .models import Product, Solution, UserDevice, DeviceReading, Post

# ---------
# A. Autentification (Login, Register, Verify)
# ---------

# 1. User Creation (Registration) - generics.CreateAPIView
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] 

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # If creation is successful, automatically generate a JWT token
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        })

# 2. User Login (Login) - APIView
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Check credentials
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# 3. Token Verification (Verify) - APIView
class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request):
        # request.user is automatically populated by the JWT
        user = User.objects.get(username=request.user) 
        refresh = RefreshToken.for_user(request.user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

# 5. Product Detail Views:
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id' 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

# 6. Solution Views:
class SolutionList(generics.ListCreateAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

# 7. Solution Detail Views:
class SolutionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

# 8. Post Views, Blog
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

# 9. Post Detail Views
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserDeviceList(generics.ListCreateAPIView):
    serializer_class = UserDeviceSerializer
    
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# 11. UserDevice Detail Views
class UserDeviceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserDeviceSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserDevice.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        device = self.get_object()
        if device.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to edit this device."})
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied({"message": "You do not have permission to delete this device."})
        instance.delete() #

# 12. DeviceReading Views 
class DeviceReadingCreate(generics.CreateAPIView):
    queryset = DeviceReading.objects.all()
    serializer_class = DeviceReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

# 13. DeviceReading List Views
class DeviceReadingList(generics.ListAPIView):
    serializer_class = DeviceReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Dohvata ID uređaja iz URL-a
        device_id = self.kwargs['device_id']
        # Vraća samo očitavanja za taj uređaj
        return DeviceReading.objects.filter(device__id=device_id, device__user=self.request.user)
    # 14. Custom route for turning irrigation on/off
class ToggleIrrigation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        try:
            # 1. Find device by ID
            device = UserDevice.objects.get(id=id)
        except UserDevice.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

        # 2. Check if the user is the owner (Data protection)
        if device.user != request.user:
            raise PermissionDenied({"message": "You do not have permission to control this device."})

        # 3. Switch status (True -> False, False -> True)
        device.is_irrigation_on = not device.is_irrigation_on
        device.save()

        # 4. Return the updated status using our serializer
        serializer = UserDeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)