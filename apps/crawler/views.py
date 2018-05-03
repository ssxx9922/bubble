from datetime import datetime
from xml import etree
from django.http import JsonResponse
from bs4 import BeautifulSoup as bs
from django.views import View
from information.models import information
from information.models import coin
from crawler.models import crawlState

import re
import requests
import time
import json
import threading

class CrawlerInfoView(View):
    def get(self,request):
        try:
            crawlObj = crawlInfo()
            crawlObj.crawler_run()

        except Exception as e:
            return JsonResponse({'error':e})
        else:
            return JsonResponse({'code': 'OK'})

class CrawlerCoinView(View):
    def get(self,request):
        try:
            crawlObj = crawlMarket()
            crawlObj.crawlerClockCC()
        except Exception as e:
            return JsonResponse({'error':e})
        else:
            return JsonResponse({'code':'OK'})


class baseCrawl(object):
    def crawlState(self,name,isSuccess,note,time):
        state = 'success' if isSuccess == True else 'failure'
        crawlState.objects.create(target=name, state=state, note=note, completetime=time)

    def get_data(self,url,cookies=None):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
            response = requests.get(url, headers=headers,timeout=10,cookies=cookies)
            if response.status_code == 200:
                return response
            else:
                return None
        except Exception as e:
            print('Crawling Failed', url)
            return None

    def afterInfoTime(self,infotime):
        cur_time = time.mktime(datetime.now().timetuple())

        per_infotime = datetime.strptime(infotime, '%Y-%m-%d %H:%S:%M')
        per_time = time.mktime(per_infotime.timetuple())

        if cur_time - per_time < 0:
            infotime = datetime.fromtimestamp(int(per_time-3600*24))
        return infotime


class crawlInfo(baseCrawl):
    def crawler_run(self):
        t1 = threading.Thread(target=self.crawler_bshijie)
        t2 = threading.Thread(target=self.crawler_jinse)
        t3 = threading.Thread(target=self.crawler_wallstreetcn)
        t4 = threading.Thread(target=self.crawler_biknow)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()

    def crawler_bshijie(self):
        response = self.get_data('http://www.bishijie.com/api/news')
        if response:
            result = json.loads(response.text)
            for date in dict(result['data']).keys():
                list = result['data'][date]['buttom']
                for r in list:
                    info = r['content'].strip()
                    infoid = 'BSJ-' + str(r['newsflash_id'])
                    infotime = datetime.fromtimestamp(r['issue_time'])
                    self.save_obj(info, infoid, infotime, 'bishijie')

    def crawler_jinse(self):
        response_home = self.get_data('http://www.jinse.com/lives')
        response = self.get_data('http://api.jinse.com/v4/live/list?limit=20', response_home.cookies)
        if response:
            result = json.loads(response.text)
            for r in result['list']:
                for item in r['lives']:
                    info_id = 'JS-' + str(item['id'])
                    info_time = datetime.fromtimestamp(item['created_at'])
                    info = item['content']
                    self.save_obj(info,info_id,info_time,'jinse')

    def crawler_wallstreetcn(self):
        response = self.get_data('http://api-prod.wallstreetcn.com/apiv1/content/lives/pc?limit=20')
        if response:
            result = json.loads(response.text)
            for item in result['data']['blockchain']['items']:
                infoid = 'HRJ' + str(item['id'])
                info_time = datetime.fromtimestamp(item['display_time'])
                info = item['content_text'].strip()
                self.save_obj(info,infoid,info_time,'wallstreetcn')


    def crawler_biknow(self):
        response = self.get_data('http://www.biknow.com')
        if response:
            response.encoding = 'utf-8'
            result = bs(response.text, 'lxml').find('ul', id='jiazai')
            date = datetime.now().strftime('%Y-%m-%d ')
            for item in result.find_all('li'):
                infoid = 'BZD-' + item.find('p', class_='kuaixunconr').find('a').get('href')[17:]
                crawl_time = date + item.find('p', class_='kuaixunconl').get_text().strip() + ':00'
                info_time = self.afterInfoTime(crawl_time)
                info = item.find('p', class_='kuaixunconr').find('a').get_text().strip()
                self.save_obj(info, infoid, info_time, 'biknow')

    def save_obj(self, info, infoid, infotime, author):
        if information.objects.filter(infoid=infoid):
            pass
        else:
            information.objects.create(info=self.infoToRe(info), infoid=infoid, infotime=infotime, author=author)

    def infoToRe(self,info):
        info = re.sub('\n', '', info)
        info = re.sub('\[查看原文\]', '', info)
        info = re.sub('\.\.\.', '', info)
        info = re.sub('【消息来源:biknow.com】','',info)
        infore = re.match('^【.*?】', info)
        return info if infore != None else '【快讯】' + info

class crawlMarket(baseCrawl):
    def crawlerFeixiaohao(self):
        response = self.get_data('http://www.feixiaohao.com')

        html = etree.HTML(response.text)
        tbody = html.xpath('//*[@id="table"]/tbody/tr')
        for item in tbody:
            id = item.xpath('@id')[0]
            name = item.xpath('td[2]/a/img/@alt')[0]
            marketValue = item.xpath('td[3]/text()')[0]
            price = item.xpath('td[4]/a/text()')[0]
            circulation = item.xpath('td[5]/text()')[0]
            self.save_obj(id,name,name,price,circulation,marketValue,'','','','FXH')

    def crawlerClockCC(self):
        response = self.get_data('http://block.cc/api/v1/coin/list?page=0&size=100')
        result = json.loads(response.text)

        if len(result['data']['list']) != 100:
            return

        save_list = []

        for i,item in enumerate(result['data']['list']):
            noNum = i
            coinId = item.get('id')
            eName = item.get('name')
            name = item.get('zhName')
            symbol = item.get('symbol')
            price = item.get('price')
            volume_ex = item.get('volume_ex')
            marketCap = item.get('marketCap')

            change1h = item.get('change1h')
            change1d = item.get('change1d')
            change7d = item.get('change7d')

            if name == None or name == '':
                name = eName

            new_coin = coin(coinId=coinId, name=name, symbol=symbol, price=price, volume_ex=volume_ex,
                            marketCap=marketCap,change1h=change1h,change1d=change1d,change7d=change7d,no=noNum,crawlfrom='BLOCK')

            save_list.append(new_coin)

        coin.objects.bulk_create(save_list)




