from django.contrib import admin
from .models import Product, Solution, UserDevice, DeviceReading, Post
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
admin.site.register(Product)
admin.site.register(Solution)
admin.site.register(UserDevice)
admin.site.register(DeviceReading)
admin.site.register(Post)