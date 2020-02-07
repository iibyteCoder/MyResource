from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from myresource.views import *

urlpatterns = [
    path('login/', login),
    path('login_info/', login_info),
    path('registry/', registry),
    path('forget/', forget),
    path('index/', index),
    path('base/', base),
    path('calender/', calender),
    # path('Api/', csrf_exempt(ResourceApi.as_view())),
    path('Api/', ResourceApi.as_view()),
    path('test/',test)
]
