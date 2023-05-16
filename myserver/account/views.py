...
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView, UpdateView, CreateView, DetailView
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import check_password
from .models import User, UserLog, UserGroup
from .forms import *
from datetime import timedelta
import json, datetime
...
def register(request):
    # GET 방식 요청 -> 회원가입 페이지 요청
    if request.method == 'GET':
        return render(request, 'register.html')

    # POST 방식 요청 -> 사용자가 보낸 데이터를 데이터베이스에 저장
    elif request.method == 'POST':

        # client에게 입력받은 값을 가져온다.
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)
        email = request.POST.get('email', None)

        # 템플릿에 넘길 응답 데이터
        res_data = {}

        # 유효성 검사1 - 값을 모두 채우지 않는 경우
        if not (username and password and re_password and email):
            res_data['error'] = '모든값을 입력해야 합니다.'

        # 유효성 검사2 - 비밀번호와 확인-비밀번호가 다른 경우
        elif password != re_password:
            res_data['error'] = '비밀번호가 일치하지 않습니다.'

        # 모든 값을 입력받고 비밀번호가 일치하는 경우 User의 인스턴스를 생성
        # make_password 를 사용해 비밀번호 보안
        else:
            user = User(
                username=username,
                password=make_password(password),
                email=email
            )
            user.save()
            userLog = UserLog(
                username=User.objects.get(username=username),
            )

            # 데이터베이스에 저장

            userLog.save()

        # res_data = {'error':''} 에러 메세지를 전달
        return render(request, 'register.html', res_data)


# 로그인 함수
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            request.session['user'] = form.user_id
            userinfo = UserLog.objects.get(username=form.user_id)
            if userinfo.visitcount == None:
                cnt = 1
            else:
                cnt = userinfo.visitcount + 1
            userinfo.visitcount = cnt
            userinfo.login_at = datetime.datetime.utcnow()
            userinfo.save()
            return redirect('/home/')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@csrf_exempt
def login_api(request):

    if request.method == 'GET':
        # data = JSONParser().parse(request)
        username = request.GET['username']
        password = request.GET['password']

        request.session['user'] = username
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('incorrect id')

        userinfo = UserLog.objects.get(username=user.id)

        if check_password(password, user.password):
            if userinfo.visitcount == None:
                cnt = 1
            else:
                cnt = userinfo.visitcount + 1
            userinfo.visitcount = cnt
            userinfo.login_at = datetime.datetime.utcnow()
            userinfo.save()
            return HttpResponse('success!')
        else:
            return HttpResponse('incorrect password')


@csrf_exempt
def logout_api(request):
    # 로그아웃은 session에 저장된 user_id값을 지우면 된다.
    if request.session.get('user'):
        userinfo = UserLog.objects.get(username=request.session['user'])
        userinfo.logout_at = datetime.datetime.utcnow()
        userinfo.save()
        del (request.session['user'])
    return HttpResponse('success!')

def userlists_api(request):

    user_list = User.objects.all()
    user_result = []
    for i in user_list:
        user_dict = {}
        user_dict['id'] = i.id
        user_dict['username'] = i.username
        user_dict['password'] = i.password
        user_dict['email'] = i.email
        user_result.append(user_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(user_result, default=json_default)) # demo_task(soup)

# 127.0.0.1:8000/
def home(request):
    # login을 통해서 확인된 user는 session을 통해 user.id를 넘겨 받았다.
    user_id = request.session.get('user')

    # user_id유무를 통해 login판단
    if user_id:
        user = User.objects.get(pk=user_id)
        return HttpResponse(f'{user} login success')

    return HttpResponse('Home')


# 로그아웃 함수
def logout(request):
    # 로그아웃은 session에 저장된 user_id값을 지우면 된다.
    if request.session.get('user'):

        userinfo = UserLog.objects.get(username=request.session['user'])
        userinfo.logout_at = datetime.datetime.utcnow()
        userinfo.save()
        del (request.session['user'])

    # 로그아웃 후 127.0.0.1:8000/ 이동
    return redirect('/account/login/')

# 사용자
# user list HTML
# Users/User search
def userlists(request):
    template_name = 'user_list.html'
    user_list = User.objects.all()
    date = datetime.datetime.today() - timedelta(days=3)
    date = {
        "user_list": user_list,
        'dateFrom': date.strftime("%Y-%m-%d"),
        # 'path': '회사정보 / 설비정보등록'
    }
    return render(request, template_name, date)

# 사용자
def userstats(request):
    template_name = 'user_stat.html'

    date = datetime.datetime.today() - timedelta(days=3)
    date = {
        'dateFrom': date.strftime("%Y-%m-%d"),
        # 'path': '회사정보 / 설비정보등록'
    }
    return render(request, template_name, date)

def userstat_data(request):
    user_result = []
    user_list = UserLog.objects.all()

    for i in user_list:
        user_dict = {}
        user_dict['username'] = i.username.username
        user_dict['visitcount'] = i.visitcount
        user_dict['login_at'] = i.login_at
        user_dict['logout_at'] = i.logout_at
        user_result.append(user_dict)

    def json_default(value):
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        raise TypeError('not JSON serializable')

    return HttpResponse(json.dumps(user_result, default=json_default)) # demo_task(soup)


# Create your views here.
def user_group_update(request):

    UserGroup.objects.create(
        user_group_id = "visitor",
        user_group="3",
    )

    return JsonResponse({"message": 'success'})