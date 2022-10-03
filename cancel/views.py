from django.core.paginator import Paginator
from django.shortcuts import render

from cancel.models import CancelDao


def cancelList(request):
    cancelDao = CancelDao()
    result = cancelDao.canList()
    # print(f"cancelList result => {result}")
    page = int(request.GET.get('page','1'))
    paginator = Paginator(result, '10')
    result = paginator.get_page(page)
    return render(request, "cancel/cancelList.html", {'result':result})

def cancelResult(request):
    cancelDao = CancelDao()
    result = cancelDao.canResult()
    return render(request, "cancel/cancelResult.html", {'result': result})

def cancelChart(request):
    cancelDao = CancelDao()
    res = cancelDao.canResult()
    print("cancelChart views res => ",res)
    print("cancelChart views res type => ",type(res))
    # listv = []
    list1 = []
    list2 = []
    for e in res:
        # result.append(list(e))
        # listv = list(e)
        list1.append(e[0])
        list2.append(e[1])
    result = zip(list1,list2)
    print("cancelChart views result => ",result)
    # result = list(res)
    for e in list1:
        print("list1 =>",e)
    for e in list2:
        print("list2 =>",e)

    return render(request, "cancel/cancelChart.html", {'result': result})
