from django.urls import path

from cancel import views

# http://localhost:9000/address/write ==> views.py write() 호출
urlpatterns = [
    path('cancelList', views.cancelList),
    path('cancelResult', views.cancelResult),
    path('cancelChart', views.cancelChart),

]

