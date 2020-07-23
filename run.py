import init  # 导入init.py文件
from deep_web_spider import DeepWebSpider


def main():
    # 建立新的tor节点
    current_status = init.switch_tor_ip()
    if current_status == 'false':
        return
    deep_spider = DeepWebSpider()
    deep_spider.spider()


if __name__ == "__main__":
    main()
