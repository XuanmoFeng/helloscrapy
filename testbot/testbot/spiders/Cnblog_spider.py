# coding:utf-8
import scrapy
from testbot.items import *
from scrapy.selector import Selector
from selenium import webdriver


class Cnblog_Spider(scrapy.Spider):
    name = "cnblog1"
    allowed_domains = []
    driver = webdriver.Firefox()  # 封装浏览器信息
    start_urls = [
        'http://music.163.com/artist/album?id=3684&limit=100'
    ]

    def parse(self, response):
        selector = Selector(response=response)
        albumname = selector.xpath(
            '//ul/li/div[@class="u-cover u-cover-alb3"]/@title').extract()
        albumid = selector.xpath(
            '//ul/li/div[@class="u-cover u-cover-alb3"]/a[@class="msk"]/@href').extract()
        albumpic = selector.xpath(
            '//ul/li/div[@class="u-cover u-cover-alb3"]/img/@src').extract()
        for name, id, pic in zip(albumname, albumid, albumpic):
            album = AlbumIdItem()
            album['albumname'] = name
            album['albumid'] = id
            album['albumpic'] = pic
            album.save()
        for url in albumid:
            url = response.urljoin(url)
            self.driver.get(url)
            self.driver.switch_to_frame("contentFrame")
            page = self.driver.page_source
            self.parse_music(page)
        return

    # 获取歌曲的内容
    def parse_music(self, page):
        selector = Selector(text=page)
        urls = selector.xpath('//span[@class="txt"]/a/@href').extract()
        names = selector.xpath('//span[@class="txt"]/a/b/@title').extract()
        for url, name in zip(urls, names):
            music = TestbotItem()
            music['url'] = url
            music['name'] = name
            music.save()
