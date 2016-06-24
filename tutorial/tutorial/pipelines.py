# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors
from tutorial.settings import database
import Mail.mail as my_mail
import ConfigParser

class TutorialPipeline(object):
    def __init__(self):
    	self.connection = pymysql.connect(
    		host=database['MYSQL_HOST'],
    		port=database['MYSQL_PORT'],
        	user=database['MYSQL_USER'],
        	password=database['MYSQL_PASSWD'],
        	db=database['MYSQL_DBNAME'],
        	charset='utf8',
        	cursorclass=pymysql.cursors.DictCursor
        )

    def process_item(self, item, spider):
    	succeed=False
    	try:
	    	with self.connection.cursor() as cursor:
	    		sql="INSERT INTO `zbj_order` (`order_id`, `title`, `money`, `link`, `desc`, `type`) VALUES (%s, %s, %s, %s, %s, %s)"
	    		cursor.execute(sql,(item['order_id'],item['title'],item['money'],item['link'],item['desc'],item['_type']))
	    	self.connection.commit()
	    	succeed=True
    	except:
    		print '数据保存失败..'

        if succeed:
            config=ConfigParser.ConfigParser()
            config.read('tutorial/config.cfg')

            send_eamil=config.get('option','send_email')
            if int(send_eamil)==1:
                if item['money']==-1:
                    title="【可议价】"+str(item['title'])
                else:
                    title="【￥ "+item['money']+"】"+str(item['title'])
            
                mailto_list=list(config.get('mailto_list','list_1').split(','))
                my_mail.send_mail(mailto_list,title,item['link'])
            else:
                print '不发送邮件..'
