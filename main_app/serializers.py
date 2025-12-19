from rest_framework import serializers
from .models import Product, Solution, UserDevice, DeviceReading, Post
from django.contrib.auth.models import User
from datetime import date

# 1. Serializers for PUBLIC routes (Catalog, Solutions, Blog)

# A) Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# B) Solution Serializer
class SolutionSerializer(serializers.ModelSerializer):
    # Prikazivanje liste Proizvoda povezanih sa Rešenjem (M:N veza)
    # Koristi ProductSerializer za detaljan prikaz
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Solution
        fields = '__all__'

# C) Post Serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

#-----
# 2. Serializers for PROTECTED rute (User Dashboard)
#-----
# D) DeviceReading Serializer
class DeviceReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceReading
        fields = '__all__'
        # fields = ('air_temp', 'soil_moisture', 'co2_concentration', 'timestamp') 

# E) UserDevice Serializer
class UserDeviceSerializer(serializers.ModelSerializer):
    # The user (owner) will be set automatically (B.2. perform_create)
    user = serializers.ReadOnlyField(source='user.username')
    
    # Show Product details instead of just the ID
    product_details = ProductSerializer(source='product', read_only=True)
    

    class Meta:
        model = UserDevice
        fields = '__all__' # Include is_irrigation_on, name, location, etc.

# -------
# 3. User Serializer (za Autentifikaciju)
# -------

# F) User Serializer (used to return basic info after registration/login)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')