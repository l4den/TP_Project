from django.shortcuts import render
from .models import Shop
from workingtimes.models import WorkingTime
from services.models import Service


def shops_page(request):
    context = {'shops': Shop.objects.all()}
    return render(request, 'shops/partners.html', context)


def shop_details_page(request, id):
    shop = Shop.objects.get(id=id)
    times = WorkingTime.objects.filter(shop=shop)
    services = Service.objects.filter(shop=shop)
    context = {'shop': shop, 'times': times, 'services': services}
    return render(request, 'shops/shop_details.html', context)