from django.urls import path

from item import views
#http://localhost:9000/address/write ==> views.py write() 호출
urlpatterns = [
    path('detail',views.detail_item),
    path('new',views.new_itemList),
    path('write',views.register_page),
    path('regist',views.register_item),
    path('searchResult',views.search_item),
    path('chart',views.chart),
    path('admin',views.adminpage),
]