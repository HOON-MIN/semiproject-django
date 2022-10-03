from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect

from config.models import MyModel
from orders.models import OrdersDao, MyorderDao


def ordersForm(request):
    return render(request, "orders/ordersForm.html")
'''
    "insert into orders values(null,:mem_no,:i_no,:ord_count" \
    ",'상품준비중',:ord_address,:ord_name,now(), null,null,null);"
'''
def ordersInsert(request):
    ordersDao = OrdersDao()
    ordersData = (request.POST['mem_no'], request.POST['i_no'],
            request.POST['ord_count'],request.POST['ord_address'],
            request.POST['ord_name'])
    print(ordersData)
    print(type(ordersData))
    ordersDao.ordInsert(ordersData)
    return render(request, "orders/ordersList.html",
                  {'ord_name':request.POST['ord_name']})
# -------------- 보류 ---------------------------
# 회원이 주문 시(orders insert) 구매한 상품의 재고가 줄어들도록! stock update
# def ordersStockUpdate(request):
#     ordersDao = OrdersDao()
#     num = (int(request.POST['ord_no']))
#     print("ordersStockUpdate num => ", num, type(num))
#     ordersDao.ordStockUpdate(num)
#     return redirect("/orders/adminOrdersList")
# ---------------------------------------------

def adminOrdersList(request):
    ordersDao = OrdersDao()
    result = ordersDao.adminOrdList()
    # print(f"adminOrdListv => {result}")
    page = int(request.GET.get('page','1'))
    paginator = Paginator(result, '10')
    result = paginator.get_page(page)
    return render(request, "orders/adminOrdersList.html",
                  {'result':result})

def adminOrdersDetail(request):
    ordersDao = OrdersDao()
    ord_nov = int(request.GET['ord_no'])
    print("adminOrdersDetail ord_nov => ",ord_nov)
    ordDetailv = ordersDao.adminOrdDetail(ord_nov)
    print(f"adminOrdersDetail views res => {ordDetailv}")
    return render(request, 'orders/adminOrdersDetail.html', {'ordDetailv':ordDetailv})

def adminOrdersUpdate(request):
    ordersDao = OrdersDao()
    ordUpData = (int(request.POST['ord_no']),request.POST['ord_name'], request.POST['ord_address'],
                  request.POST['i_status'])
    print(ordUpData)
    print(type(ordUpData))
    ordersDao.adminOrdUpdate(ordUpData)
    return redirect("/orders/adminOrdersList")

def adminOrdersDelete(request):
    ordersDao = OrdersDao()
    ord_nov = int(request.GET['ord_no'])
    print(f"views ord_nov => {ord_nov, type(ord_nov)}")
    ckNum = ordersDao.adminOrdDeleteCheck(ord_nov)
    print("adOrdDel views ckNum =>",type(ckNum))
    # ckNum가 튜플로 반환되므로 인덱스 값으로 비교해야 됨!
    if ckNum[0] == 1:
        ordersDao.adminOrdDelete(ord_nov)
        print(f"주문번호 {ord_nov} 삭제 성공!")
        return redirect("/orders/adminOrdersList")
    else:
        # 알림 메세지 창 띄우려고 했는데 모르겠네 ?
        # messages.warning(request, "주문상태가 '주문취소' 경우에만 삭제가 가능합니다.")
        return redirect(f"/orders/adminOrdersDetail?ord_no={ord_nov}")

