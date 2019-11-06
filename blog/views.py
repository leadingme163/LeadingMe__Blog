# -*- coding: UTF-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from blog.models import *
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
def global_settings(request):
    # 站点基本信息
    PER_NAME = settings.PER_NAME,
    PER_DESC = settings.PER_DESC,
    # 分类信息获取(导航数据)
    category_list = Catagory.objects.all()
    # 广告数据
    # 标签云数据
    tag_list = Tag.objects.all()
    # 友情链接
    # 文章归档的数据
    archive_list = Article.objects.distinct_date()
    # 点击量排行
    click_list = Article.objects.all().order_by('-click_count')[:6]
    # 最新文章排行
    publish_list = Article.objects.all().order_by('-date_publish')[:6]
    # 推荐文章排行(按发布日期)
    recommend_list = Article.objects.all().filter(is_recommend=True).order_by('-date_publish')[:6]
    # 图文推荐排行(按点赞量)
    imageText_list = Article.objects.all().filter(is_recommend=True).order_by('-click_count')[:3]
    # 标题导航分类
    nav_list = Catagory.objects.all()[:5]
    # 广告推荐
    ad_list = Ad.objects.all()[:4]
    return locals()


def index(request):
    try:
        # 最新文章数据
        article_list = Article.objects.all()
        article_list = getPage(request, article_list)
    except Exception as e:
        print(e)
    return render(request, 'index.html', locals())  # locals将返回所有的页面变量


def archive(request):
    try:
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(date_publish__icontains=year + '-' + month)  # i或略大写,contains模糊查询
        article_list = getPage(request, article_list)
    except Exception as e:
        print(e)
    return render(request, 'archive.html', locals())


def getPage(request, article_list):
    paginator = Paginator(article_list, 5)  # 传入查询的文章列表，每页3条文章
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)  # 分页器将返回传入的页数的3条数据
    except(EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)  # 如果是错误页数信息，默认返回第一页
    return article_list


def tagCloud(request):
    try:
        tag_id = request.GET.get('tag_id')
        tag = Tag.objects.get(id=tag_id)
        article_list = tag.article_set.all()
        article_list = getPage(request, article_list)
    except Exception as e:
        print(e)
    return render(request, 'tagCloud.html', locals())


def notOpen(request):
    return render(request, 'NotOpen.html')


def notAd(request):
    return render(request, 'NotAd.html')


def register(request):
    article = request.GET.get('article')
    return render(request, 'register.html', locals())


def doRegister(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    article_id = request.POST.get('article')
    newUser = User.objects.create(username=username, password=make_password(password, None, 'pbkdf2_sha256'))
    newUser.save()
    return HttpResponseRedirect('/blog_content/?article_id=' + article_id)


def login(request):
    request.session.clear()
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        article_id = request.POST.get('article_id')
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            content = {
                'article_id': article_id,
                'tip': '登录状态！',
                'username': user.username,
                'password': user.password,
                'userId': user.id,
            }
            request.session['user'] = content
    except Exception as e:
        print(e)
    return HttpResponseRedirect('/blog_content/?article_id=' + article_id)


def out(request):
    try:
        article_id = request.session.get('user')['article_id']
        request.session.clear()
        tip = '未登录状态！'
        return HttpResponseRedirect('/blog_content/?article_id=' + article_id)
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/')





def blog_content(request):
    try:
        article_id = request.GET.get('article_id')  # 获取文章id
        try:
            username = request.session.get('user')['username']
            password = request.session.get('user')['password']
            tip = request.session.get('user')['tip']
        except Exception as e:
            print(e)
        try:
            article = Article.objects.get(id=article_id)  # 获取文章信息
        except Article.DoesNotExist:
            print('没有找到相应文章！')

        # 评论表单
        comment_form = {
            'author': request.user.username,
            'article': article_id
        }

        # 本文章的所有评论
        comments = Comment.objects.filter(article=article_id).order_by('id')
        # 存所有pid=0
        comment_list = []

        for comment in comments:
            if comment.pid_id is None:
                setattr(comment, 'children_comment', [])
                comment_list.append(comment)
            for item in comment_list:
                if comment.pid_id is not None:
                    if item.id == comment.pid_id:
                        item.children_comment.append(comment)
                    else:
                        continue
    except Exception as e:
        print(e)
    return render(request, 'blogContent.html', locals())


def relay(request):
    try:
        comment = request.POST.get('comment')
        article_id = request.POST.get('article_id')
        comment_id = request.POST.get('comment_id')
        user_id = request.session.get('user')['userId']
        newComment = Comment.objects.create(content=comment, article_id=article_id, pid_id=comment_id, user_id=user_id)
        newComment.save()
    except Exception as e:
        print(e)
    return HttpResponseRedirect('/blog_content/?article_id=' + article_id)


def report(request):
    try:
        comment = request.POST.get('comment')
        article_id = request.POST.get('article_id')
        user_id = request.session.get('user')['userId']
        newComment = Comment.objects.create(content=comment, article_id=article_id, pid_id=None, user_id=user_id)
        newComment.save()
    except Exception as e:
        print(e)
    return HttpResponseRedirect('/blog_content/?article_id=' + article_id)