# main_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # --------
    # A. Autentifikacija
    # --------
    path('users/register/', views.CreateUserView.as_view(), name='register'),
    path('users/login/', views.LoginView.as_view(), name='login'),
    path('users/token/refresh/', views.VerifyUserView.as_view(), name='token_refresh'),
    
    # --------
    # B. CRUD Rute za Agro ConSys
    # --------

    # Products catalogue
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:id>/', views.ProductDetail.as_view(), name='product-detail'),
    
    # Solution (Water Management, etc )
    path('solutions/', views.SolutionList.as_view(), name='solution-list'),
    path('solutions/<int:id>/', views.SolutionDetail.as_view(), name='solution-detail'),

    # Blog / News
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:id>/', views.PostDetail.as_view(), name='post-detail'),
    
    # --------
    # C. Protected Routes (User Dashboard)
    # --------
    
    # Users Device
    path('mydevices/', views.UserDeviceList.as_view(), name='mydevice-list'),
    path('mydevices/<int:id>/', views.UserDeviceDetail.as_view(), name='mydevice-detail'),
    path('mydevices/<int:id>/toggle_irrigation/', views.ToggleIrrigation.as_view(), name='toggle-irrigation'),
    # Reading for specific device
    path('readings/create/', views.DeviceReadingCreate.as_view(), name='reading-create'),
    # Rout for specific list reading diagram
    path('mydevices/<int:device_id>/readings/', views.DeviceReadingList.as_view(), name='reading-list'),
]
