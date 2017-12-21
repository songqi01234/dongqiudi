# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymysql
from scrapy.pipelines.images import ImagesPipeline
from scrapy.conf import settings


class DownloadImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):  # 下载图片
        for image_url in item['img']:
            yield scrapy.Request(image_url,meta={'item': item, 'index': item['img'].index(image_url)})  # 添加meta是为了下面重命名文件名使用

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']  # 通过上面的meta传递过来item
        index = request.meta['index']  # 通过上面的index传递过来列表中当前下载图片的下标
        # 图片文件名
        image_name = request.url.split('/')[-1]
        # 图片下载目录
        filename = '/Users/xiaolongxia/Desktop/11/{0}/{1}'.format(item['title'], image_name)
        return filename


class DongqiudiPipeline(object):
    def process_item(self, item, spider):
        host = settings['MYSQL_HOSTS']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        c = settings['CHARSET']
        port = settings['MYSQL_PORT']
        # 数据库连接
        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
        # 数据库游标
        cue = con.cursor()
        print("mysql connect succes")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
        try:
            cue.execute(
                "insert into dongqiudi (title,author,url,times,img,news) values(%s,%s,%s,%s,%s,%s)", [item['title'], item['author'], item['url'], item['times'], item['img'], item['news']])
            print("insert success")  # 测试语句
        except Exception as e:
            print('Insert error:', e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item
