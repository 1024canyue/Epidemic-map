from flask import Flask,render_template,jsonify
import pandas as pd
import numpy as np
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False

try:
    data=pd.read_csv(r'./now.data').replace(np.nan,0)
    sf=list(data["省份/地区"].value_counts().keys())
    sf_data=[]
    for i in sf:
        sf_data.append({
                        "name":i,
                        "value":int(data["现存确诊"][data["省份/地区"] == i].sum()),
                        "data":[
                            int(data["昨日新增"][data["省份/地区"] == i].sum()),
                            int(data["累计确诊"][data["省份/地区"] == i].sum()),
                            int(data["累计治愈"][data["省份/地区"] == i].sum()),
                            int(data["累计死亡"][data["省份/地区"] == i].sum()),
                            int(data["无症状感染者"][data["省份/地区"] == i].sum()),
                        ]
                    })
    @app.route("/")
    def index():
        index_data={
            "COVID_19_data":sf_data,
            "max":int(data["现存确诊"].max())
        }
        return render_template("index.html",**index_data)
    @app.route("/get_table_xq", methods=["GET"])
    def to_table():
        data.sort_values(by="现存确诊",ascending=False,inplace=True)
        d=[data["省份/地区"].to_list(),
           data["城市"].to_list(),
           data["昨日新增"].to_list(),
           data["累计确诊"].to_list(),
           data["累计治愈"].to_list(),
           data["累计死亡"].to_list(),
           data["现存确诊"].to_list(),
           data["无症状感染者"].to_list()
        ]
        return jsonify(d)

except:
    print("你不应该直接执行该文件!!\n请返回上层目录使用终端执行:\nscrapy crawl cityData\n\n")
    input("键入回车退出")
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
