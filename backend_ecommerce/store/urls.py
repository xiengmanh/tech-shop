from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Bro đã tự viết logout rồi
    path('register/', views.register_view, name='register'),

    # Password change
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='store/password_change_done.html'), name='password_change_done'),

    # Giỏ hàng, checkout, đơn hàng
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),

    # Sản phẩm
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('laptop/', views.laptop_list, name='laptop_list'),
    path('phone/', views.phone_list, name='phone_list'),
    path('tablet/', views.tablet_list, name='tablet_list'),
    path('smartwatch/', views.smartwatch_list, name='smartwatch_list'),
    path('headphones/', views.headphones_list, name='headphones_list'),
    path('pc/', views.pc_list, name='pc_list'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
]
