import requests
from bs4 import BeautifulSoup
import time
import csv
import send_mail
from datetime import date

urls = ["https://finance.yahoo.com/quote/AMZN?p=AMZN&.tsrc=fin-srch","https://finance.yahoo.com/quote/GOOG?p=GOOG&.tsrc=fin-srch","https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch","https://finance.yahoo.com/quote/FB?p=FB&.tsrc=fin-srch"]
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}

today = str(date.today()) + ".csv"
csv_file = open(today,"w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Stock Name','Current Price','Previous Close','Open','Bid','Ask','Days Range','52 Week Range','Volume','Avg. Volume'])

for url in urls:
    stock = []
    html_page = requests.get(url,headers = headers)
    soup = BeautifulSoup(html_page.content, 'lxml')

    stock_title = soup.find_all("div",id="quote-header-info")[0].find("h1").get_text()
    current_price = soup.find("div",class_="D(ib) Mend(20px)").find("span").get_text()

    stock.append(stock_title)
    stock.append(current_price)

    # print(stock_title)
    # print(current_price)

    table_info = soup.find_all("div",class_="D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)")[0].find_all("tr",)
    for i in range(0,8):
        # heading = table_info[i].find_all("td")[0].get_text()
        value = table_info[i].find_all("td")[1].get_text()
        stock.append(value)

    csv_writer.writerow(stock)
        # print(heading + " : " + value)
    # print("---------------")
    time.sleep(3)
csv_file.close()
send_mail.send(filename=today)
