from tkinter import *
import tkinter.ttk as ttk
import pandas as pd
import csv
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# writing code needs to
# create the main window of
# the application creating
# main window object named root
root = Tk()

# Creating object of photoimage class
# Image should be in the same folder
# in which script is saved
p1 = PhotoImage(file='coin.png')

# Setting icon of master window
root.iconphoto(False, p1)
# giving title to the main window
root.title("PRICE COMPARISON APP")


# Label is what output will be
# shown on the window
label = Label(root, text="TRY BEING AS SPECIFIC AS YOU CAN TO HELP YOU GIVE BEST RESULTS! FOR EG.: VIVO V21 8GB RAM 256GB STORAGE").pack()

text_box = Entry(root,text="Enter Product Name",width=102)
text_box.pack()


def button_click():
    split = text_box.get().split(' ')
    x = ''
    y = ''
    for i in range(0, len(split)):  # this is a loop to make a string which will be accepted in the url of the websites
        x = x + '+' + split[i]
        y = y + '-' + split[i]
    amazon_url = f"https://www.amazon.in/s?k={x}&ref=nb_sb_noss_2"
    vijay_sales_url = f'https://www.vijaysales.com/search/{y[1:]}'
    #croma_url = f'https://www.croma.com/search/?text={x[1:]}'
    flipkart_url = f'https://www.flipkart.com/search?q={x[1:]}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&sort=relevance'

    uClient = uReq(amazon_url)  # opening up the connection
    amazon_html = uClient.read()  # grabbing the page data
    uClient.close()

    amazon_soup = soup(amazon_html, "html.parser")  # html parsing
    amazon_product_titles = amazon_soup.findAll("a", {
        "class": "a-link-normal a-text-normal"})  # finds all titles of products using the title's a tag

    amazon_prices = amazon_soup.findAll("span", {"class": "a-price-whole"})  # finds all prices
    amazon_database = [['amazon', ], ['amazon', ], ['amazon', ], ['amazon', ], ['amazon', ]]

    uClient3 = uReq(vijay_sales_url)  # opening up the connection
    vijay_html = uClient3.read()  # grabbing the page data
    uClient3.close()

    vijay_soup = soup(vijay_html, "html.parser")  # html parsing
    vijay_product_titles = vijay_soup.findAll("a",
                                              {"rel": "follow"})  # finds all titles of products using the title's a tag
    vijay_prices = vijay_soup.findAll("div", {"class": "Dynamic-Bucket-vsp"})  # finds all prices
    vijay_database = [['vijay', ], ['vijay', ], ['vijay', ], ['vijay', ], ['vijay', ]]

    uClient2 = uReq(flipkart_url)  # opening up the connection
    flipkart_html = uClient2.read()  # grabbing the page data
    uClient2.close()

    flipkart_soup = soup(flipkart_html, "html.parser")  # html parsing
    flipkart_product_titles = flipkart_soup.findAll("div", {
        "class": "_4rR01T"})  # finds all titles of products using the title's a tag
    flipkart_prices = flipkart_soup.findAll("div", {"class": "_30jeq3 _1_WHN1"})  # finds all prices
    flipkart_database = [['flipkart', ], ['flipkart', ], ['flipkart', ], ['flipkart', ], ['flipkart', ]]

    for i in range(0, 5):
        try:
            amazon_database[i].append(amazon_product_titles[i].text)

            a = (amazon_prices[i].text.replace('₹', ''))  # remove rupees sign
            amazon_database[i].append(int(a.replace(',', '')))  # removes all commas and converts to int
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

    with open('products.csv', 'w', newline='') as f:
        thewriter = csv.writer(f)
        writer = csv.DictWriter(f, fieldnames=["WEBSITE", "PRODUCT", "PRICE"])
        writer.writeheader()
        thewriter.writerows(amazon_database)
        thewriter.writerows(flipkart_database)
        thewriter.writerows(vijay_database)

    csv_reader = pd.read_csv('products.csv')
    csv_reader.sort_values(by=["PRICE"], ascending=False, inplace=True)
    csv_reader.to_csv('products.csv', index=False)

    print(csv_reader)


    with open('products.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            WEBSITE = row['WEBSITE']
            PRODUCT = row['PRODUCT']
            PRICE = row['PRICE']
            tree.insert("", 0, values=(WEBSITE, PRODUCT, PRICE))
        f.close()


search_button = Button(root,text="Search",command=button_click)
search_button.pack()

def clear():
    text_box.delete(0,'end')
    tree.delete(*tree.get_children())

clear_button = Button(root,text="Clear",command=clear)
clear_button.pack()

TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("WEBSITE", "PRODUCT", "PRICE"), height=100, selectmode="extended",
                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('WEBSITE', text="WEBSITE", anchor=W)
tree.heading('PRODUCT', text="PRODUCT", anchor=W)
tree.heading('PRICE', text="PRICE", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=200)
tree.column('#2', stretch=NO, minwidth=0, width=200)
tree.column('#3', stretch=NO, minwidth=0, width=300)
tree.pack()




# calling mainloop method which is used
# when your application is ready to run
# and it tells the code to keep displaying
root.mainloop()


