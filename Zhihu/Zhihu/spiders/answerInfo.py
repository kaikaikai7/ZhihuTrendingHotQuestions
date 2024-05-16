import json
from datetime import datetime
import scrapy
from Zhihu.items import ZhihuAnswerItem


class AnswerinfoSpider(scrapy.Spider):
    name = "answerInfo"
    allowed_domains = ["www.zhihu.com"]
    start_urls = []
    # current_date = datetime.now().strftime('%Y-%m-%d')
    # urls_file = open(f'Zhihu/data/question/{current_date}.json', 'r', encoding='utf-8')
    urls_file = open(f'Zhihu/data/question/2024-05-05.json', 'r', encoding='utf-8')
    data = json.load(urls_file)
    # URL 模板
    url_template = "https://www.zhihu.com/api/v4/questions/{question_id}/feeds?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cvip_info%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings.table_of_content.enabled&offset=2&limit=200&order=default&platform=desktop"
    # 遍历数据，拼接 URL
    for item in data:
        question_id = item["question_id"]
        url = url_template.format(question_id=question_id)
        start_urls.append(url)

    i = 0

    def parse(self, response):
        data = json.loads(response.body)
        print(f"第{self.i}页爬取完成")
        self.i = self.i + 1
        for entry in data["data"]:
            item = ZhihuAnswerItem()
            item["answer_id"] = entry['target']['id']
            item["content"] = entry['target']['content']
            item["voteup_count"] = entry['target']['voteup_count']
            item["updated_time"] = entry['target']['updated_time']
            item["question_id"] = entry['target']['question']['id']
            item["user_id"] = entry['target']['author']['id']
            yield item

        if not data['paging']['is_end']:
            new_url = data['paging']['next']
            yield scrapy.Request(url=new_url, callback=self.parse)
