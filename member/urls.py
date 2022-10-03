from django.urls import path

from member import views
# http://localhost:9000/address/write ==> views.py write() 호출
urlpatterns = [
    path('joinForm', views.joinForm),
    path('joinMember', views.joinMember),
    path('loginForm', views.loginForm),
    path('logout', views.logout),
    path('findId', views.findId),
    path('findPwd', views.findPwd),
    path('myPageMain', views.myPageMain),
    path('myPageInfo', views.myPageInfo),
    path('idChk', views.idChk),
    path('emailChk', views.emailChk),
    path('memberList', views.MemberList),
    path('memberDetail', views.MemberDetail),
    path('memberUpdate', views.MemberUpdate),
    path('memberDelete', views.MemberDelete),
    path('memberChart', views.memberChart),
    path('memberChartAjax', views.memberChartAjax),
    path('memberLogChart', views.memberLogChart),
    path('memberLogChartAjax', views.memberLogChartAjax),
]

