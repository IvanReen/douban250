# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from db_spider.items import DbSpiderItem


class DbMmcSpider(CrawlSpider):
    name = 'db_mmc'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    # https://movie.douban.com/subject/1291546/
    rules = (
        # 翻页
        Rule(LinkExtractor(allow=r'\?\w+=\d+&\w+='), callback='parse_item', follow=False),
        # 具体电影链接
        # Rule(LinkExtractor(allow=r'https://\w+\.\w+\.\w+\/\w+\/\d+\/'), callback='movie_info', follow=False),
    )

    def parse_item(self, response):
        print('***************************')
        movie_info_list = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for movie_info in movie_info_list:
            item = DbSpiderItem()
            # 图片
            item['img_url'] = movie_info.xpath('./div/div/a/img/@src').extract_first()
            # 电影名
            item['movie_name'] = movie_info.xpath(".//div[@class='hd']/a/span[1]/text()").extract_first()
            # 电影详细页面链接
            movie_href = movie_info.xpath(".//div[@class='hd']/a/@href").extract_first()
            # 多少评论
            item['comment'] = movie_info.xpath(".//div[@class='star']/span[last()]").extract_first()
            yield scrapy.Request(movie_href, self.movie_info, meta={'item': item})

    def movie_info(self, res):
        item = res.meta['item']
        # 电影简介
        item['movie_content'] = res.xpath('//div[@id="link-report"]/span[2]/text()').extract_first()
        # 主演
        item['leading'] = res.xpath('//div[@id="info"]/span[@class="actor"]//a/text()').extract()
        # IMDB链接
        item['imdb_url'] = res.xpath('//div[@id="info"]/a[last()]/@href').extract_first()
        yield item