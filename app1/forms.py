from django import forms

# 前端表单传值到后端IssueForm
# 前端输入框的name字段设置成对应的form字段名称，必须保持一致，
# 这样初始化IssueForm的时候，IssueForm可以主动识别出表单中对应的字段和数据。
class IssueForm(forms.Form):
    # id = forms.IntegerField(required = False)
    title = forms.CharField(max_length=128)
    description = forms.CharField(required=False)
    anonymity = forms.BooleanField(required=False)

# 前端表单传值到后端AnswerForm
 #对应前端（前端表单里面有标题、描述、匿名提问的三个输入框），一一对应表单的name写form
class AnswerForm(forms.Form):
    # 如果通过url传id的话，前端表单就不需要接收这个值了。
    # issue_id = forms.IntegerField(required = False)
    answer = forms.CharField(strip = False)
    anonymity = forms.BooleanField(required = False)
    

# 1 view 中从模型类Issue中get所有的Issue对象 赋值给issue，通过render渲染到前端。
# 2 前端拿到issue，获取自带的id和属性title 并展示。
# 3 用户选择了对应的issue后，赋值给表单value = form.id。传值到后端AnswerForm的issue_id。
# 4 view中拿到issue_id 并赋值给 issue_id
# 5 从模型类Issue中get对应id的issue对象，赋值给Answer 模型类。
# Q： 前端 name="issue" 对应的是表单还是传入的kmap 还是都要对应？？？？？
# A: <select name="issue">	{% for i in issues %}
# A: 前端form中name对应后端form， 前端代码部分{{}}对应传入的kmap。

# 好像外键就不用设定.设置一下除外键外的属性。
class CommentForm(forms.Form):
    content = forms.CharField(min_length=1)