from django.urls import path

from orders import views

urlpatterns = [
    path('ordersForm', views.ordersForm),
    path('ordersInsert', views.ordersInsert),
    path('adminOrdersList', views.adminOrdersList),
    path('adminOrdersDetail', views.adminOrdersDetail),
    path('adminOrdersUpdate', views.adminOrdersUpdate),
    path('adminOrdersDelete', views.adminOrdersDelete),
    path('adminCanInsert', views.adminCanInsert),
    path('ordersform',views.orderForm),
    path('orderIn',views.orderIn),
    path('orderslist',views.order_list),
    path('orderschart', views.orderschart),


]