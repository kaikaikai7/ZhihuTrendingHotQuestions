# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ZhihuQuestionItem(scrapy.Item):
    # 问题（id）、标题（title）、网址（url）、创建时间（created）、回答数量（answer_count）
    # 关注者数量（follower_count）、概要（excerpt）、热度（heat）
    question_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    created = scrapy.Field()
    answer_count = scrapy.Field()
    follower_count = scrapy.Field()
    excerpt = scrapy.Field()
    heat = scrapy.Field()


class ZhihuAnswerItem(scrapy.Item):
    # 回答（id）、内容（content）、赞同数（voteup_count）、更新时间（updated_time）
    # 问题（id）、用户（id）
    answer_id = scrapy.Field()
    content = scrapy.Field()
    voteup_count = scrapy.Field()
    updated_time = scrapy.Field()
    question_id = scrapy.Field()
    user_id = scrapy.Field()


class ZhihuUserItem(scrapy.Item):
    pass
