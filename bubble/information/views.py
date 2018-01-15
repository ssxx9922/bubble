from django.core import paginator, serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import models
# Create your views here.


def list(request):
    list = models.information.objects.values('info', 'infotime').order_by('-infotime')
    info_list = Paginator(list, 20)

    page = request.GET.get('page')

    page = page if page is not None else 1

    try:
        contacts = info_list.page(page)
    except PageNotAnInteger:
        return JsonResponse({'error':'服务器出了问题'})
    except EmptyPage:
        return JsonResponse({'error':'没用更多数据了'})

    dict_list = []

    for item in contacts:
        dict_list.append({'text':item['info'],
                          'time':item['infotime'].strftime('%Y-%m-%d %H:%M:%S')})

    return JsonResponse({'page':info_list.num_pages,
                         'data':dict_list})

