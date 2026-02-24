import requests, csv, os, time, random, django, datetime
from lxml import etree
import pandas as pd
from datetime import date, timedelta
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()
from myApp.models import CarInfo

class Spider:
    def __init__(self):
        last_month = (date.today().replace(day=1) - timedelta(days=1)).strftime('%Y%m')
        self.spiderUrl = (f'https://www.dongchedi.com/motor/pc/car/rank_data?'
                          f'aid=1839&app_name=auto_web_pc&city_name=玉林&count=10&month={last_month}'
                          f'&new_energy_type=&rank_data_type=11&brand_id=&price=&manufacturer=&series_type=&nation=0')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        # self.max_offset = 1000 # 保护性上限

    # ------------- 工具函数 --------------
    def get_page(self):
        with open('./spiderPage.txt', 'r') as f:
            return int(f.readlines()[-1].strip())

    def set_page(self, new):
        with open('./spiderPage.txt', 'a') as f:
            f.write('\n' + str(new))

    def xpath0(self, tree, xp):
        t = tree.xpath(xp)
        return t[0] if t else ''

    # ------------- 主流程 --------------
    def main(self,max_pages=200):
        offset = self.get_page()
        if offset // 10 >= max_pages:
            print(f'已达上限 {max_pages}，强制退出')
            return
        print('开始 offset =', offset)
        params = {'offset': offset}
        resp = requests.get(self.spiderUrl, headers=self.headers, params=params, timeout=15)
        if resp.status_code != 200:
            print('接口异常', resp.status_code)
            return
        data = resp.json()['data']['list']
        if not data:
            print('已到真实末尾，正常退出')
            return
        for car in data:
            try:
                carData = [
                    car["brand_name"],
                    car["series_name"],
                    car["image"],
                    car["count"],
                    f'[{car["min_price"]}, {car["max_price"]}]',
                    car["sub_brand_name"],
                    car["rank"]
                ]
                # 详情页
                detail = requests.get(f'https://www.dongchedi.com/auto/params-carIds-x-{car["series_id"]}',
                                      headers=self.headers, timeout=15)
                tree = etree.HTML(detail.text)
                carData += [
                    self.xpath0(tree, "//div[@data-row-anchor='jb']/div[2]/div/text()"),
                    self.xpath0(tree, "//div[@data-row-anchor='fuel_form']/div[2]/div/text()"),
                    self.xpath0(tree, "//div[@data-row-anchor='market_time']/div[2]/div/text()"),
                    self.xpath0(tree, "//div[@data-row-anchor='period']/div[2]/div/text()")
                ]
                self.save_csv(carData)
            except Exception as e:
                print('解析失败', e, car.get('series_name'))
                continue
            time.sleep(random.uniform(1, 2))
        self.set_page(offset + 10)
        self.main()          # 仍用递归，但上限已卡死

    # ------------- 落盘 --------------
    def init_csv(self):
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv', 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(
                    ["brand", "carName", "carImg", "saleVolume", "price", "manufacturer", "rank",
                     "carModel", "energyType", "marketTime", "insure"])

    def save_csv(self, row):
        with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(row)

    def clean_csv(self):
        df = pd.read_csv('./temp.csv').dropna().drop_duplicates()
        print('清洗后共', len(df), '条')
        return df.values

    def save_sql(self):
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE `carinfo`;')  # MySQL 会同时把 AUTO_INCREMENT 置 1
        for row in self.clean_csv():
            CarInfo.objects.create(
                brand=row[0], carName=row[1], carImg=row[2], saleVolume=row[3],
                price=row[4], manufacturer=row[5], rank=row[6],
                carModel=row[7], energyType=row[8], marketTime=row[9], insure=row[10]
            )
        print(f'本次入库 {len(self.clean_csv())} 条')

    def run(self):
        if os.path.exists('./temp.csv'):
            os.remove('./temp.csv')
        with open('./spiderPage.txt', 'w', encoding='utf-8') as f:
            f.write('0\n')
        self.init_csv()
        self.main()          # 爬完自动写 csv
        self.save_sql()      # 立即写库
        print('=== 本次定时任务完成 ===')

# ------------- 入口 --------------
if __name__ == '__main__':
    Spider().run()