# ------------------------ 주문 취소 -------------------------------
def adminCanInsert(request):
    ordersDao = OrdersDao()
    ord_nov = request.POST['ord_no']
    creasonv = request.POST['creason']
    print("adminCanInsert ord_nov => ",ord_nov, type(ord_nov))
    print("adminCanInsert creason => ",creasonv, type(creasonv))
    indata = (ord_nov, creasonv)
    updata = (ord_nov, ord_nov)
    print("adminCanInsert indata updata => ",type(indata),type(updata))
    # --------------------------------
    # m = MyModel()
    # conn = m.mysqlconn()
    # cursor = conn.cursor()
    # sql_ins = """
    #     insert into cancel values(null, %s, sysdate(), %s)
    # """
    # cursor.execute(sql_ins, indata)
    # sql_up = """
    #     update orders set i_status = '주문취소', rcnt = 0,
    #         ord_cdate = (select cdate from cancel where ord_no = %s)
    #         where ord_no = %s
    # """
    # cursor.execute(sql_up, updata)
    # print("adminCanOrdUp 2")
    # cursor.close()
    # conn.commit()
    # conn.close()
    # print("여기는 adminCanOrdUp models 성공")
    # --------------------------------
    ordersDao.adminCanIns(indata, updata)
    ordDetailv = ordersDao.adminOrdDetail(ord_nov)
    print(f"adminCanInsert 의 Detail res => {ordDetailv}")

    # return redirect("/orders/adminOrdersList")
    return render(request, 'orders/adminOrdersDetail.html', {'ordDetailv': ordDetailv})
    # return redirect(f"/orders/adminOrdersDetail?ord_no={ord_nov}")


def adminCanOrdUpdate(request):
    ordersDao = OrdersDao()
    ordUpData = (int(request.POST['ord_no']),request.POST['ord_name'], request.POST['ord_address'],
                  request.POST['i_status'])
    print(ordUpData)
    print(type(ordUpData))
    ordersDao.adminOrdUpdate(ordUpData)
    return redirect("/orders/adminOrdersList")

# ------------- 보류 !!!  - 트랜잭션
# 고객이 주문취소 할 경우,
# cancel insert / orders update / stock 재고 update
# 3가지 쿼리 실행 필요하므로 트랜잭션 처리! : models에 3가지 dao만들고 여기에 불러다쓰자
# @transaction.atomic()
# def adminCanInsert(request):
#     ordersDao = OrdersDao()
#     d1 = (int(request.POST('ord_no')), int(request.POST['creason']))
#     # d2 =
#     # d3 =
#     ordersDao.transac_Cancel()
#     return redirect("/orders/adminOrdersList")

def orderForm(request):
    return render(request,"orders/ordersform.html")

# ord_no,mem_no,i_no,ord_count,i_status,ord_address,ord_name,ord_date,ord_edate,ord_cdate,rcnt
#sql = "insert into orders values(orders_seq.nextVal,:1, :2, :3,'상품준비중', :4,:5, sysdate(), null, null, null)"

#document.form1.action ='insert'
def orderIn(request):
    ordersDao = OrdersDao()
    data =(request.session['mem_no'],request.POST['i_no'], request.POST['ord_count'],
           request.POST['ord_address'], request.POST['ord_name'])
    print(data)
    ordersDao.ordInsert(data)
    return render(request, "orders/orderslist.html",
                  {'ord_address':request.POST['ord_address'],'ord_name':request.POST['ord_name']})

def order_list(request):
    myorderDao = MyorderDao()
    result = myorderDao.listMyorders(request)
    print(f"myorderList =>{result}")
    page = int(request.GET.get('page','1'))
    pageinator = Paginator(result, '10')
    result = pageinator.get_page(page)
    return render(request, "orders/orderslist.html",{'result':result})
# def order_list(request):
#     myorderDao = MyorderDao()
#     if request.method == 'GET':
#         page = int(request.GET.get('page', '1'))
#         searchValue = request.GET.get('searchValue', '')
#         if 0 < len(searchValue):
#             myorderList = MyorderDao.listMyorders(searchValue)
#         else:
#             myorderList = MyorderDao.listMyorders('')
#         pageinator = Paginator(myorderList, '10')
#         myorderList = pageinator.get_page(page)
#         return render(request, "orders/morderslist.html",
#                       {'myorderList': myorderList, 'searchValue': searchValue})
#     else:  # POST -> search
#         searchValue = request.POST['searchValue']
#         if 0 < len(searchValue):
#             myorderList = MyorderDao.listMyorders(searchValue)
#         else:
#             myorderList = MyorderDao.listMyorders('')
#
#         pageinator = Paginator(myorderList, '10')
#         page = 1
#         myorderList = pageinator.get_page(page)
#         return render(request, "orders/morderslist.html",
#                       {'myorderList': myorderList, 'searchValue': searchValue})


    # def orderChart(request):
    #     return render()

def orderschart(request):
    return render(request, "orders/orderschart.html")