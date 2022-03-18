# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time
import os

class Covid19Pipeline:
    csv_file=None
    now_file=None
    def open_spider(self,spider):
        f_name=time.strftime("%Y-%m-%d %H%M%S.csv",time.localtime())
        self.csv_file=open(f_name,"w",encoding="utf-8")
        self.now_file=open("now.data","w",encoding="utf-8")
        self.csv_file.write("省份/地区,城市,昨日新增,累计确诊,累计治愈,累计死亡,现存确诊,无症状感染者\n")
        self.now_file.write("省份/地区,城市,昨日新增,累计确诊,累计治愈,累计死亡,现存确诊,无症状感染者\n")
    def process_item(self, item, spider):
        self.csv_file.write("{},{},{},{},{},{},{},{}\n".format(item["area"],item["city"],item["nativeRelative"],
            item["confirmed"],item["crued"],item["died"],item["curConfirm"],item["asymptomatic"]))
        self.now_file.write("{},{},{},{},{},{},{},{}\n".format(item["area"],item["city"],item["nativeRelative"],
            item["confirmed"],item["crued"],item["died"],item["curConfirm"],item["asymptomatic"]))
        return item
    def close_spider(self,spider):
        self.csv_file.close()
        self.now_file.close()
        os.system("explorer http://127.0.0.1:5000")
        os.system("echo 若为能支持打开浏览器，请在访问127.0.0.1:5000")
        os.system("python ./echarts/main.py")
