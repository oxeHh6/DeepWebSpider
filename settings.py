import os
import sys
import configparser  # 读取ini文件

# 项目基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# tesseract路径
if 'win' in sys.platform:
    TESSERACT_PATH = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
else:
    TESSERACT_PATH = ''

# tor参数配置
config = configparser.ConfigParser()
config.read('tor_init.ini', encoding='UTF-8')
tor_listener_port = config.get('tor', 'tor_listener_port')
tor_sockets_port = config.get('tor', 'tor_sockets_port')
proxy_rules = config.get('tor', 'proxy_rules')
default_path = config.get('file', 'default_path')

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
}

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'close',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion',
    'Referer': 'http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/entrance/login.php',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'
}

PROXY = {"https": "{}://127.0.0.1:{}".format(proxy_rules, tor_sockets_port),
         "http": "{}://127.0.0.1:{}".format(proxy_rules, tor_sockets_port)
         }

# cookies
COOKIES_DICT = {
    'PHPSESSID': 'uonq267miee8mv7lvcs6tjlucp',
    'userid': '568700',
}

# 中文暗网用户名和密码
USERNAME = '568700'
PASSWORD = 'wjh0213..'

# 访问超时
TIMEOUT = 30

# mysql数据库的配置
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_DBNAME = 'DeepWebSpider'
MYSQL_CHARSET = 'utf8'





