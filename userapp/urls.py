from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("productdetails/<str:slug>/",views.productdetails,name="productdetails"),
    path("shop/",views.shop_page,name="shop_page"),
    path("retail_shop/",views.retail_shop,name="retail_shop"),
    path("search_items/",views.search_result,name="search_items"),
    path("filter_result/",views.filter_result,name="filter_result"),
    path("shop/category/<slug:cat_slug>/",views.category_page,name="category_page"),
    path("wats_on_sale/",views.wat_on_sale,name="wats_on_sale"),
    path("how_to_order/",views.how_to_order,name="how_to_order"),
    path("faqs/",views.faqs,name="faqs"),

    path('wishlist/wishlist-detail/',views.wishlist_detail,name='wishlist_detail'),
    path('wishlist/add/<int:id>/', views.wishlist_add, name='wishlist_add'),
    path('wishlist/item_clear/<int:id>/', views.wishlist_item_clear, name='wishlist_item_clear'),
   

    


    # cart function 
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path("cart/checkout/",views.place_order,name="place_order"),
    path("user_logout/",views.user_logout,name="user_logout"),
    path("customerregister/",views.customerregister,name="customerregister"),
    path("customerlogin/",views.customerlogin,name="customerlogin"),





]