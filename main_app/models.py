
# Create your models here.
from django.db import models
from django.contrib.auth.models import User 
from datetime import date 

# --- 1. Model: Product (Catalog of Senzors/OpremeProducts) ---
# Relation: Many-to-Many with Solution
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=50, default='Senzor')

    def __str__(self):
        return f'{self.name} ({self.category})'

# --- 2. Model: Solution (Koncepcijska Rešenja, npr. Water Management) ---
# Relation: Many-to-Many with Product
class Solution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    icon_url = models.CharField(max_length=200, blank=True, null=True)
    # M:N relation: One Product is part of multiple Solutions, and one Solution uses multiple Products.
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name

# --- 3. Model: UserDevice (A device that belongs to the user) ---
# Relation: One-to-Many sa User (vlasnikom)
class UserDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    name = models.CharField(max_length=100) # The name given by the user (e.g. ‘Pepper Greenhouse’)
    location = models.CharField(max_length=200, blank=True)
    
    # B.1. Custom Logic: Irrigation Status Simulation
    is_irrigation_on = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} (Vlasnik: {self.user.username})'

# --- 4. Model: DeviceReading
# Veza: Many-to-One with UserDevice (each reading belongs to a single device)
class DeviceReading(models.Model):
    device = models.ForeignKey(UserDevice, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Fields for simulation
    air_temp = models.DecimalField(max_digits=5, decimal_places=2)
    air_humidity = models.DecimalField(max_digits=5, decimal_places=2)
    soil_moisture = models.DecimalField(max_digits=5, decimal_places=2)
    soil_minerals = models.DecimalField(max_digits=5, decimal_places=2)
    co2_concentration = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        # Sorts the readings by time (newest first)
        class Meta:
            ordering = ['-timestamp']
            
        return f'Očitavanje za {self.device.name} @ {self.timestamp}'


# --- 5. Model: Post (News/Blog) ---
# An additional model for complexity and CRUD functionality
class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    date_posted = models.DateField(default=date.today)
    author = models.CharField(max_length=100, default='Agro ConSys Team')

    def __str__(self):
        return self.title