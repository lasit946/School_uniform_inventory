from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # LANDING PAGE (Now Login)
    path('', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    
    # INVENTORY PAGES
    path('inventory/', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('sell/<int:pk>/', views.sell_item, name='sell_item'),
    path('report/', views.sales_report, name='sales_report'),

    # AUTHENTICATION
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
]