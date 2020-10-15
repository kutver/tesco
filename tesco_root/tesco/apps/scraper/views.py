from django.shortcuts import render, redirect
import csv
from django.http import HttpResponse
from django.views import View
from .models import Scrap
import datetime
import urllib.request

# Create your views here.
def index(request):
    categories = Scrap().scrap_categories()

    return render(request, 'scraper/index.html', {'categories': categories})

def details(request, category, second_category, third_category, page):
    categories = Scrap().scrap_categories()
    products = Scrap().scrap_products(category, second_category, third_category, page)

    return render(request, 'scraper/details.html', {'categories': categories, 'products': products, 'category':category, 'second_category': second_category, 'third_category': third_category, 'page': page})

def search_url(request):
    url = request.POST.get('url', '')
    results = Scrap().find_category_depth(url)

    return redirect('details', category=results['category'], second_category=results['second_category'], third_category=results['third_category'], page=results['page'])

def export(request, category, second_category, third_category, page):
    response = HttpResponse(content_type='text/csv')
    file_name = str(datetime.datetime.now())+'-'+category+'-'+second_category+'-'+third_category+'-page'+str(page)+'.csv'
    response['Content-Disposition'] = 'attachment; filename='+file_name

    writer = csv.writer(response)
    writer.writerow(['Title','URL','Unit Price','Quantity Price','Weight','Currency'])

    products = Scrap().scrap_products(category, second_category, third_category, page)
    for product in products:
        writer.writerow([product['title'], product['url'], product['price_unit'], product['price_quantity'], product['weight'], product['currency']])

    return response    
