#!/usr/bin/python
# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup
import re
import csv

def url_parser(url):
    "收集信息：单价，面积，总价，房龄，地址，房源编号，(小区单价)"
    req = requests.get(url)
    soup = BeautifulSoup(req.content,'html.parser')
    total =  soup.find(class_='price-total').span.get_text()
    unit_price =  soup.find(class_='price-unit-num').span.get_text()
    items = soup.find("li",class_="main-item u-tr").find_all('p')
    area = items[0].get_text().rstrip(u'\u5e73')
    age = items[1].get_text().strip().rstrip(u'\u5e74\u5efa')

    address =  soup.find(class_='item-cell maininfo-estate-address').string.encode('utf-8')	
    record_sum = soup.find('look-list')['count90']
    id =  re.compile("sh\d+").search(soup.get_text()).group()

    return [id,total,unit_price,area,age,address,record_sum]

def list_page_parser(district,start=1,stop=5):
    #url_format = 'http://sh.lianjia.com/ershoufang/d{}'
    url_format = 'http://sh.lianjia.com/ershoufang/{}/b0to300d{}m40to100000000s1'
	#eg: http://sh.lianjia.com/ershoufang/pudong/b0to300d1m40to100000000s1
	# b:售价 m:面积 s1:总价从低到高
    results = []
    count = 0
    for page in range(start,stop):
        req = requests.get(url_format.format(district,page))
        sp = BeautifulSoup(req.content,'html.parser')
        urls = [ i['href'] for i in \
                 sp.find(class_='js_fang_list').find_all(class_='text',href=re.compile('sh\d+'))]
        for url in urls:
            real_url="http://sh.lianjia.com%s" % url
            count +=1
            print "Parsing no.%d : %s" % (count,real_url)
            results.append(url_parser(real_url))

	with open('lianjia.csv','wb') as f: 
		csv_writer=csv.writer(f)
		csv_writer.writerow(['房源编号','总价','单价','面积','房龄','地址','看房纪录'])
		for r in results:
		    #print " ".join([isinstance(j,unicode) and j.encode('utf-8') or j for j in r])
			csv_writer.writerow([isinstance(j,unicode) and j.encode('utf-8') or j for j in r])	

if __name__ == "__main__":
    print "---start---"
    list_page_parser("pudong",1,2)
    print "---end---"
