from django.core.paginator import Paginator
from django.http import request
from django.shortcuts import render, redirect

# Create your views here.
from basket.models import MybasketDao

def basketordersForm(request):
    return render(request,"basket/basketordersform.html")

def basket_list(request):
    mybasketDao = MybasketDao()
    result = mybasketDao.listMybasket(request)
    print(f"result =>{result}")
    page = int(request.GET.get('page','1'))
    pageinator = Paginator(result, '10')
    result = pageinator.get_page(page)
    return render(request, "basket/blist.html",{'result':result})

# #Detail 페이지 만들기
def basketdetail(request):
    mybasketDao = MybasketDao()
    bnum= int(request.GET['b_num'])
    print("bnum :",bnum)
    basketdetail = mybasketDao.basketDetail(bnum)
    return render(request, 'basket/basketDetail.html', {'basketdetail': basketdetail})

def basketUpdate(request):
    mybasketDao = MybasketDao()
    data1 = request.POST['b_num']
    data2 = request.POST['b_stock']
    data3 = (data2,data1)
    mybasketDao.basketUpdate(data3)
    return redirect('/basket/blist')

def basketDelete(request):
    mybasketDao = MybasketDao()
    bnum = int(request.POST['b_num'])
    basketDelete = mybasketDao.basketDelete(bnum)
    return redirect('/basket/blist')

# def insertBasket(request):
#     mybasketDao = MybasketDao()
#     data = (request.POST['b_num'],request.session['mem_no'], request.POST['i_no'],
#             request.POST['b_stock'])
#     print(data)
#     print(type(data))
#     mybasketDao.insertBasket(data)
#     return render(request, "basket/bist.html")

# 장바구니폼에서  select 하기
def selbaorform(request):
    mybasketDao = MybasketDao()
    bnum = int(request.POST['b_num'])
   # bnum = request.POST.get('bnum', False);
    print("bnum :", bnum)
    baorder = mybasketDao.basketordersform(bnum)
    return render(request, 'basket/basketordersform.html', {'baorder': baorder})

# 장바구니폼에서 주문하기
# def basketorderIn(request):
#     mybasketDao = MybasketDao()
#     data = (request.POST['b_num'],request.session['mem_no'], request.POST['i_no'],
#             request.POST['b_stock'])
#     print(data)
#     print(type(data))
#     mybasketDao.baOrderInsert(data)
#     return render(request, "basket/bist.html")

# 장바구니에서 폼에서 주문하기
##"insert into item values(null,%s,%s,%s" \",'상품준비중',%s,%s,sysdate(), null,null,null);"
##        sql_ordInsert = "insert into item values(null,:mem_no,:i_no,:ord_count" \
##                     ",'상품준비중',:ord_address,:ord_name,sysdate(), null,null,null)"
def baOrderInsert(request):
    mybasketDao = MybasketDao()
    num1 = int(request.POST['i_no'])
    num2 = int(request.POST['ord_count'])
    bnum = int(request.POST['b_num'])
    data = (request.session['mem_no'],num1,num2,
            request.POST['ord_address'],request.POST['ord_name'])
    print(data)
    print(type(data))
    mybasketDao.baOrderInsert(data)
    mybasketDao.basketDelete(bnum)
    return redirect('/orders/orderslist')

