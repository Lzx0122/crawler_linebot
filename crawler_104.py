import requests as req
import json
from bs4 import BeautifulSoup


def notifybot():
    headers = {
        "Authorization": "Bearer " + "r4J0BaYHj4yruCRVdO490gxrrUhkjaYQQegqKwi2cBP",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {"message": "測試"}
    r = req.post("https://notify-api.line.me/api/notify",
                 headers=headers, params=params)


def get_104(inputlist):
    d104 = {
        "台北市": "6001001000",
        "新北市": "6001002000",
        "桃園市": "6001005000",
        "台中市": "6001008000",
        "彰化縣": "6001010000",
        "台南市": "6001014000",
        "高雄市": "6001016000"
    }
    arealist = inputlist[2].split(',')
    for i in range(len(arealist)):
        arealist[i] = d104[arealist[i]]

    strbox = ""

    for i in range(int(inputlist[3])):
        i += 1
        strbox += "\n頁數"+str(i)+":---------------\n\n"
        url = "https://www.104.com.tw/jobs/search/list?ro=0&isnew=0&kwop=7&keyword="+inputlist[1]+"&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&area="+",".join(arealist)+"&order=12&asc=0&page=" + \
            str(i)+"&mode=s&langFlag=0&langStatus=0&recommendJob=1&hotJob=1"
        header = {

            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
            "Cookie": "_T_MYPOOL_104I=1; luauid=1856058949; __auc=e2a4b43617fc089e8bc3555acf6; _gid=GA1.3.998545743.1648202738; _gcl_au=1.1.1205875470.1648210440; ALGO_EXP_6019=C; ALGO_EXP_12509=G; lup=1856058949.5001489413863.4623532291991.1.4507568175053; lunp=4623532291991; TS016ab800=01180e452d8660dfd738016151c3f15d8b58f9918a1302be5327335e918dbc6e071406788d496ae3c059aedc230fdef409766a17b9341963e66abdd39f38a692c822c4b95dcca090104d76c9b207a0407a9d6d0ace; __asc=2d4c1b7d17fc4554417b552a4a4; _dc_gtm_UA-15276226-1=1; _ga_W9X1GB1SVR=GS1.1.1648266396.3.1.1648266408.48; _ga_FJWMQR9J2K=GS1.1.1648266396.4.1.1648266408.48; _ga=GA1.3.1948524712.1648202738",
            "Referer": "https://www.104.com.tw/jobs/search/"}
        request = req.get(url, headers=header)

        data = request.json()
        print(data)

        for i in data["data"]["list"]:
            try:
                appearDateDesc = i["appearDateDesc"]  # 上傳時間
                coIndustryDesc = i["coIndustryDesc"]  # 工作類別
                description = i["description"]  # 工作需求
                jobAddrNoDesc = i["jobAddrNoDesc"]+i["jobAddress"]  # 工作地點
                salaryDesc = i["salaryDesc"]  # 薪水
                link = i["link"]["job"]  # 連結
                strbox += i["jobName"] + \
                    f"\n----------------------\n上傳時間:{appearDateDesc}\n薪資：{salaryDesc}\n工作地點:{jobAddrNoDesc}\n類別：{coIndustryDesc}\n連結:{link}\n=======================\n"
                strbox += f"{description}" + \
                    "\n=======================\n\n❤️🧡❤️🧡❤️🧡❤️🧡❤️\n\n"
            except Exception as e:
                print(e)
    try:

        return strbox.replace("&lt;", "<").replace("&gt;", ">")
    except Exception as e:
        print(e)
        # 呼叫notify
        # notifybot()
