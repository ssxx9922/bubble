from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

from django.views import View

from information.models import information,coin
# Create your views here.


class ListView(View):
    def get(self,request):
        list = information.objects.values('info', 'author', 'infotime', 'id', 'favour', 'disfavor').order_by('-infotime')
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
                              'time':item['infotime'].strftime('%Y-%m-%d %H:%M')})

        return JsonResponse({'code':'OK',
                             'data':{'page':info_list.num_pages,
                                     'list':dict_list}})

class InteractView(View):
    def get(self,request):
        id = request.GET.get('id')
        type = request.GET.get('type')

        if id is None or type is None:
            return JsonResponse({'error':'参数错误'})

        obj = information.objects.filter(id=id)
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

class coinOnly(View):
    def get(self,request):
        pass
        #TODO
        # coinId = request.GET.get('coinId')
        #
        # if coin.objects.filter(coinId=coinId):
        #     list = coin.objects.filter(coinId=coinId).order_by('-crawltime')
        #
        #     objs = Paginator(list, 1)
        #     print(objs)
        #     print(type(objs))
        #
        #     dict = {}
        #     for obj in objs:
        #         dict = {'id': obj['coinId'],
        #                 'image': obj['image'],
        #                 'name': obj['name'],
        #                 'marketValue': obj['marketValue'],
        #                 'price': obj['price'],
        #                 'circulation': obj['circulation'],
        #                 'crawlfrom': obj['crawlfrom']}
        #
        #     return JsonResponse({'code': 'OK',
        #                          'data': {'item': dict}})
        # else:
        #     return JsonResponse({'error': 'ID错误'})

class coinList(View):
    def get(self,request):
        pass
