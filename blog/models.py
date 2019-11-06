# -*- coding: UTF-8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models

is_authenticated = True
is_active = True
is_anonymous = False


# Create your models here.
# 用户类型
# 采用的继承方式扩展用户信息
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/%Y%m', default='avatar/default.png', max_length=200, blank=True,
                               null=True)
    qq = models.CharField(max_length=11, blank=True, null=True, verbose_name='QQ号码')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 'User'
        ordering = ['-id']  # 对象的默认顺序

    def __unicode__(self):
        return self.username


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名', )

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        db_table = 'Tag'

    def __unicode__(self):
        return self.name  # 字符串类型


# 分类
class Catagory(models.Model):  # 按类型
    name = models.CharField(max_length=30, verbose_name='分类名称')
    index = models.IntegerField(default='999', verbose_name='分类的排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        db_table = 'Catagory'
        ordering = ['index', 'id']  # 先按照index排序, 如果一样就按id排序，正负表示从小到大，从大到小

    def __unicode__(self):
        return self.name


# 自定义一个文章Model的管理器
# 1、新加一个数据处理方法
# 2、改变原有的queryset
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish').order_by('-date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m') + '文章'
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list


# 文章
class Article(models.Model):
    title = models.CharField(max_length=30, verbose_name='文章标题')
    desc = models.CharField(max_length=50, verbose_name='文章描述')
    content = models.TextField(verbose_name='文章内容')
    click_count = models.IntegerField(default=0, verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, on_delete=True, verbose_name='用户')
    category = models.ForeignKey(Catagory, on_delete=True, verbose_name='分类')
    tag = models.ForeignKey(Tag, on_delete=True, verbose_name='标签')

    objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        db_table = 'Article'
        ordering = ['-date_publish']

    def __unicode__(self):
        return self.title


# 评论模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    user = models.ForeignKey(User, on_delete=True, blank=True, null=True, verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=True, blank=True, null=True, verbose_name='文章')
    pid = models.ForeignKey('self', on_delete=True, blank=True, null=True, verbose_name='父级评论', default=0)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        db_table = 'Comment'
        ordering = ['-date_publish']

    def __unicode__(self):
        return str(self.id)


# 友情链接
class Links(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    description = models.CharField(max_length=200, verbose_name='友情链接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        db_table = 'Links'
        ordering = ['-index', 'id']

    def __unicode__(self):
        return self.title


# 广告
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='广告标题')
    description = models.CharField(max_length=200, verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y%m', verbose_name='图片路径')
    callback_url = models.URLField(null=True, blank=True, verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    index = models.IntegerField(default=999, verbose_name='排序顺序(从小到大)')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        db_table = 'Ad'
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.title
