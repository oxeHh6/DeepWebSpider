import pymysql
from peewee import *

import settings

Links = {
    'host': settings.MYSQL_HOST,
    'port': settings.MYSQL_PORT,
    'user': settings.MYSQL_USER,
    'password': settings.MYSQL_PASSWORD,
}

try:
    con = pymysql.connect(**Links)
    with con.cursor() as cursor:
        cursor.execute(
            f'create database {settings.MYSQL_DBNAME} character set UTF8mb4 collate utf8mb4_bin'
        )
        con.close()
except pymysql.err.ProgrammingError as e:
    if '1007' in str(e):
        pass
except Exception as e:
    raise e


db = MySQLDatabase(settings.MYSQL_DBNAME, **Links)


class BaseModel(Model):
    class Meta:
        database = db


class DarkWebInfo(BaseModel):
    description = TextField()
    title = CharField()
    publish_date = CharField()
    publisher = CharField()
    detail_link = CharField()
    price = CharField()
    data_type = CharField()

    class Meta:
        table_name = 'dark_web'


db.create_tables([DarkWebInfo])


if __name__ == '__main__':
    items = {
        'title': 'this is test 1',
        'publish_date': '2020/6/10 10:00',
        'detail_link': 'xxx.onion',
        'publisher': 'xxx',
        'price': '0.00035',
        'data_type': '数据资源',
        'description': '出售xxx数据'
    }

    a = DarkWebInfo.select().where(DarkWebInfo.title == items['title']).count()
    if a == 0:
        print('插入数据')
        dark_web_info = DarkWebInfo.create(**items)
    else:
        print(a)





