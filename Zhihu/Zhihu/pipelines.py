# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
from datetime import datetime
import re
from bs4 import BeautifulSoup


class ZhihuPipeline:
    # 时间转换函数
    def convert_unix_timestamp(self, unix_timestamp):
        # 将UNIX时间戳转换为datetime对象
        dt = datetime.fromtimestamp(unix_timestamp)

        # 将datetime对象转换为可读的日期和时间格式
        formatted_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")

        return formatted_datetime

    # 过滤html标签，提取文字
    def get_text_from_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        return text

    # 爬虫开启的时候执行一次
    def open_spider(self, spider):
        print(f"{spider.name} 爬取开始")
        if spider.name == 'questionInfo':
            # 获取当前日期
            current_date = datetime.now().strftime('%Y-%m-%d')
            self.questionFile = open(f'Zhihu/data/question/{current_date}.json', 'w', encoding='utf-8')
            self.questionData = []
        if spider.name == 'answerInfo':
            pass

    # 爬虫关闭的时候执行一次
    def close_spider(self, spider):
        print(f"{spider.name} 爬取完成")
        if spider.name == 'questionInfo':
            json.dump(self.questionData, self.questionFile, ensure_ascii=False, indent=4)
            self.questionFile.close()
        if spider.name == 'answerInfo':
            pass

    def process_item(self, item, spider):
        if spider.name == 'questionInfo':
            item['url'] = item['url'].replace("api.zhihu.com/questions", "www.zhihu.com/question")
            item['created'] = self.convert_unix_timestamp(item['created'])
            # item['heat'] = int(re.search(r'\d+', item['heat']).group())
            if item['heat'] == "热度累计中":
                item['heat'] = 0
            else:
                item['heat'] = int(re.search(r'\d+', item['heat']).group())
            item_dict = {
                'question_id': item['question_id'],
                'title': item['title'],
                'url': item['url'],
                'created': item['created'],
                'answer_count': item['answer_count'],
                'follower_count': item['follower_count'],
                'excerpt': item['excerpt'],
                'heat': item['heat']
            }
            self.questionData.append(item_dict)

        if spider.name == 'answerInfo':
            # 文件模板
            file_template = "Zhihu/data/answer/{question_id}.json"
            question_id = item["question_id"]
            file_path = file_template.format(question_id=question_id)
            # 检查文件是否存在
            if not os.path.exists(file_path):
                # 如果文件不存在，则创建文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump([], file, ensure_ascii=False, indent=4)

            # 构造数据
            item['content'] = self.get_text_from_content(item['content'])
            item['updated_time'] = self.convert_unix_timestamp(item['updated_time'])
            item_dict = {
                'answer_id': item['answer_id'],
                'content': item['content'],
                'voteup_count': item['voteup_count'],
                'updated_time': item['updated_time'],
                'question_id': item['question_id'],
                'user_id': item['user_id']
            }
            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            data.append(item_dict)
            # 写入JSON文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

        return item
