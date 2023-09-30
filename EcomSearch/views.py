from django.http import HttpResponse
from django.shortcuts import render
import urllib.parse
import requests
from bs4 import BeautifulSoup
import openpyxl

def About_us(request):
    return render(request,"about_us.html")

def index(request):
    if request.method == 'GET':
        product = request.GET.get('product')
        if product is not None and product:
            url1 = "https://www.amazon.in/s?k=" +product+ "&crid=2F1YXJKJO28UB&sprefix=t-shirts%2Caps%2C337&ref=nb_sb_noss_1"
            url2 = "https://www.flipkart.com/search?q=" +product+ "&otracker=search&otracker1=search&marketplace=FLIPKART&as-show="
            url3 = "https://www.snapdeal.com/search?clickSrc=top_searches&keyword=" +product+ "&categoryId=0&vertical=p&noOfResults=20&SRPID=topsearch&sort=rlvncy"


            HEADERS = HEADERS = ({ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",})

            page1 = requests.get(url1,headers=HEADERS)
            page2 = requests.get(url2,headers=HEADERS)
            page3 = requests.get(url3,headers=HEADERS)


            soup1 = BeautifulSoup(page1.content, 'html.parser' )
            soup2 = BeautifulSoup(page2.content, 'html.parser' )
            soup3 = BeautifulSoup(page3.content, 'html.parser' )

            amazon_div_elements = soup1.find_all('div', class_='s-result-item')
            amazon_product_imgs = []
            amazon_product_descriptions = []
            amazon_product_prices = []
            amazon_product_ratings = []
            amazon_product_links = []

            flipkart_div_elements = soup2.find_all('div' ,class_='_1xHGtK _373qXS')    
            flipkart_product_imgs = []
            flipkart_product_descriptions = []
            flipkart_product_prices = []
            flipkart_product_links = []

            snapdeal_div_elements = soup3.find_all('div' ,class_='col-xs-6 favDp product-tuple-listing js-tuple') 
            snapdeal_product_imgs = []
            snapdeal_product_descriptions = []
            snapdeal_product_prices = []
            snapdeal_product_links = []

            for div in amazon_div_elements:
                img = div.find('img', class_='s-image')
                product_img = img['src'] if img else ""

                description = div.find('span', class_='a-size-base-plus a-color-base a-text-normal')
                product_des = description.get_text(strip=True) if description else ""

                price = div.find('span', class_='a-price-whole')
                product_price = price.get_text(strip=True) if price else ""

                rating = div.find('span', class_='a-icon-alt')
                product_rating = rating.get_text(strip=True) if rating else ""

                link = div.find(class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
                if link is not None:
                    link = link['href']
                    link = urllib.parse.unquote(link)
                    product_link = "https://www.amazon.in" + link
                else:
                    link2 = ""

                if not product_img or not product_des or not product_price or not link:
                    continue

                amazon_product_imgs.append(product_img)
                amazon_product_descriptions.append(product_des)
                amazon_product_prices.append(product_price)
                amazon_product_ratings.append(product_rating)
                amazon_product_links.append(product_link)

            for div in flipkart_div_elements:
                img = div.find('img', class_='_2r_T1I')
                product_img = img['src'] if img else ""

                description = div.find('a', class_='IRpwTa')
                product_des = description.get_text(strip=True) if description else ""

                price = div.find('div', class_='_30jeq3')
                product_price = price.get_text(strip=True) if price else ""

                link = div.find('a', class_='_2UzuFa')
                product_link = "https://www.flipkart.com"+link['href']

                if not product_img or not product_des or not product_price:
                    continue
                flipkart_product_imgs.append(product_img)
                flipkart_product_descriptions.append(product_des)
                flipkart_product_prices.append(product_price)
                flipkart_product_links.append(product_link)

            for div in snapdeal_div_elements:
                img = div.find(class_='picture-elem')
                product_img = img.source['srcset'] if img else ""

                description = div.find('p', class_='product-title')
                product_des = description.get_text(strip=True) if description else ""

                price = div.find('span', class_='lfloat product-price')
                product_price = price.get_text(strip=True) if price else ""

                link = div.find('a', class_='dp-widget-link')
                product_link = link['href']

                if not product_img or not product_des or not product_price:
                    continue
                snapdeal_product_imgs.append(product_img)
                snapdeal_product_descriptions.append(product_des)
                snapdeal_product_prices.append(product_price)
                snapdeal_product_links.append(product_link)
            product_site = []
            product_imgs = []
            product_descriptions = []
            product_prices = []
            product_links = []
            max_length = max(len(amazon_product_imgs), len(flipkart_product_imgs), len(snapdeal_product_imgs))
            for i in range(max_length):
                if i < len(amazon_product_imgs):
                    product_site.append("Amazon")
                    product_imgs.append(amazon_product_imgs[i])
                    product_descriptions.append(amazon_product_descriptions[i])
                    product_prices.append(amazon_product_prices[i])
                    product_links.append(amazon_product_links[i])
                if i < len(flipkart_product_imgs):
                    product_site.append("Flipcart")
                    product_imgs.append(flipkart_product_imgs[i])
                    product_descriptions.append(flipkart_product_descriptions[i])
                    product_prices.append(flipkart_product_prices[i])
                    product_links.append(flipkart_product_links[i])
                if i < len(snapdeal_product_imgs):
                    product_site.append("Snapdeal")
                    product_imgs.append(snapdeal_product_imgs[i])
                    product_descriptions.append(snapdeal_product_descriptions[i])
                    product_prices.append(snapdeal_product_prices[i])
                    product_links.append(snapdeal_product_links[i])

            # print(product_imgs)
            # print(product_descriptions)
            # print(product_prices)
            # print(product_links)
            new_list = []
            for item1, item2, item3, item4, item5 in zip(product_imgs, product_descriptions, product_prices, product_links, product_site):
                new_item = {'product_imgs': item1, 'product_descriptions': item2, 'product_prices': item3, 'product_links': item4, 'product_site': item5}
                new_list.append(new_item)

            # print(new_list)
            data = {
            'all_product': new_list,
            }

        else:
            data = {
            'all_product': '',
            }

            
    return render(request,"index.html", {"data": data})