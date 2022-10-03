from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from member.models import LogModel, JoinProcess, MemberProcess, PagingSet, memberChart1, MemberLogChart


def joinForm(request):
    return render(request, "member/joinForm.html")

def joinMember(request):
    join_list = (request.POST['mem_id'], request.POST['mem_pw'], request.POST['mem_name'],
                request.POST['mem_jubun'], request.POST['mem_email'], request.POST['mem_phone'],
                request.POST['mem_adr'], request.POST['mem_q'], request.POST['mem_a'])
    joinProcess = JoinProcess()
    joinProcess.joinmember(join_list)
    return render(request, "main.html")

def idChk(request):
    mem_id = request.GET['mem_id']
    print(mem_id)
    joinProcess = JoinProcess()
    res = joinProcess.idcheck(mem_id)
    print('id', res[0])
    return render(request, 'member/idChk.html', {'res': res[0]})

def emailChk(request):
    mem_email = request.GET['mem_email']
    print(mem_email)
    joinProcess = JoinProcess()
    res = joinProcess.emailcheck(mem_email)
    print('email', res[0])
    return render(request, 'member/emailChk.html', {'res': res[0]})

def MemberList(request):
    if request.session['user_id'] != 'admin':
        return redirect("/")
    chk_method = request.method
    page = int(request.GET.get('page', '1'))
    paging = PagingSet(chk_method, request)
    count = paging.count()
    searchValue = paging.page_list()
    items = paging.searchVal_len(searchValue)
    paginator = Paginator(items, '10')

    # 페이징 처리를 위한 연산과정
    last_page_num = 0
    for last_page in paginator.page_range:
        last_page_num = last_page_num + 1

    current_block = ((int(page) -1) / 5) +1
    current_block = int(current_block)
    page_start_number = ((current_block - 1) * 5) + 1
    page_end_number = page_start_number + 5 - 1

    res = paginator.get_page(page)

    return render(request, 'member/memberList.html', {'result':res, 'searchValue':searchValue, 'count':count, 'last_page_num':last_page_num, 'page_start_number':page_start_number, 'page_end_number':page_end_number})

def MemberDetail(request):
    memberProcess = MemberProcess()
    if request.session['user_id'] == 'admin':
        msg1 = 'mem_no'
        msg2 = request.GET['mem_no']
        tup1 = (msg1, msg2)
        memberDetail = memberProcess.memberDetail(tup1)
        print(memberDetail)
        return render(request, 'member/memberDetail.html', {'memberDetail': memberDetail})
    else:
        msg1 = 'mem_id'
        msg2 = request.session['user_id']
        tup1 = (msg1, msg2)
        memberDetail = memberProcess.memberDetail(tup1)
        print(memberDetail)
        return render(request, 'member/myPageInfo.html', {'memberDetail': memberDetail})

def MemberUpdate(request):
    memberProcess = MemberProcess()
    list = (request.POST['mem_name'], request.POST['mem_phone'], request.POST['mem_adr'], request.POST['mem_no'])
    memberProcess.memberUpdate(list)
    if request.session['user_id'] == 'admin':
        return redirect('/member/memberList')
    else:
        return redirect('/member/myPageMain')

def MemberDelete(request):
    memberProcess = MemberProcess()
    mem_no = request.POST['mem_no']
    print(mem_no)
    memberProcess.memberDelete(mem_no)
    if request.session['user_id'] == 'admin':
        return redirect('/member/memberList')
    else:
        logout(request)
        return redirect('/')

def myPageInfo(request):
    return render(request, 'member/myPageInfo.html')

def loginForm(request):
    if 'user_id' in request.session:
       return redirect('/')
    if request.method == 'POST':
        user_id = request.POST['mem_id']
        user_pwd = request.POST['mem_pw']
        loginArg = (user_id,user_pwd)
        res = LogModel(loginArg).loginCheck()
        print(res)
        if res is not None:
            request.session['user_id'] = user_id
            request.session['user_name'] = res[0]
            request.session['mem_no'] = res[1]
            msg = 'login'
            LogModel(msg).memberlog(request)
            return redirect('/')
        else:
            warning = {'msg':'아이디 또는 비밀번호를 올바르게 입력하세요'}
            return render(request, 'member/loginForm.html', {'warning':warning})
    return render(request, 'member/loginForm.html')

def logout(request):
    msg = 'logout'
    LogModel(msg).memberlog(request)
    del request.session['user_id']
    del request.session['user_name']
    del request.session['mem_no']
    return redirect('/')

def findId(request):
    if request.method == 'POST':
        mem_name = request.POST['mem_name']
        mem_email = request.POST['mem_email']
        find = (mem_name,mem_email)
        res = LogModel(find).findIdPwd()
        if res is not None:
            result = {'id':res[0]}
        else:
            result = {'id':'해당하는 아이디가 존재하지 않습니다'}
        return render(request, 'member/findId.html', {'result': result})
    return render(request, 'member/findId.html')

def findPwd(request):
    if request.method == 'POST':
        mem_id = request.POST['mem_id']
        mem_q = request.POST['mem_q']
        mem_a = request.POST['mem_a']
        find = (mem_id,mem_q,mem_a)
        res = LogModel(find).findIdPwd()
        if res is not None:
            result = {'pwd':res[0]}
        else:
            result = {'pwd':'해당하는 비밀번호가 존재하지 않습니다'}
        return render(request, 'member/findPwd.html', {'result': result})
    return render(request, 'member/findPwd.html')

def myPageMain(request):
    return render(request, 'member/myPageMain.html')

def memberChart(request):
    return render(request, 'member/memberChart.html')

def memberChartAjax(request):
    rval = request.GET['rval']
    print(rval)
    if rval == 'a':
        result = memberChart1().genderChart()
        result2 = dict(result)
        return JsonResponse(result2,safe=False)
    elif rval == 'b':
        result = memberChart1().birthChart()
        result2 = dict(result)
        return JsonResponse(result2, safe=False)
    elif rval == 'c':
        result = memberChart1().locChart()
        result2 = dict(result)
        return JsonResponse(result2, safe=False)
    else:
        result = memberChart1().locChart2(rval)
        result2 = dict(result)
        return JsonResponse(result2, safe=False)

def memberLogChart(request):
    return render(request, 'member/memberLogChart.html')

def memberLogChartAjax(request):
    rval = request.GET['rval']
    if rval == 'a':
        chart = dict(MemberLogChart().envLogChart1())
        return JsonResponse(chart,safe=False)
    elif rval == 'b':
        chart = dict(MemberLogChart().browserLogChart1())
        return JsonResponse(chart,safe=False)
    elif rval == 'c':
        chart = MemberLogChart().ratioChart1()
        chart1 = tuple(chart[0])
        print(chart1)
        return JsonResponse(chart1, safe=False)