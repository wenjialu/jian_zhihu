from django.db import models
from django.contrib.auth.models import User, AbstractUser
import datetime
# Create your models here.
# 写完 Admin 用户类， 都要去 admin.py 去注册。

#拓展User表格的方法，
# 方法一：使用和用户模型一对一的链接(使用Profile扩展User模块)：
class Profile(models.Model):
    nickname = models.CharField(max_length=128,default="很懒的一个用户")
    phone = models.CharField(max_length=11,default="1234566")
    address = models.CharField(max_length=256,default="用户很懒，没填写地址")
    abstract = models.TextField(default="用户很懒，没有描述")
    #和User表做一对一关系映射.  注意要加上on_delete
    user = models.OneToOneField(to=User, related_name="profile", on_delete=models.CASCADE)
    def __str__(self):
        return self.nickname

#拓展User表格的方法，(setting 中 配置  AUTH_USER_MODEL 慎用！！！)
# 方法二：继承AbstractUser创建自己的用户模型：   
# step1:     
# class User(AbstractUser):
#     nickname = models.CharField(max_length=128,default="很懒的一个用户")
#     phone = models.CharField(max_length=11,default="1234566")
#     address = models.CharField(max_length=256,default="用户很懒，没填写地址")
#     abstract = models.TextField(default="用户很懒，没有描述")
#     def __str__(self):
#         return self.nickname
# step2: 在 setting.py 中.(注意在setting中改了model就算注释掉也不可逆，除非重新赋值)
# 设置 AUTH_USER_MODEL = "app1.User"，这样使用的就不是自带的user，而是自定义的 user 类。


# 问题
# 问题标题 问题描述 提问者 匿名与否 时间  （话题）
class Issue(models.Model):
    # id 是django自带的。models默认都会有个id属性，是自增的.
    title = models.CharField(max_length=256)
    description = models.TextField(default="")
    author = models.ForeignKey(to=User, related_name="issues", on_delete=models.CASCADE)
    create_time = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    anonymity = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# 回答
# 对应问题 回答内容 回答者 匿名与否 回答时间 赞成 反对 阅读量 草稿/发布 
class Answer(models.Model):
    issue = models.ForeignKey(to = Issue ,related_name="answers", on_delete=models.CASCADE)
    content = models.TextField(default="")
    author = models.ForeignKey(to = User ,related_name="answers", on_delete=models.CASCADE)
    anonymity = models.BooleanField(default=False)
    create_time = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    agree = models.IntegerField(default=0)
    disagree = models.IntegerField(default=0)
    read_num = models.IntegerField(default=0)
    Status = (
        (0,'草稿'),
        (1,'发布')
        )
    status = models.IntegerField(choices=Status,default=0)
    def __str__(self):
        return self.content[:17]
    
 #观点：赞成， 反对
 # 一篇文章，我可以给它点赞，也可以给它反对；
# 重复点击赞同和反对则是取消赞同和反对；
# 每个回答都可以让很多人，除了自己；
# 一个人可以对每个回答持不同观点；
# 从第三条和第四条可以得到，一个观点只属于一个回答，一个回答可以有多个观点，所以是一对多关系；
# 一个观点只属于一个User，但是一个User对不同的文章有不同的观点，所以观点和User也是一对多的关系；   
class Attitude(models.Model):
    Attitude = ((-1,"反对"),(0,"没表态"),(1,"赞成"))
    attitude = models.IntegerField(choices=Attitude, default=0)
    user = models.ForeignKey(to=User, related_name="user_attitudes", on_delete=models.CASCADE)
    answer = models.ForeignKey(to=Answer, related_name="answer_attitudes", on_delete=models.CASCADE)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    def __str__(self):
        return self.attitude
    
# 评论：属于哪个回答（一对多，这属多的那方）、属于哪个用户（一对多，这属多的那方）、内容、时间
# 回复：回复的评论/回复[这个怎么写？？]，指定用户（不指定）
class Comment(models.Model):
    answer = models.ForeignKey(to=Answer,related_name="comments", on_delete=models.CASCADE) 
    author = models.ForeignKey(to=User,related_name="comments", on_delete=models.CASCADE) 
    content = models.TextField(default="") 
    create_time = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    reply = models.ForeignKey(to=User,null=True,blank=True, on_delete=models.CASCADE)
    #  __str__ 设置展示在admin后台的是什么。
    def __str__(self):
        return self.author.username + self.content[:13]