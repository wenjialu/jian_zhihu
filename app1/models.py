from django.db import models
from django.contrib.auth.models import User, AbstractUser

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