import datetime
import hashlib
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from myresource.models import *
from myresource.forms import *


# Create your views here.
def pwd_set(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    pwd_setted = md5.hexdigest()
    return pwd_setted


def check_login(func):
    def inner(request, *args, **kwargs):
        # 把当前访问的网址拿到
        login_user = request.session.get('username')
        login_status = request.session.get('login_status')
        login_cookies_verification = request.COOKIES.get('username')
        if login_user and login_cookies_verification and login_status == '1' and login_user == login_cookies_verification:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'myresource/login.html')

    return inner


def login_info(request):
    data = {
        'code': '400',
        'status': 'false'
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = pwd_set(password)
        user_registry = Users.objects.filter(username=username).first()
        if user_registry:
            password_registry = user_registry.password
            if password_registry == password:
                data['code'] = '200'
                data['status'] = 'true'
        return JsonResponse(data)
    return render(request, 'myresource/login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('fullname')
        password = request.POST.get('password')
        rememberme = request.POST.get('rememberme')
        print(rememberme)
        password = pwd_set(password)
        user_registry = Users.objects.filter(username=username).first()
        if user_registry:
            password_registry = user_registry.password
            if password_registry == password:
                response = render(request, 'myresource/index.html')
                request.session['username'] = username
                request.session['login_status'] = '1'
                if rememberme:
                    response.set_cookie('username', username, max_age=30 * 24 * 60 * 60)
                response.set_cookie('username', username)
                return response
    return render(request, 'myresource/login.html')


def registry(request):
    data = {
        'code': '400',
        'status': 'false'
    }
    if request.method == 'POST':
        valid_data = request.POST
        username = valid_data.get('username')
        password = valid_data.get('confirmpassword')
        email = valid_data.get('email')
        password = pwd_set(password)

        user = Users()
        user.username = username
        user.email = email
        user.password = password
        user.save()
        data['code'] = '200'
        data['status'] = 'true'
    return JsonResponse(data)


def forget(request):
    return HttpResponse('hello world!')


@check_login
def index(request):
    return render(request, 'myresource/index.html')


@check_login
def base(request):
    return render(request, 'myresource/base.html')


@check_login
def calender(request):
    result = {
            "code": "400",
            "version": "v1.0",
            "data": [],
        }
    method = request.method
    username = request.COOKIES.get('username')
    user = Users.objects.filter(username=username).first()
    u_id = user.id
    event_list = DailyRoutine.objects.filter(user_id=u_id)
    for i in event_list:
        event_obj = {'id': i.id, 'title': i.title, 'start': i.time_start, 'end': i.time_end,
                     'backgroundColor': i.event_color, 'url': i.event_url, 'event_imgs': i.event_imgs,
                     'event_details': i.event_details, 'editable': i.event_editable}
        result['data'].append(event_obj)
    result["data"].append(method)
    result["code"] = "200"
    return render(request, 'myresource/calender.html',result)


class ResourceApi(View):
    def __init__(self, **kwargs):
        super(ResourceApi, self).__init__(**kwargs)
        self.result = {
            "code": "400",
            "version": "v1.0",
            "data": [],
        }

    def get(self, request):
        """
        查询event
        :param request:
        :return: json数据
        """
        method = request.method
        username = request.COOKIES.get('username')
        user = Users.objects.filter(username=username).first()
        u_id = user.id
        event_list = DailyRoutine.objects.filter(user_id=u_id)
        a = event_list[0].time_start
        print(a)
        for i in event_list:
            print(i.time_end)
            print(i.time_start)
            event_obj = {'id': i.id, 'title': i.title, 'start': i.time_start, 'end': i.time_end,
                         'backgroundColor': i.event_color, 'url': i.event_url, 'event_imgs': str(i.event_imgs),
                         'event_details': i.event_details, 'editable': i.event_editable}
            self.result['data'].append(event_obj)
        self.result["data"].append(method)
        self.result["code"] = "200"
        return JsonResponse(self.result)

    def post(self, request):
        """
        添加event
        :param request:
        :return: json数据
        """
        method = request.method
        username = request.COOKIES.get
        user = Users.objects.filter(username=username).first()
        event_title = request.POST.get('event_title')
        event_special = request.POST.get('event_special')
        time_start = request.POST.get('time_start')
        time_end = request.POST.get('time_end')
        event_color = request.POST.get('event_color')
        event_url = request.POST.get('event_url')
        event_imgs = request.POST.get('event_imgs')
        event_details = request.POST.get('event_details')

        event_new = DailyRoutine()
        event_new.title = event_title
        event_new.event_special = event_special
        event_new.time_start = time_start
        event_new.time_end = time_end
        event_new.event_color = event_color
        event_new.event_url = event_url
        event_new.event_imgs = event_imgs
        event_new.event_details = event_details
        event_new.user_id = user
        event_new.save()
        self.result["data"].append(method)
        self.result["code"] = "200"
        return JsonResponse(self.result)

    def put(self, request):
        """
        修改event
        :param request:
        :return: json数据
        """
        event_id = request.POST.get('event_id')
        modify_title = request.POST.get('modify_title')
        modify_special = request.POST.get('modify_special')
        modify_start = request.POST.get('modify_start')
        modify_end = request.POST.get('modify_end')
        modify_color = request.POST.get('modify_color')
        modify_url = request.POST.get('modify_url')
        modify_details = request.POST.get('modify_details')

        event_modify = DailyRoutine.objects.filter(id=event_id)
        event_modify.title = modify_title
        event_modify.event_special = modify_special
        event_modify.time_start = modify_start
        event_modify.time_end = modify_end
        event_modify.event_color = modify_color
        event_modify.event_url = modify_url
        event_modify.event_details = modify_details
        event_modify.save()
        method = request.method
        self.result["data"].append(method)
        self.result["code"] = "200"
        return JsonResponse(self.result)

    def delete(self, request):
        """
        删除event
        :param request:
        :return: json数据
        """
        method = request.method
        event_id = request.POST.get('event_id')
        event_delete = DailyRoutine.objects.filter(event_id)
        event_delete.delete()
        self.result["data"].append(method)
        self.result["code"] = "200"
        return JsonResponse(self.result)

def test(request):
    username = '1'
    user = Users.objects.filter(username=username).first()
    event_title = '1111111111111111111111'
    event_special = 'no'
    time_start = datetime.datetime.now().strftime('%Y-%m-%d')
    time_end = datetime.datetime.now().strftime('%Y-%m-%d')
    event_color = '#ff6700'
    event_url = 'www.baidu.com'
    event_imgs = '/static/myresource/img/1.jpeg'
    event_details = '11111111111111111111111111111111111111111111'

    event_new = DailyRoutine()
    event_new.title = event_title
    event_new.event_special = event_special
    event_new.time_start = time_start
    event_new.time_end = time_end
    event_new.event_color = event_color
    event_new.event_url = event_url
    event_new.event_imgs = event_imgs
    event_new.event_details = event_details
    event_new.user_id = user
    event_new.save()
    return HttpResponse('successful!')
