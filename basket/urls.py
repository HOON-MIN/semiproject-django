from django.urls import path

from basket import views

urlpatterns = [
    path('blist', views.basket_list),
    path('basketDetail', views.basketdetail),
    path('basketUpdate', views.basketUpdate),
    path('basketDelete', views.basketDelete),
    path('basketordersform', views.selbaorform),
    path('baOrderInsert', views.baOrderInsert),

    # path('product_detail', views.product_detail),
    # path('product_update', views.product_update),
    # path('product_delete', views.product_delete),


]