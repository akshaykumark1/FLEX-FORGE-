from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.signin, name='signin'),  # Ensure this line is here
    path('cart/', views.Cart_view, name='cart'),
    path('signup',views.signup,name='signup'),
    path('orders',views.orders,name='orders'),
    path('help',views.help,name='help'),
    path('log-out',views.userlogout,name='userlogout'),
    path('cart',views.Cart_view, name='cart'),


    path('admin',views.admin,name='admin'),





    path('product_buy',views.product_buy,name='product_buy'),   
    path('wheretobuy',views.wheretobuy,name='wheretobuy'),
    path('buy-now', views.buy_now, name='buy_now'),
    # Change this line
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('product_details/<int:pk>/',views.product_detail, name='product_detail'),   
    path('account',views.account,name='account'),
    # path('product')







    
    path('address',views.address,name='address'),
    path('security',views.security,name='security'),

#____________________wishlist___________________________#
    path('wishlist',views.wishlist,name='wishlist'),
    path('addtowishlist/<int:product_id>/', views.addtowishlist, name='addtowishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),






    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
