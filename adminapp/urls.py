from django.urls import path

from . import views

urlpatterns = [
    path('admin-login/', views.index, name='admin-login'),
    path("admin/sales/",views.sales,name="sales"),
    path("admin/purchase/",views.purchase,name="purchase"),
    path("admin/expence/",views.expence,name="expence"),
    path("admin/payment/",views.payment,name="payment"),
    path("admin/daybook/",views.daybook,name="daybook"),
    path("admin/ledger/",views.ledger,name="ledger"),
    path("admin/finalaccount/",views.ledger,name="finalaccount"),
    path("admin/customer/",views.customer,name="customer"),
    path("admin/supplier/",views.supplier,name="supplier"),
    
    path("admin/setting",views.setting,name="setting"),

    path("admin/product/",views.product,name="product"),
    path("product/update/<int:pk>/",views.product_update,name="productupdate"),
    path("product/delete/<int:pk>/",views.product_delete,name="productdelete"),

    path("admin/order/",views.order,name="order"),
    path("order/update/<str:pk>/",views.order_update,name="orderupdate"),
    path("order/delete/<int:pk>/",views.order_delete,name="orderdelete"),
    path("customerorder/details/<int:pk>/",views.product_as_per_customer,name="customerorder"),

]