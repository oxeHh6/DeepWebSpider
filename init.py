from stem import Signal  # tor的控制工具
from stem.control import Controller
import requests
from bs4 import BeautifulSoup
import os
import settings
from settings import tor_listener_port, tor_sockets_port, proxy_rules, default_path, header, TIMEOUT


def switch_tor_ip():
    """切换TOR节点"""
    try:
        # controller = Controller.from_port(port=int(tor_listener_port))  # 9151为tor的监听端口
        # controller.authenticate()
        # controller.signal(Signal.NEWNYM)
        session = requests.session()
        resp = session.get(url="https://check.torproject.org/?lang=zh_CN",
                           headers=header,
                           proxies=settings.PROXY,
                           timeout=TIMEOUT,
                           )
        soup = BeautifulSoup(resp.content, 'lxml')
        print('[+] ' + soup.find('h1').text.replace("\n", "").replace(' ', ''))  # 删除输出中的换行符和空格
        print('[+] ' + soup.find('p').text)
        make_new_path()  # 如果代理成功则创建爬虫目录
    except Exception as e:
        print("[-] Error，请重新配置tor_init.ini")
        return 'false'
    else:
        # controller.close()
        return 'success'


def make_new_path():
    """生成新的文件存放目录。以日期为文件夹名"""
    if not (os.path.exists(default_path)):
        os.mkdir(default_path)


if __name__ == '__main__':
    switch_tor_ip()





