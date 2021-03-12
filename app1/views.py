from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
# Create your views here.

# UserCreationForm: Django 自带的注册表单
def register(request):
    if request.method == "GET":
        form  = UserCreationForm()
    if request.method == "POST":
        form  = UserCreationForm(request.POST)
        print(request.POST)
        # is_valid 不仅判断 表单是否存在，主要会判断是否符合规范，比如至少8个字符，包含字母等。
        print(form.is_valid())
        if form.is_valid():
            print("开始保存表单")
            form.save()
            print("表单保存成功")
            return redirect(to = "login")
    # 用字典来装 post 的内容， 并传入到 render 函数中。
    content = {}
    content["form"] = form 
    content["status"] = "register"
    # 默认返回 register.html 页面，注册成功则返回 "Register Success"/跳转到登录界面。
    # return render(request, "register.html",content)        
    return render(request, "Jzhihu_login.html",content)     

# AuthenticationForm： Django 自带的认证表单 
# 注意函数起名不要起login啊，和  Django 自带的login 冲突了。
def index_login(request):
# 如果是简单的GET请求，只需要初始化登录的表单，然后传到前端进行渲染
    if request.method == "GET":
        form = AuthenticationForm()
# 如果是POST请求，使用AuthenticationForm接收post参数，并进行验证，验证通过，进行登录处理。        
    if request.method == "POST":
        # 注意： 这里传参一定要传给 data ！！！！！
        form = AuthenticationForm(data = request.POST)  
        print(form.is_valid(),form.error_messages)
        if form.is_valid():
            print(form.get_user())
            login(request, form.get_user())
            return HttpResponse("Login Success")
    content = {}
    content["form"] = form 
    content["status"] = "login"
    # 默认返回 login.html 页面，注册成功则返回 "Login Success"/跳转到产品界面。
    # return render(request, "login.html",content)    
    return render(request, "Jzhihu_login.html", content)                  

 

