import csv
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
print("TRY BEING AS SPECIFIC AS YOU CAN TO HELP YOU GIVE BEST RESULTS! FOR EG.: VIVO V21 8GB RAM 256GB STORAGE")
user_entered_name = input("enter the product name: ")

split = user_entered_name.split(' ')
x=''
y=''
for i in range(0,len(split)):  #this is a loop to make a string which will be accepted in the url of the websites
    x = x+'+'+split[i]
    y = y+'-'+split[i]

amazon_url = f"https://www.amazon.in/s?k={x}&ref=nb_sb_noss_2"
vijay_sales_url = f'https://www.vijaysales.com/search/{y[1:]}'
croma_url = f'https://www.croma.com/search/?text={x[1:]}'
flipkart_url = f'https://www.flipkart.com/search?q={x[1:]}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&sort=relevance'

print(amazon_url,vijay_sales_url,flipkart_url)
uClient = uReq(amazon_url) #opening up the connection
amazon_html = uClient.read() #grabbing the page data
uClient.close()

amazon_soup = soup(amazon_html, "html.parser") #html parsing
amazon_product_titles = amazon_soup.findAll("a",{"class":"a-link-normal a-text-normal"})  #finds all titles of products using the title's a tag

amazon_prices = amazon_soup.findAll("span",{"class":"a-price-whole"})  #finds all prices
amazon_database = [['amazon', ], ['amazon', ], ['amazon', ], ['amazon', ], ['amazon', ]]

uClient3 = uReq(vijay_sales_url) #opening up the connection
vijay_html = uClient3.read() #grabbing the page data
uClient3.close()

vijay_soup = soup(vijay_html, "html.parser") #html parsing
vijay_product_titles = vijay_soup.findAll("a",{"rel":"follow"})  #finds all titles of products using the title's a tag
vijay_prices = vijay_soup.findAll("div",{"class":"Dynamic-Bucket-vsp"})  #finds all prices
vijay_database = [['vijay',],['vijay',],['vijay',],['vijay',],['vijay',]]


uClient2 = uReq(flipkart_url) #opening up the connection
flipkart_html = uClient2.read() #grabbing the page data
uClient2.close()

flipkart_soup = soup(flipkart_html, "html.parser") #html parsing
flipkart_product_titles = flipkart_soup.findAll("div",{"class":"_4rR01T"})  #finds all titles of products using the title's a tag
flipkart_prices = flipkart_soup.findAll("div",{"class":"_30jeq3 _1_WHN1"})#finds all prices
flipkart_database = [['flipkart',],['flipkart',],['flipkart',],['flipkart',],['flipkart',]]


for i in range(0,5):
    try:
        amazon_database[i].append(amazon_product_titles[i].text)

        a = (amazon_prices[i].text.replace('₹', '')) #remove rupees sign
        amazon_database[i].append(int(a.replace(',',''))) #removes all commas and converts to int
    except:
        print("error in amazon")
    try:
        flipkart_database[i].append(flipkart_product_titles[i].text)

        b = (flipkart_prices[i].text.replace('₹', ''))  # remove rupees sign
        flipkart_database[i].append(int(b.replace(',', '')))  # removes all commas and converts to int
    except:
        print("error in flipkart")
    try:
        vijay_database[i].append(vijay_product_titles[i]['title'])

        c = (vijay_prices[i].text.replace('₹', ''))  # remove rupees sign
        vijay_database[i].append(int(c.replace(',', '')))  # removes all commas and converts to int
    except:
        print("error in vijay sales")
        continue

with open('products.csv','w',newline='') as f:
    thewriter = csv.writer(f)
    writer = csv.DictWriter(f, fieldnames=["WEBSITE", "PRODUCT", "PRICE"])
    writer.writeheader()
    thewriter.writerows(amazon_database)
    thewriter.writerows(flipkart_database)
    thewriter.writerows(vijay_database)


#uClient1 = uReq(croma_url) #opening up the connection
#croma_html = uClient1.read() #grabbing the page data
#uClient1.close()
#
#croma_soup = soup(croma_html, "html.parser") #html parsing
#croma_product_titles = croma_soup.findAll("h3",{"class":"product-title plp-prod-title"})  #finds all titles of products using the title's a tag
#
#croma_prices = croma_soup.findAll("span",{"class":"amount"})  #finds all prices
#
#croma_database = [['croma',],['croma',],['croma',],['croma',],['croma',]]
