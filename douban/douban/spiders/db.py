# -*- coding: utf-8 -*-
import scrapy

from douban.items import DoubanItem


class DbSpider(scrapy.Spider):
    name = 'db'
    allowed_domains = ['www.douban.com']
    url = 'https://movie.douban.com/top250?start='
    page = 0
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movie_info_list = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for movie_info in movie_info_list:
            item = DoubanItem()
            # 图片
            item['img_url'] = movie_info.xpath('./div/div/a/img/@src').extract_first()
            # 电影名
            item['movie_name'] = movie_info.xpath(".//div[@class='hd']/a/span[1]/text()").extract_first()
            # 电影详细页面链接
            movie_href = movie_info.xpath(".//div[@class='hd']/a/@href").extract_first()
            # 多少评论
            item['comment'] = movie_info.xpath(".//div[@class='star']/span[last()]/text()").extract_first()
            yield scrapy.Request(movie_href, self.movie_info, meta={'item': item}, dont_filter=True)

        self.page += 25
        if self.page <= 225:
            url = self.url + str(self.page)
            yield scrapy.Request(url, callback=self.parse)

    def movie_info(self, res):
        item = res.meta['item']
        # 电影简介
        item['movie_content'] = res.xpath('//div[@id="link-report"]/span[2]/text()').extract_first()
        # 主演
        item['leadings'] = res.xpath('//div[@id="info"]/span[@class="actor"]//a/text()').extract()
        # IMDB链接
        item['imdb_url'] = res.xpath('//div[@id="info"]/a[last()]/@href').extract_first()
        yield item

