import scrapy
import re
from covid19.items import Covid19Item


class CitydataSpider(scrapy.Spider):
    name = 'cityData'
    # allowed_domains = ['ncov.dxy.cn']
    start_urls = ['https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_aladin_banner']

    def parse(self, response):       #从Java-Script脚本中找到需要的obj类型的数据
        data=response.xpath('.//script[@id="captain-config"]').extract_first()
        caseList=re.findall('\"confirmed\"(.*?),\"caseOutsideList',data)      #亿点点预处理
        caseList=caseList[0].split(",{\"confirmed\":")
        for area_data in caseList:
            area = re.findall("area\":\"(.*?),\"subList\"", area_data)[0].strip("\"") \
                .encode('utf-8').decode("unicode_escape")  # unicode转中文
            item = Covid19Item()   #实例化items
            if "\"city\":" in area_data:   #城市列表的数据
                sub_list = re.findall("subList\":\[(.*)", area_data)  # 贪婪模式匹配不到
                city_data_list = re.findall("{(.*?)}", sub_list[0])  # 各省份所有城市的数据
                for city_data in city_data_list:
                    city_data =city_data.split(",")
                    d = {}
                    for i in city_data:
                        name=i.split(":")[0].strip("\"")     #最后的处理
                        value=i.split(":")[1].strip("\"").encode('utf-8').decode("unicode_escape")  # unicode转中文
                        d[name]=value

                    item["area"]=area
                    item["city"]=d["city"]
                    item["nativeRelative"]=d["nativeRelative"]
                    item["confirmed"]=d["confirmed"]
                    item["crued"]=d["crued"]
                    item["died"]=d["died"]
                    item["curConfirm"]=d["curConfirm"]
                    item["asymptomatic"]=d["asymptomatic"]
                    print(item)
                    yield item

            elif area!="欧洲":   #港澳台 不关心欧洲
                d={}
                for i in area_data.split(",")[1:]:
                    name = i.split(":")[0].strip("\"")  # 最后的处理
                    value = i.split(":")[1].strip("\"")
                    d[name] = value
                item["area"] = area
                item["city"] = area
                item["nativeRelative"] = d["confirmedRelative"]
                item["confirmed"] = int(d["died"])+int(d["crued"])+int(d["curConfirm"])
                item["crued"] = d["crued"]
                item["died"] = d["died"]
                item["curConfirm"] = d["curConfirm"]
                item["asymptomatic"] = d["asymptomatic"]
                print(item)
                yield item