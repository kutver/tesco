from django.db import models
from bs4 import BeautifulSoup
import requests

class Scrap(models.Model):

    url_category_list = 'https://www.tesco.com/groceries/en-GB'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    
    def get_page_content(self, url):
        page = requests.get(url, headers = {'user-agent':self.user_agent})
        return BeautifulSoup(page.content, 'html.parser')

    def scrap_categories(self):
        page = self.get_page_content(self.url_category_list)
        categories = page.find_all("ul", {"class":"menu menu-superdepartment"})
        results = []

        for category in categories:
            elements = category.find_all("a", href=True)

            for element in elements:
                title = str(element.contents[0]).replace('<span><span class="visually-hidden">Shop</span>', '')
                title = title.replace('<span class="visually-hidden">department</span></span>', '')
                url = str(element['href']).replace('/groceries/en-GB/shop/', '')
                url = url.replace('?include-children=true', '')

                results.append({'title':title, 'url':url}) 

        return results

    def scrap_products(self, category, second_category, third_category, page):

        if second_category and third_category == 'None':      
            source_page = self.get_page_content(f'https://www.tesco.com/groceries/en-GB/shop/{category}/all?page={page}')

        if second_category != 'None' and third_category == 'None':
            source_page = self.get_page_content(f'https://www.tesco.com/groceries/en-GB/shop/{category}/{second_category}/all?page={page}')

        if second_category and third_category != 'None':
            source_page = self.get_page_content(f'https://www.tesco.com/groceries/en-GB/shop/{category}/{second_category}/{third_category}?page={page}')

        products = source_page.find_all("div", {"class":"tile-content"})

        results = []
        
        for product in products:
            url_and_title = product.find('a', {'class': 'sc-fzqNqU kikdAh'})
            title = url_and_title.contents[0]
            url = 'https://www.tesco.com'+url_and_title['href']
            try:
                currency_price_quantity_weight = product.find('div', {'class': 'price-per-quantity-weight'}).contents[0]
                price_unit = product.find('div', {'class': 'price-per-sellable-unit price-per-sellable-unit--price price-per-sellable-unit--price-per-item'}).contents[0]
                price_unit = price_unit.find('span', {'class': 'value'}).text
                currency = currency_price_quantity_weight.find('span', {'class': 'currency'}).text
                price_quantity = currency_price_quantity_weight.find('span', {'class': 'value'}).text
                weight = product.find('div', {'class': 'price-per-quantity-weight'}).contents[1].text                 
            except:
                currency = "Not available."
                price_quantity = "Not available."
                price_unit = "Not available."
                weight = ""

            results.append({'url': url, 'title': title, 'currency': currency, 'price_unit': price_unit, 'price_quantity': price_quantity, 'weight': weight})
        
        return results

    def search_by_url(self, url):
        print(url)        
        source_page = self.get_page_content(url)
        print(source_page)

    def find_category_depth(self, url):
        url_parts = url.split('/')        

        if len(url_parts) == 7:
            category_depth = 1
        if len(url_parts) == 8:
            category_depth = 2
        if len(url_parts) == 9:
            category_depth = 3

        if url_parts[-1].startswith('all') and category_depth > 1:
            category_depth = category_depth - 1

        if url_parts[-1].find("page=") != -1:
            page = url_parts[-1].split("page=",1)[1]
        else:
            page = 1

        category = None
        second_category = None
        third_category = None

        if category_depth >= 1:
            category = url_parts[6]
        if category_depth >= 2:
            second_category = url_parts[7]
        if category_depth >= 3:
            third_category = url_parts[8].split('?', 1)[0]
        
        return {'category': category, 'second_category': second_category, 'third_category': third_category, 'page': page}
