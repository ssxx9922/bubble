from datetime import datetime
import time
import json
import requests

from django.http import JsonResponse
from bs4 import BeautifulSoup as bs
from django.views import View
from information.models import information,coin
from crawler.models import crawlState
from lxml import etree

class CrawlerInfoView(View):
    def get(self,request):
        try:
            crawlObj = crawlInfo()
            crawlObj.crawlerBshijie()
            crawlObj.crawlerJinse()
            crawlObj.crawlerWallstreetcn()
            crawlObj.crawlerBiknow()
        except Exception as e:
            return JsonResponse({'error':e})
        else:
            return JsonResponse({'code': 'OK'})

class CrawlerCoinView(View):
    def get(self,request):
        try:
            crawlObj = crawlMarket()
            crawlObj.crawlerFeixiaohao()
        except Exception as e:
            return JsonResponse({'error':e})
        else:
            return JsonResponse({'code':'OK'})


class baseCrawl(object):
    def crawlState(self,name,isSuccess,note,time):
        state = 'success'if isSuccess == True else 'success'
        crawlState.objects.create(target=name, state=state, note=note, completetime=time)

    def getData(self,url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
            start = time.clock()
            response = requests.get(url, headers=headers,timeout=10)
            end = time.clock()
            if response.status_code == 200:
                self.crawlState(url, True, str(response.status_code), '%f' %(end - start))
                return response
            else:
                self.crawlState(url, False, str(response.status_code),'')
                return None
        except Exception as e:
            print('Crawling Failed', url)
            self.crawlState(url,False,e)
            return None

    def afterInfoTime(self,infotime):
        cur_time = time.mktime(datetime.now().timetuple())

        per_infotime = datetime.strptime(infotime, '%Y-%m-%d %H:%S:%M')
        per_time = time.mktime(per_infotime.timetuple())

        if cur_time - per_time < 0:
            infotime = datetime.fromtimestamp(int(per_time-3600*24))
        return infotime


class crawlInfo(baseCrawl):
    def crawlerBshijie(self):
        response = self.getData('http://www.bishijie.com/api/news')
        result = json.loads(response.text)
        for date in dict(result['data']).keys():
            list = result['data'][date]['buttom']
            for r in list:
                info = r['content'].strip()
                infoid = 'BSJ-' + str(r['newsflash_id'])
                infotime = datetime.fromtimestamp(r['issue_time'])
                self.saveObj(info, infoid, infotime, 'bishijie')

    def crawlerJinse(self):
        response = self.getData('http://www.jinse.com/lives')
        result = bs(response.text, 'lxml').find_all('li', class_='clearfix ')
        date_id = bs(response.text, 'lxml').find('ul', class_='lost').get('id')
        date = datetime.now().strftime('%Y-%m-%d ')
        for r in result:
            infoid = '' + date_id[5:] + '-' + r.get('data-id').strip()
            time = date + r.find('p', class_='live-time').get_text().strip() + ':00'
            infotime = self.afterInfoTime(time)
            info = r.find('div', class_='live-info').get_text().strip()
            self.saveObj(info,infoid,infotime,'jinse')

    def crawlerWallstreetcn(self):
        response = self.getData('http://api-prod.wallstreetcn.com/apiv1/content/lives/pc?limit=20')
        result = json.loads(response.text)
        for item in result['data']['blockchain']['items']:
            infoid = 'HRJ' + str(item['id'])
            infotime = datetime.fromtimestamp(item['display_time'])
            info = item['content_text'].strip()
            self.saveObj(info,infoid,infotime,'wallstreetcn')

    def crawlerBiknow(self):
        response = self.getData('http://www.biknow.com')
        response.encoding = 'utf-8'
        result = bs(response.text, 'lxml').find('ul', id='jiazai')
        date = datetime.now().strftime('%Y-%m-%d ')
        for item in result.find_all('li'):
            infoid = 'BZD-' + item.find('p', class_='kuaixunconr').find('a').get('href')[17:]
            time = date + item.find('p', class_='kuaixunconl').get_text().strip() + ':00'
            infotime = self.afterInfoTime(time)
            info = item.find('p', class_='kuaixunconr').find('a').get_text().strip()
            self.saveObj(info, infoid, infotime, 'biknow')

    def saveObj(self, info, infoid, infotime, author):
        if information.objects.filter(infoid=infoid):
            pass
        else:
            information.objects.create(info=info, infoid=infoid, infotime=infotime, author=author)


class crawlMarket(baseCrawl):
    def crawlerFeixiaohao(self):
        response = self.getData('http://www.feixiaohao.com')

        html = etree.HTML(response.text)
        tbody = html.xpath('//*[@id="table"]/tbody/tr')
        for item in tbody:
            id = item.xpath('@id')[0]
            image = 'http:' + item.xpath('td[2]/a/img/@src')[0]
            name = item.xpath('td[2]/a/img/@alt')[0]
            marketValue = item.xpath('td[3]/text()')[0]
            price = item.xpath('td[4]/a/text()')[0]
            circulation = item.xpath('td[5]/text()')[0]
            self.saveObj(id,image,name,marketValue,price,circulation,'FXH')


    def saveObj(self,id,image,name,marketValue,price,circulation,crawlFrom):
        coin.objects.create(coinId=id, image=image, name=name, marketValue=marketValue, price=price,
                            circulation=circulation,crawlfrom=crawlFrom)



