from bs4 import BeautifulSoup as bs
import requests
import csv

page = 1
count = 1
jokes_list = []

def parse(url, pages):
    global page
    global count
    while page != pages + 1:
        url = url
        req = requests.get(url)
        soup = bs(req.content, 'html.parser')
        s = soup.find('article')
        # new content
        content = s.find_all('p')

        for line in content:
            d = {}
            d['index'] = count
            d['joke'] = line.text.strip()
            count += 1
            jokes_list.append(d)
        
        page = page + 1
    print('Success!')

parse(f"https://onelinefun.com/it/{page}/", 21)
page = 1
parse(f"https://onelinefun.com/dirty/{page}/", 46)

print(jokes_list)

filename = 'jokes.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['index','joke'])
    w.writeheader()
     
    w.writerows(jokes_list)