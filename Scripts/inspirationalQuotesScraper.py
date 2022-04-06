'''imports'''
import csv
from bs4 import BeautifulSoup as bs
import requests

count = 1
quotes_list = []

def parse(url):
    global count
    url = url
    req = requests.get(url)
    soup = bs(req.content, 'html.parser')
    s = soup.find('div', class_ = 'ModernArticleBody__cleanBodyText__sNffF article-body')
    # new content
    content = s.find_all('p')

    for line in content:
        d = {}
        d['index'] = count
        d['quote'] = line.text.strip()
        count += 1
        quotes_list.append(d)
        
print('Success!')

parse("https://www.inc.com/bill-murphy-jr/366-top-inspirational-quotes-motivational-quotes-for-every-single-day-in-2020.html")


print(quotes_list)

filename = 'quotes.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['index','quote'])
    w.writeheader()
     
    w.writerows(quotes_list)