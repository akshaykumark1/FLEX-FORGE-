from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.signin, name='signin'),  # Ensure this line is here
    path('cart/', views.Cart_view, name='cart'),
    path('remove_from_cart/<id>',views.remove_from_cart,name='remove_from_cart'),
    path('signup',views.signup,name='signup'),
    path('orders',views.orders,name='orders'),
    path('help',views.help,name='help'),
    path('log-out',views.userlogout,name='userlogout'),
    path('search',views.search1,name='search'),







    path('product_buy',views.product_buy,name='product_buy'),   
    path('wheretobuy',views.wheretobuy,name='wheretobuy'),
    path('buy-now<int:product_id>/', views.buy_now, name='buy_now'),
    # Change this line
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('product_details/<int:pk>/',views.product_detail, name='product_detail'),   
    path('account',views.account,name='account'),
    # path('product')


#######admin#####
    path('admin', views.admin, name='admin'),

    path('add_product',views.add_product,name='add_product'),



    
    path('address',views.address,name='address'),
    path('security',views.security,name='security'),

#____________________wishlist___________________________#
    path('wishlist',views.wishlist,name='wishlist'),
    path('addtowishlist/<int:product_id>/', views.addtowishlist, name='addtowishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
# payments
    path('index',views.index,name='index'),
    path('order_payment/<id>',views.order_payment,name='order_payment')






    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
