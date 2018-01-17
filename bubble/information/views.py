import json
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import JsonResponse

from . import models
# Create your views here.


def list(request):
    list = models.information.objects.values('info', 'infotime', 'infoid', 'favour', 'disfavor').order_by('-infotime')
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
        dict_list.append({'id':item['infoid'],
                          'text':item['info'],
                          'favour':item['favour'],
                          'disfavor':item['disfavor'],
                          'time':item['infotime'].strftime('%Y-%m-%d %H:%M:%S')})

    return JsonResponse({'code':'OK',
                         'data':{'page':info_list.num_pages,
                                 'list':dict_list}})

def interact(request):

    id = request.GET.get('id')
    type = request.GET.get('type')

    if id is None or type is None:
        return JsonResponse({'error':'参数错误'})

    obj = models.information.objects.filter(infoid=id)
    if obj.count() == 0:
        return JsonResponse({'error':'ID错误'})

    if type == 'favour':
        obj.update(favour=obj.first().favour + 1)
        return JsonResponse({'code': 'OK'})
    elif type == 'disfavor':
        obj.update(disfavor=obj.first().disfavor + 1)
        return JsonResponse({'code': 'OK'})
    else:
        return JsonResponse({'error':'数据错误'})


def crawler(request):
    # try:
    crawlerBshijie()
    crawlerJinse()
    # except:
    #     return JsonResponse({'error':'爬取失败'})

    return JsonResponse({'code':'OK'})

def crawlerBshijie():
    response = requests.get('http://www.bishijie.com/api/news')
    result = json.loads(response.text)
    date = datetime.now().strftime('%Y-%m-%d')
    list = result['data'][date]['buttom']
    for r in list:
        info = r['content']
        infoid = r['newsflash_id']
        infotime = datetime.fromtimestamp(r['issue_time'])
        saveObj(info, infoid, infotime,'http://www.bishijie.com/api/news')

def crawlerJinse():
    response = requests.get('http://www.jinse.com/lives')
    result = bs(response.text, 'lxml').find_all('li', class_='clearfix ')
    date_id = bs(response.text, 'lxml').find('ul', class_='lost').get('id')
    date = datetime.now().strftime('%Y-%m-%d ')
    for r in result:
        infoid = date_id + '-' + r.get('data-id').strip()
        time = r.find('p', class_='live-time').get_text().strip() + ':00'
        infotime = date + time
        info = r.find('div', class_='live-info').get_text().strip()
        saveObj(info,infoid,infotime,'http://www.jinse.com/live')


def saveObj(info,infoid,infotime,author):
    list = models.information.objects.filter(infoid=infoid)
    if list.count() == 0:
        models.information.objects.create(info=info, infoid=infoid, infotime=infotime, author=author)