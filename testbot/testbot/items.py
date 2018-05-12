# -*- coding: utf-8 -*-
import scrapy
from scrapy_djangoitem import DjangoItem
from warehouse.models import TestScrapy
from albumCom.models import AlbumComent
from albumId.models import AlbumId
from singerId.models import SingerId


# class AlbumItem(scrapy.Item):
#     # define the fields for your item here like:
#     name = scrapy.Field()  # 专辑名字
#     pic = scrapy.Field()  # 专辑图片
#     url = scrapy.Field()  # 专辑的链接
#     pass


class TestbotItem(DjangoItem):
    django_model = TestScrapy


class AlbumComItem(DjangoItem):
    django_model = AlbumComent


class AlbumIdItem(DjangoItem):
    django_model = AlbumId


class SingerItem(DjangoItem):
    django_model = SingerId
