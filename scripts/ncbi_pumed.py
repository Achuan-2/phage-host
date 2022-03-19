# Author  : cxnie66
import requests
import re
from lxml import etree
import pandas as pd
class NCBISpider:
    def __init__(self):
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}
        self.start_url = "https://pubmed.ncbi.nlm.nih.gov/?term=AHLs&page=1"

    def url_lists(self, total_num):
        url_lists = []
        for i in range(total_num):
            # 需要判断i是否需要字符串还是数字
            url = "https://pubmed.ncbi.nlm.nih.gov/?term=AHLs&page={}".format(
                i)
            print(url)
            url_lists.append(url)
        return url_lists

    def parase_url(self, url):  # 爬取内容
        print(url)
        response = requests.get(url, headers=self.headers, timeout=8)
        return response.content.decode()

    def save_csv_title(self):  # 先保存headers，也是就title
        columns = ["PMID", "title", "paper_citation","author", "Abstract", "paper_url"]
        title_csv = pd.DataFrame(columns=columns)
        title_csv.to_csv('AHLs_paper.csv', mode="a",
                    index=False, header=1, encoding="utf-8")

    def get_content(self, html):  # 获取相关内容

        nodes = etree.HTML(html)
        articel = nodes.xpath(
            '//div[@class="search-results-chunk results-chunk"]/article')
        # print(articel)
        ret = []
        for art in articel:
            # pass
            item = {}
            # 实现标题的去换行、空字符和连接
            item["title"] = art.xpath(
                './div[@class="docsum-wrap"]/div[@class="docsum-content"]/a[@class="docsum-title"]//text()')
            item["title"] = [i.replace("\n", "").strip()
                             for i in item["title"]]
            item["title"] = [''.join(item["title"])]

            item["PMID"] = art.xpath(
                './div[@class="docsum-wrap"]//span[@class="citation-part"]/span/text()')

            # 期刊相关信息
            item["paper_citation"] = art.xpath(
                './div[@class="docsum-wrap"]//span[@class="docsum-journal-citation full-journal-citation"]/text()')

            # 作者
            item["author"] = art.xpath(
                './div[@class="docsum-wrap"]//span[@class="docsum-authors full-authors"]/text()')
            # 摘要
            item["Abstract"] = art.xpath(
                './div[@class="docsum-wrap"]//div[@class="full-view-snippet"]//text()')
            item["Abstract"] = [i.replace("\n", "").strip()
                                for i in item["Abstract"]]
            item["Abstract"] = [''.join(item["Abstract"])]
            # 文章地址
            item["url"] = art.xpath(
                './div[@class="docsum-wrap"]//div[@class="share"]/button/@data-permalink-url')
            ret.append(item)

        self.save_content(ret)
        print("保存好了！！！")

    def save_content(self, ret):  # 保存到指定内容
        pf = pd.DataFrame(ret)
        pf.to_csv('AHLs_paper.csv', mode="a",
                  index=False, header=0, encoding="utf-8")

    def run(self):  # 实现主要逻辑
        self.save_csv_title()
        start_html = self.parase_url(self.start_url)
        total_num = re.findall(
            'totalResults: parseInt\("(.*?)", 10\)', start_html, re.S)[0]
        total_num = int(total_num)
        print(type(total_num))

        # 1、构造url列表
        url_lists = self.url_lists(total_num)
        for url in url_lists:
            # 2、requests爬虫
            htmls = self.parase_url(url)
            self.get_content(htmls)


if __name__ == "__main__":
    ncbi_spider = NCBISpider()
    ncbi_spider.run()
