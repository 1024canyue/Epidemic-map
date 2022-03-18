# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Covid19Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area = scrapy.Field()  # 地区
    city = scrapy.Field()  # 城市
    nativeRelative = scrapy.Field()  # 昨日新增
    confirmed = scrapy.Field()  # 累计确诊
    crued = scrapy.Field()  # 累计治愈
    died = scrapy.Field()  # 累计死亡
    curConfirm = scrapy.Field()  # 现有
    asymptomatic = scrapy.Field()  # 无症状感染者

    # pass
