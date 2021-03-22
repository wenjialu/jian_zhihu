"""jian_zhihu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app1.views import register, index_login, ask_question, answer, submit_comment

urlpatterns = [
    path(r'admin/', admin.site.urls),
    # path(r'admin/app1/profile/', admin.site.urls),
    path(r'', register),
    path(r'login/', index_login, name="login"),
    path(r'register/', register, name="register"),
    path(r'questions/', ask_question, name="ask_questions"),
    path(r'questions/(.*)', ask_question, name="ask_questions"),
    path(r'questions/...', ask_question, name="ask_questions"),
    path(r'questions/?', ask_question, name="ask_questions"),
    # path(r'answer/', answer, name="answer"),
    # 在django2.0之后，需要用re_path函数才适合正则匹配。 (?P<username>re)
    re_path(r'answer/(?P<issue_id>\d+)/$',answer, name="answer"),
    re_path(r'comment/(?P<answer_id>\d+)/$',submit_comment, name="comment"),
]
