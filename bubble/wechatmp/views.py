import hashlib

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from wechatmp.WXBizMsgCrypt import WXBizMsgCrypt


def verify(request):
    try:
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')

        token = 'bibibi8wechat'

        sortlist = [token, timestamp, nonce]
        sortlist.sort()
        sha = hashlib.sha1()
        sha.update(("".join(sortlist)).encode("utf8"))
        hashcode = sha.hexdigest()

        if hashcode == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('')
    except Exception as e:
        return e