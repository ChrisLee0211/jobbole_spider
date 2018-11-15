# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst
import datetime


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
        create_date = str(create_date)
    return create_date


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def return_value(value):
    return value


class JobBoleArticleItem(scrapy.Item):
    # 文章标题
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )# 发布日期
    url = scrapy.Field()# 地址
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    ) # 封面图地址
    front_image_path = scrapy.Field()# 存放路径
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )# 点赞数
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    ) # 评论数
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    ) # 收藏数
    content = scrapy.Field()
    tag = scrapy.Field(
        output_processor=Join(",")
    )

    def get_insert_sql(self):
        insert_sql = """
            insert into article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
        """
        params = (self["title"], self["url"], self["create_date"], self["fav_nums"])

        return insert_sql, params
