import json
import scrapy
from Zhihu.items import ZhihuQuestionItem


class QuestioninfoSpider(scrapy.Spider):
    name = "questionInfo"
    allowed_domains = ["www.zhihu.com"]
    # 备用API:https://api.zhihu.com/topstory/hot-list
    start_urls = ["https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"]

    def parse(self, response):
        data = json.loads(response.body)
        for entry in data["data"]:
            item = ZhihuQuestionItem()
            item["question_id"] = entry["target"]["id"]
            item["title"] = entry["target"]["title"]
            item["url"] = entry["target"]["url"]
            item["created"] = entry["target"]["created"]
            item["answer_count"] = entry["target"]["answer_count"]
            item["follower_count"] = entry["target"]["follower_count"]
            item["excerpt"] = entry["target"]["excerpt"]
            item["heat"] = entry["detail_text"]
            yield item
