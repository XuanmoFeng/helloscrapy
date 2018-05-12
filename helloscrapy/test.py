# from django.shortcuts import get_tempalte
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template.loader import get_template

from albumId.models import AlbumId


def test(request):
    response = ""
    response1 = ""
    t = get_template("test.html")
    lists = AlbumId.objects.get_queryset().order_by('id')
    paginator = Paginator(lists, 10)
    page = request.GET.get('page', 1)
    # 把当前的页码数转换成整数类型
    currentPage = int(page)
    try:
        lists = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        lists = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
        lists = paginator.page(paginator.num_pages)
    html = t.render(locals())
    return HttpResponse(html)


def index(request):
    t = get_template("footer.html")
    return HttpResponse(t.render())


def search(request):
    param = request.GET.get('singer')
    t = get_template("singer.html")
    return HttpResponse(t.render())


def commentor(request):
    t = get_template("commentor.html")
    return HttpResponse(t.render())


def comment(request):
    t = get_template("comment.html")
    return HttpResponse(t.render())