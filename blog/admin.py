from django.contrib import admin
from blog.models import *


# Register your models here.

class ArticleAdmin(admin.ModelAdmin):  # 引入富文本编辑器
    list_display = ['id', 'title', 'click_count', 'is_recommend', 'date_publish', 'user', 'category', 'tag']

    class Media:
        js = (
            '/static/kindeditor/kindeditor-all.js',  # 引入富文本js代码
            '/static/kindeditor/lang/zh-CN.js',  # 引入中文包
            '/static/kindeditor/config.js',  # 引入配置文件
        )


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_superuser']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class CatagoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'index']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'date_publish', 'user', 'article', 'pid']


class LinksAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'callback_url', 'index']


class Adadmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image_url', 'callback_url', 'date_publish', 'index']


class MyAdminSite(admin.AdminSite):
    site_header = 'Leadingme的个人博客'  # 此处设置页面显示标题
    site_title = '博客管理'  # 此处设置页面头部标题


admin.site = MyAdminSite(name='management')
admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Catagory, CatagoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Links, LinksAdmin)
admin.site.register(Ad, Adadmin)
