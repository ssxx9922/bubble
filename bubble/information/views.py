import json
from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import time
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from django.views import View

from . import models
# Create your views here.


class ListView(View):
    def get(self,request):
        list = models.information.objects.values('info', 'author', 'infotime', 'id', 'favour', 'disfavor').order_by('-infotime')
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
            dict_list.append({'id':item['id'],
                              'text':item['info'],
                              'favour':item['favour'],
                              'disfavor':item['disfavor'],
                              'author': item['author'],
                              'time':item['infotime'].strftime('%Y-%m-%d %H:%M:%S')})

        return JsonResponse({'code':'OK',
                             'data':{'page':info_list.num_pages,
                                     'list':dict_list}})

class InteractView(View):
    def get(self,request):
        id = request.GET.get('id')
        type = request.GET.get('type')

        if id is None or type is None:
            return JsonResponse({'error':'参数错误'})

        obj = models.information.objects.filter(id=id)
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

class CrawlerView(View):
    def get(self,request):
        try:
            crawlerBshijie()
            crawlerJinse()
            crawlerWallstreetcn()
            crawlerBiknow()
        except Exception as e:
            return JsonResponse({'error':e})

        return JsonResponse({'code':'OK'})

def crawlerBshijie():
    response = requests.get('http://www.bishijie.com/api/news')
    result = json.loads(response.text)
    for date in dict(result['data']).keys():
        list = result['data'][date]['buttom']
        for r in list:
            info = r['content']
            infoid = 'BSJ-' + str(r['newsflash_id'])
            infotime = datetime.fromtimestamp(r['issue_time'])
            saveObj(info, infoid, infotime,'bishijie')

def crawlerJinse():
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    response = requests.get('http://www.jinse.com/lives',headers=headers)
    result = bs(response.text, 'lxml').find_all('li', class_='clearfix ')
    date_id = bs(response.text, 'lxml').find('ul', class_='lost').get('id')
    date = datetime.now().strftime('%Y-%m-%d ')
    for r in result:
        infoid = date_id[5:] + '-' + r.get('data-id').strip()
        time = r.find('p', class_='live-time').get_text().strip() + ':00'
        infotime = date + time
        infotime = afterInfoTime(infotime)
        info = r.find('div', class_='live-info').get_text().strip()
        saveObj(info,infoid,infotime,'jinse')

def afterInfoTime(infotime):
    cur_time = time.mktime(datetime.now().timetuple())

    per_infotime = datetime.strptime(infotime, '%Y-%m-%d %H:%S:%M')
    per_time = time.mktime(per_infotime.timetuple())

    if cur_time - per_time < 0:
        infotime = datetime.fromtimestamp(int(per_time-3600*24))

    return infotime


def crawlerWallstreetcn():
    response = requests.get('http://api-prod.wallstreetcn.com/apiv1/content/lives/pc?limit=20')
    result = json.loads(response.text)
    for item in result['data']['blockchain']['items']:
        infoid = str(item['id'])
        infotime = datetime.fromtimestamp(item['display_time'])
        info = item['content_text'].strip()
        saveObj(info,infoid,infotime,'wallstreetcn')

def crawlerBiknow():
    response = requests.get('http://www.biknow.com')
    response.encoding = 'utf-8'
    result = bs(response.text, 'lxml').find('ul', id='jiazai')
    date = datetime.now().strftime('%Y-%m-%d ')
    for item in result.find_all('li'):
        infoid = 'BZD-' + item.find('p', class_='kuaixunconr').find('a').get('href')[17:]
        time = item.find('p', class_='kuaixunconl').get_text().strip() + ':00'
        infotime = date + time
        infotime = afterInfoTime(infotime)
        info = item.find('p', class_='kuaixunconr').find('a').get_text().strip()
        saveObj(info, infoid, infotime, 'biknow')


def saveObj(info,infoid,infotime,author):
    list = models.information.objects.filter(infoid=infoid)
    if list.count() == 0:
        models.information.objects.create(info=info.strip(), infoid=infoid, infotime=infotime, author=author)


sched = BackgroundScheduler()

@sched.scheduled_job('interval',seconds=630,id='job')
def autoCrawler():
    try:
        crawlerBshijie()
    except:
        send_mail('爬取失败', '币世界爬虫出现问题', 'ssxx9922@163.com', ['andy.shi@foxmail.com'], fail_silently=False)

    try:
        crawlerJinse()
    except:
        send_mail('爬取失败', '金色财经爬虫出现问题', 'ssxx9922@163.com', ['andy.shi@foxmail.com'], fail_silently=False)

    try:
        crawlerWallstreetcn()
    except:
        send_mail('爬取失败', '华尔街见闻爬虫出现问题', 'ssxx9922@163.com', ['andy.shi@foxmail.com'], fail_silently=False)

    try:
        crawlerBiknow()
    except:
        send_mail('爬取失败', '币知道爬虫出现问题', 'ssxx9922@163.com', ['andy.shi@foxmail.com'], fail_silently=False)

sched.start()