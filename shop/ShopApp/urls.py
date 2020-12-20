from django.urls import path, include
from . import views
from .views import *

app_name = 'ShopApp'


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('logout', views.logout, name='logout'),
    # этот url нужен для авторизации пользователя
    path('login/', views.login, name='login'),
    # этот url нужен для регистрации пользователя
    path('register/', views.register, name='register'),
    path('contacts/', views.contacts, name='contacts'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart', CartView.as_view(), name='cart'),
    path('delete-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCart.as_view(), name='delete_from_cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCart.as_view(), name='add_to_cart'),
    path('change-qty/<str:ct_model>/<str:slug>/', ChangeQTY.as_view(), name='change_qty'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
