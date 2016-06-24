# -*- coding:utf-8 -*-
import scrapy
from tutorial.items import TutorialItem
from urlparse import urlparse
import sys
import ConfigParser  

reload(sys)
sys.setdefaultencoding('utf-8')

config=ConfigParser.ConfigParser()  
#with open('tutorial/config.cfg','rw') as cfgfile:  
    #config.readfp(cfgfile)  
config.read('tutorial/config.cfg')

class DmozSpider(scrapy.spiders.Spider):
    name = 'dmoz'
    allowed_domians = ['www.zbj.com']
    start_urls = [
        "http://www.zbj.com/wxptkf/t.html?w=2&o=7",
        "http://www.zbj.com/ydyykf/t.html?w=2&o=7"
    ]

    def parse(self,response):
        res = response.xpath('//tr')
        items = []
        temp_id=0
        cur_type='wx'

        for sel in res:
            #print sel
            item = TutorialItem()
            link = ''.join(sel.xpath('td/p/a[@class="list-task-title"]/@href').extract()).encode("utf-8")

            if link=="":
                continue

            url = urlparse(link)
            url = url.path
            cur_id = long(url[1:-1])

            if response.url=="http://www.zbj.com/wxptkf/t.html?w=2&o=7":
                cur_type='wx'
                item['_type']=1
            else:
                cur_type='app'
                item['_type']=2

            max_id=long(config.get('last_id',cur_type))

            if cur_id>max_id:
                item['order_id'] = cur_id
                item['link'] = link
                item['title'] = ''.join(sel.xpath('td/p/a[@class="list-task-title"]/text()').extract()).encode("utf-8")

                money = ''.join(sel.xpath('td/p/em[@class="list-task-reward"]/text()').extract()).encode("utf-8")

                if money.find("¥ ")!=-1:
                    item['money']=money.replace("¥ ","")
                else:
                    item['money']=-1;
                
                item['desc'] = ''.join(sel.xpath('td/p[@class="list-task-ctn"]/text()').extract()).encode("utf-8") 

                items.append(item)
                if cur_id>temp_id:
                    temp_id=cur_id
            else:
                continue

        if temp_id>0:
            config.set('last_id',cur_type,temp_id)
            config.write(open('tutorial/config.cfg', 'w')) 

        if items:
            return items
        else :
            print '没有新的需求订单..'

