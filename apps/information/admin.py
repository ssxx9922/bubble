from django.contrib import admin

# Register your models here.
from information.models import information, coin

class informationAdmin(admin.ModelAdmin):
    list_display = ('info','author','infotime','favour','disfavor')

admin.site.register(information,informationAdmin)



class coinAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'marketCap', 'price', 'change1h', 'change1d', 'change7d')

admin.site.register(coin,coinAdmin)