import re

from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from item.models import ItemList

# 새 상품 리스트 등록 순 리스트
def new_itemList(request):
    list_ref = ItemList()
    itemlist = list_ref.new_itemList()

    ## 페이징 처리
    page = int(request.GET.get('page', '1'))
    pageinator = Paginator(itemlist, '15')
    item_list = pageinator.get_page(page)
    startpage = int((page - 1) / 5) * 5 + 1;
    endpage = startpage + 5 - 1 if startpage != 1 else 5;
    pageRange = [i for i in range((startpage if startpage >= 5 else startpage), endpage + 1)]

    return render(request,"item/new_itemList.html",{'result':item_list , 'pageRange':pageRange})

#상품 검색 기능 및 검색 결과
@csrf_exempt
def search_item(request):
    search_ref = ItemList()

    if request.method == 'GET':
        page = int(request.GET.get('page', '1'))
        print(page)
        searchValue = request.GET.get('searchValue','')

        if 0 < len(searchValue):
            print("get if")
            result = search_ref.search_item(searchValue)
        else: #POST -> search
            print("get else")
            result = search_ref.search_item(searchValue)


        pageinator = Paginator(result, '15')
        item_list = pageinator.get_page(page)
        print(item_list)
        return render(request, "item/search_itemlist.html",
                      {'searchValue': searchValue, 'result': item_list})
    else:
        searchValue = request.POST['searchValue']
        if 0 < len(searchValue):
            print("post if")
            result = search_ref.search_item(searchValue)

        else:  # POST -> search
            print("post else")
            result = search_ref.search_item('')
        print(result)
        pageinator = Paginator(result, '15')
        page = 1
        item_list = pageinator.get_page(page)
        print(item_list)
        return render(request, "item/search_itemlist.html",
                      {'searchValue': searchValue, 'result': item_list})
    # where num like '%%%s%%' sql문



# 상품 디테일 페이지
def detail_item(request):
    num = request.GET['i_no']
    detail_ref = ItemList()
    res = detail_ref.detail_item(num)
    print(res)
    return render(request, "item/detail_item.html", {'itemlist':res})




#상품 등록 페이지 이동
def register_page(request):
    return render(request,"item/reg_item.html")

#상품 등록 작성 및 등록 후 newmainlist출력
@csrf_exempt
def register_item(request):
    UPLOAD_DRI = '/home/kosmo113/python/workspace/semiDemo2/item/static/images/'
    IMG_DIR = '/static/images/'
    if 'i_img' in request.FILES:
        file = request.FILES['i_img']
        file_name = IMG_DIR+file.name
        fp = open(UPLOAD_DRI+file.name,'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()
    else:
        file_name = '-'
    print(file_name)
    item = (request.POST['i_name'],
            request.POST['i_price'],
            request.POST['i_category1'],
            request.POST['i_category2'],
            request.POST['i_comm'],
            file_name,
            )
    print(type(item))
    print(item)
    register_ref = ItemList()
    res = register_ref.registration_item(item)
    print(res)
    itemlist=ItemList()
    list = itemlist.new_itemList()
    return render(request,"item/new_itemList.html",{'item_list':list})

def chart(request):
    itemlist = ItemList()
    chartres = itemlist.chart_item()
    num = 1

    return render(request,"item/chart_item.html",{'chartData':chartres,'num':num})


def adminpage(request):
    return render(request,"item/admin_item.html")
