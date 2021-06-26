from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('service/',views.service,name='service'),
    path('shop/',views.shop,name='shop'),
    path('product/',views.product,name='product'),
    path('contact/',views.contact,name='contact'),
    path('single/',views.single,name='single'),
   	path('hearder/',views.hearder,name='hearder'),
   	path('register/',views.register,name='register'),
   	path('login/',views.login,name='login'),
    path('validate_otp/',views.validate_otp,name='validate_otp'),
    path('logout/',views.logout,name='logout'),
    path('saller_login/',views.saller_login,name='saller_login'),
    path('saller_add_product/',views.saller_add_product,name='saller_add_product'),
    path('saller_view_product/',views.saller_view_product,name='saller_view_product'),
    path('saller_index/',views.saller_index,name='saller_index'),
    path('saller_details_product/<int:pk>/',views.saller_details_product,name='saller_details_product'),
    path('saller_edit_product/<int:pk>/',views.saller_edit_product,name='saller_edit_product'),
    path('saller_delete_product/<int:pk>/',views.saller_delete_product,name='saller_delete_product'),
    path('user_view_product/<str:pb>/',views.user_view_product,name='user_view_product'),
    path('user_details_product/<int:pid>/',views.user_details_product,name='user_details_product'),
    path('add_to_wishlist/<int:pk>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('mywishlist/',views.mywishlist,name='mywishlist'),
    path('remove_from_wishlist/<int:pk>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('mycart/',views.mycart,name='mycart'),
    path('remove_from_cart/<int:pk>/',views.remove_from_cart,name='remove_from_cart'),
    path('change_qty/',views.change_qty,name='change_qty'),
    path('user_product_search/',views.user_product_search,name='user_product_search'),
    path('ajax/validate_email/',views.validate_email, name='validate_email'),
    path('pay/',views.initiate_payment,name='pay'),
    path('callback/',views.callback, name='callback'),
    

    
]
