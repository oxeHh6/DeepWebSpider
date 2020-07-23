import os
import requests
from requests import exceptions
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from lxml import etree
from aip import AipOcr
from loguru import logger
import ocr
from settings import BASE_DIR, HEADERS, USERNAME, PASSWORD, TIMEOUT, PROXY


class RegisterLogin:
    def __init__(self):
        self.username = USERNAME
        self.password = PASSWORD
        self.login_url = 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/entrance/login.php'
        self.origin_url = 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion'
        self.session = requests.session()

    def register(self):
        logger.info('[*] 注册中......')
        pass

    def login(self):
        """在注册前需要访问route.php，以防直接访问注册页面地址失效"""
        logger.info('[*] 登录中......')
        content = self.get_html(self.login_url)
        soup = BeautifulSoup(content, 'lxml')
        img = soup.findAll('img', attrs={'title': '只能刷新页面换验证码, 为安全因素去除了js代码, 无法点此刷新'})
        i = img[-1]
        picture_link = i.get('src')  # 验证码地址
        verify_path = self.save_picture(picture_link)
        verify_code1 = self.get_verify_code(verify_path)
        verify_code2 = self.Identify(verify_path)
        print(f"[+] tesseract识别结果为：{verify_code1}")
        print(f"[+] 百度API识别结果为：{verify_code2}")
        verify_code = input('请输入验证码：')
        login_data = {
            'lgid': self.username,
            'lgpass': self.password,
            'sub_code': verify_code,
            'lgsub': '进入系统',
        }
        htmlXpath = etree.HTML(content)
        login_post_url = urljoin(self.origin_url, htmlXpath.xpath('//form/@action')[-1])
        try:
            r = self.session.post(url=login_post_url,
                                  headers=HEADERS,
                                  data=login_data,
                                  timeout=TIMEOUT,
                                  proxies=PROXY,
                                  verify=False,
                                  allow_redirects=True,
                                  )
            if r.status_code in {200}:
                logger.info('[*] 登录成功!')
                cookies = self.session.cookies.get_dict()
                print(cookies)
                text = r.text
                return cookies
            elif r.status_code in {301, 302}:
                logger.info('[*] 重定向!')
                return dict()
            else:
                logger.error('[*] 登录失败!')
                return dict()
        except exceptions.Timeout as e:
            logger.error('[*] 连接超时!')
            return dict()

    def get_verify_code(self, verify_path):
        verify_code = ocr.OCR_lmj(verify_path)
        return verify_code

    def get_html(self, url, cookies=None):
        for temp in range(1, 6):
            try:
                res = self.session.get(url=url,
                                       headers=HEADERS,
                                       proxies=PROXY,
                                       timeout=TIMEOUT,
                                       )

                if res.status_code != 200:
                    print("[-] 加载页面失败，正在重新加载***")
                    if temp == 5:
                        print("[-] 网络也许有问题，请重新进行配置")
                    continue
                content = res.content
                if cookies:
                    content = res.text
                return content
            except Exception as e:
                logger.info(f'{e}')
                return ''

    def save_picture(self, picture_link):
        """保存验证码图片"""
        content = self.get_html(picture_link)
        verify_path = os.path.join(BASE_DIR, 'Verification.jpg')
        with open(verify_path, 'wb') as file:
            file.write(content)
        print(f"[+] 验证码已保存到{verify_path}")
        return verify_path

    def Identify(self, picture_path):
        """通过百度API识别验证码"""
        APP_ID = '20293224'
        API_KEY = 'ydGGPNdL3Qfhn3KgKB6m0FFi'
        SECRET_KEY = 'mZ7xfQ8igZEV98047KP6G9ilv5bWAkDB'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        file = open(picture_path, 'rb')
        image = file.read()
        ''' 可选参数 '''
        options = dict()
        options["language_type"] = "ENG"  # 中英文混合
        options["detect_direction"] = "true"  # 检测朝向
        options["detect_language"] = "false"  # 是否检测语言
        options["probability"] = "false"

        result = client.basicGeneral(image, options)
        file.close()
        if 'words_result' in result:
            text = ''.join([w['words'] for w in result['words_result']])
        else:
            text = 'false'
        exclude_char_list = ' —.:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥§'
        text = ''.join([x for x in text if x not in exclude_char_list])
        return text


if __name__ == "__main__":
    deep_web = RegisterLogin()
    deep_web.login()





