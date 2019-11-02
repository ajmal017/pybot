import urllib
from bs4 import BeautifulSoup
from requests import get


url = "https://finviz.com/quote.ashx?t=AAPL"
with urllib.request.urlopen(url) as response:
   html = response.read()
   soup = BeautifulSoup(html, 'html.parser')
   print(soup.contents[36].table.tr.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.b.string)


#/html/body/table[3]/tbody/tr[1]/td/table/tbody/tr[7]/td/table/tbody/tr[11]/td[6]/b
