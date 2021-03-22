from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from app1.models import Issue, Answer, Comment
from app1.forms import IssueForm, AnswerForm, CommentForm
# django内置装饰器login_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

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
        #  @login_required 装饰器配置.记录下下个url，方便把登录信息传过去？
        next_url = request.GET.get("next")
        # 注意： 这里传参一定要传给 data ！！！！！
        form = AuthenticationForm(data = request.POST)  
        print(form.is_valid(),form.error_messages)
        if form.is_valid():
            print(form.get_user())
            login(request, form.get_user())
            # return HttpResponse("Login Success")
            if next_url:
                return redirect(to=next_url)
            return redirect(to="ask_questions")        
    content = {}
    content["form"] = form 
    content["status"] = "login"
    # 默认返回 login.html 页面，注册成功则返回 "Login Success"/跳转到产品界面。
    # return render(request, "login.html",content)    
    return render(request, "Jzhihu_login.html", content)                  

# 将装饰器 @login_required 加在 views.py 里对应的请求处理函数前
@login_required
def ask_question(request):
    kmap = {}
    answers = Answer.objects.all()
    kmap["answers"] = answers
    if request.method == "POST":
        # IssueForm可以主动识别出表单中对应的字段和数据。
        form = IssueForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            anonymity = form.cleaned_data["anonymity"]
            # 创造Issue对象，把Issue模型类里面的参数都传进来。（除了时间）
            issue = Issue(author = request.user,title=title,description=description,anonymity=anonymity)
            issue.save()
            print("++++++++++valid & saved question++++++")
            # return redirect(to="ask_questions")          
        print(form.errors)   
    return render(request, "QA_zhihu.html", kmap)

@login_required
def answer(request, issue_id):
    # 这是post情况下做的事情。  
    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        print("form", form)
        if form.is_valid():
            # 从 AnswerForm(forms.Form) 中取出issue
            # issue_id = form.cleaned_data["issue_id"]
            print("issue_id", issue_id)
            
            answer = form.cleaned_data["answer"]
            anonymity = form.cleaned_data["anonymity"]
            # 一开始从前端表单传到后端表单得到，现在直接从url中获取。
            issue_obj = Issue.objects.get(id=issue_id)
            answer = Answer(author=request.user, issue=issue_obj,content=answer,anonymity=anonymity)
            answer.save()
            print("++++++++++ valid & saved answer ++++++")
            return redirect(to="answer", issue_id = issue_id)
        print(form.errors)
    # 这是默认get情况下做的事情。Q：可以把这段顺序放到if == post前吗？  
    # Q:为啥要传这个kmap  
    # A;1因为前端要显示每个issues的内容
    # 2这是默认get情况下做的事情。 
    print("issue_id:", issue_id)
    issues = Issue.objects.all()
    issue = Issue.objects.get(id=issue_id)
    kmap = {"issues": issues}
    kmap = {"issue": issue}
    return render(request,"answer_zhihu.html",kmap)        


@login_required
def submit_comment(request, answer_id):
    if request.method == "POST":
        form  = CommentForm(data = request.POST)
        # 为啥会不存在answer？？ answer.exists()
        # answer 就是可能会不存在，所以用 filter 并判断 exists（）
        # 如果answer_id是被修改过，且数据库中没有这条数据，则会报错，函数会直接停止执行。
        # 使用filter的话，即使没有，也是一个空列表，是否有值就用exists()函数。
        answer = Answer.objects.filter(id = answer_id)
        if form.is_valid() and answer.exists():
            user = request.user
            content = form.cleaned_data["content"]
            # 为啥是 answer.first()
            comment = Comment(author = user, content = content, answer=answer.first())
            comment.save()
            print("++++++++++ valid & saved comment ++++++")
            return redirect(to="answer", issue_id = answer.first().issue.id)
        print(form.errors)
        # 这一层对应的是啥？
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', ''))
        # 1: 获取路由。 post提交评价时，request.META['HTTP_REFERER'] 可以获取这个post数据从哪个路由来。
        # 2: 跳转路由。Django提供跳转url的函数：HttpResponseRedirect
        print("从路由", request.META['HTTP_REFERER'],"来")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ''))

