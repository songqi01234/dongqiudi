# -*- coding: utf-8 -*-
import scrapy
import time


class DongqiSpiderSpider(scrapy.Spider):
    name = 'dongqiu_spider'
    allowed_domains = ['dongqiudi.com']
    start_urls = ['http://www.dongqiudi.com/?tab=1&page={}']
    cookies = {'dqduid':'ChOqelox78e5eASiTl5oAg==',' sajssdk_2015_cross_new_user':'1',' sensorsdata2015jssdkcross':'%7B%22distinct_id%22%3A%2216053109cf34bc-08891dbe9a4de-173f6d56-1764000-16053109cf4c3c%22%2C%22%24device_id%22%3A%2216053109cf34bc-08891dbe9a4de-173f6d56-1764000-16053109cf4c3c%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%E5%8F%96%E5%80%BC%E5%BC%82%E5%B8%B8%22%2C%22%24latest_referrer_host%22%3A%22%E5%8F%96%E5%80%BC%E5%BC%82%E5%B8%B8%22%7D%7D',' Hm_lvt_662abe3e1ab2558f09503989c9076934':'1513222086',' Hm_lpvt_662abe3e1ab2558f09503989c9076934':'1513223618',' laravel_session':'eyJpdiI6ImswTE5DWHZ4RVpacEVRV2lCMkhIUjdNNVpwanVoRkptUTYrSzBpaXVUYjQ9IiwidmFsdWUiOiJ1WXp3ZVhzV0RRVk5Bb1dZVFpxWElmdFVMVTAzRDJwdFJyeU9ERnZJSko1NFY2K2hiV20yZzZ0aW5lOU1ZOXVhUFJZVkZ3a0pCeUlkdzJTN1o5YjZWQT09IiwibWFjIjoiZjU2Mjc4ZDkyODEwMmY5MWRmOTU4MzA3YjI1NDU4MzcyMzVmZGFlNzc4MzZlZTA4NzkwMTU0YTllZjg4MTgxZiJ9'}

    # 构造url
    def start_requests(self):
        for url in self.start_urls:
            for i in range(1, 51):
                next_url = url.format(i)
                yield scrapy.Request(
                    next_url,
                    cookies=self.cookies,
                    callback=self.parse
                )

    # 新闻标题及url地址
    def parse(self, response):
        time.sleep(1)
        li_list = response.xpath('//ol/li')
        for li in li_list:
            item = {}
            item['title'] = li.xpath('./h2/a/text()').extract_first()
            item['url'] = li.xpath('./h2/a/@href').extract_first()
            yield scrapy.Request(
                item['url'],
                cookies=self.cookies,
                callback=self.parse_news,
                meta={'item':item}
            )

    # 时间、新闻内容、图片、作者
    def parse_news(self, response):
        time.sleep(1)
        item = response.meta['item']
        item['times'] = response.xpath('//span[@class="time"]/text()').extract_first()
        item['news'] = response.xpath('//div[@class="detail"]/div/p/text()').extract_first()
        item['img'] = response.xpath('//div[@class="detail"]/div//img/@src').extract()
        item['author'] = response.xpath('//span[@class="name"]/text()').extract_first()
        yield item