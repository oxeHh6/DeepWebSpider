import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lxml import etree
from loguru import logger
import settings
from spider_db import DarkWebInfo
from register_and_login import RegisterLogin


class DeepWebSpider:
    def __init__(self):
        self.index_url = 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/index.php'
        self.origin_url = 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion'
        self.session = requests.session()
        self.cookies_config_file = 'cookies_config.json'
        with open(self.cookies_config_file, 'r', encoding='utf-8') as f:
            cookies_str = f.read()
        if cookies_str:
            self.cookies_dict = json.loads(cookies_str)
        else:
            self.cookies_dict = settings.COOKIES_DICT

    def set_cookie(self):
        """设置cookie值"""
        cookies = requests.utils.cookiejar_from_dict(self.cookies_dict)
        self.session.cookies = cookies

    def spider(self):
        logger.info("~~~~~~~~开始爬取deepmix中文暗网信息！！！~~~~~~~~")
        self.set_cookie()
        text = self.get_html(self.index_url, is_str=True)
        soup = BeautifulSoup(text, 'html.parser')
        column_list = soup.findAll('a', attrs={'href': re.compile('^ea.php'), 'class': 'index_list_title'})  # 抓取分类
        column_count = len(column_list)
        if column_count != 0:
            logger.info("----------共发现{}个栏目----------".format(column_count))
        else:
            logger.warning("----------Cookie已过期，请在配置文件中替换Cookie后再次尝试----------")
            register_login = RegisterLogin()
            cookies = register_login.login()
            with open(self.cookies_config_file, 'w+', encoding='utf-8') as f:
                f.write(json.dumps(cookies))
            self.cookies_dict = cookies
            return self.spider()
        self.index(text)

    def index(self, text):
        logger.info("——————————访问主界面——————————")
        htmlXpath = etree.HTML(text)
        div_list = htmlXpath.xpath('//div[@class="ad_div_b"]')
        for div in div_list:
            items = dict()
            # 数据类型
            data_type = div.xpath('.//tr[1]/td/text()')[0].strip()
            items['data_type'] = data_type
            link = div.xpath('.//a[@class="index_list_title"]/@href')
            link = urljoin(self.origin_url, link[0])
            # 获取列表页前十个页面的信息
            for page in range(1, 11):
                logger.info(f'[+] 当前正在爬取第{page}页数据')
                tmp_param = f'&pagea={page}'
                list_page_link = link + tmp_param
                info_list = self.parse_list(list_page_link, items)

    def parse_list(self, link, items):
        info_list = list()
        text = self.get_html(link, is_str=True)
        htmlXpath = etree.HTML(text)
        tr_list = htmlXpath.xpath('//table[@class="u_ea_a"]//tr')
        tr_list = [tr for tr in tr_list[3:-2:2]]
        for tr in tr_list:
            # 发布时间
            publish_date = tr.xpath('./td[2]/text()')[0]
            # 发布人
            publisher = tr.xpath('./td[3]/text()')[0]
            # 内容
            title = tr.xpath('./td[4]/div/a/text()')[0].strip()
            # 数据资源详情页链接
            detail_link = urljoin(self.origin_url, tr.xpath('./td[4]/div/a/@href')[0])
            # 标价，价格单位为比特币
            price = tr.xpath('./td[5]/text()')[0]
            items['publish_date'] = publish_date
            items['publisher'] = publisher
            items['title'] = title
            items['detail_link'] = detail_link
            items['price'] = price
            items = self.parse_detail(detail_link, items)
            print(items)
            if DarkWebInfo.select().where(DarkWebInfo.title == title).count() > 0:
                continue
            DarkWebInfo.create(**items)
            info_list.append(items)
        return info_list

    def parse_detail(self, link, items):
        text = self.get_html(link, is_str=True)
        htmlXpath = etree.HTML(text)
        description_list = htmlXpath.xpath('//div[@class="div_masterbox"]/t/text()')
        # 商品描述
        description = ','.join([description.strip() for description in description_list if description.strip()])
        items['description'] = description
        return items

    def get_html(self, url, is_str=False):
        content = 'false'
        for temp in range(1, 4):
            try:
                res = self.session.get(url=url,
                                       headers=settings.HEADERS,
                                       proxies=settings.PROXY,
                                       timeout=settings.TIMEOUT,
                                       )
                res.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            except requests.RequestException as e:
                logger.warning(f'{e}')
                logger.info("[-] 加载页面失败，正在重新加载***")
            else:
                content = res.content
                if is_str:
                    content = res.text
        return content





