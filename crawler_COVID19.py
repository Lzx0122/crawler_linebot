import requests as req
import json
from bs4 import BeautifulSoup
from openpyxl import Workbook


def get_covid19():
    msg = ""
    url = "https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php"
    header = {

        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36"
    }
    request = req.get(url, headers=header)
    last_modified = request.headers.get('Last-Modified')
    print(last_modified)
    header['Last-Modified'] = last_modified
    soup = BeautifulSoup(request.text, "html.parser")

    time = soup.find(
        "span", style="font-size: 0.8em; color: #333333; font-weight: 500;").text.strip()

    text = open('timedate.txt', "r+")
    old_text = text.read()
    text.close()
    print(old_text)

    cc = soup.find(
        "h1", class_="country_confirmed mb-1 text-success").text  # 全國累積確診人數
    cr = soup.find(
        "h1", class_="country_recovered mb-1 text-info").text  # 今日新增人數
    cr_tw = soup.find_all(
        "span", class_="country_confirmed_percent")[1].text.split(" ")[1]
    print(cr_tw)  # 本土增加
    cd = soup.find(
        "h1", class_="country_deaths mb-1 text-dark").text  # 累計死亡
    cd_add = soup.find(
        "span", class_="country_deaths_change").text  # 增加死亡
    area_num_list = soup.find_all(
        "a", class_="btn btn-success btn-lg")  # 載入確診地區新增人數html
    area_list = []  # 儲存地區名
    for i in area_num_list:
        area_list.append(i.find(
            "span", style="font-size: 1em;").text.split(" ")[0])
    num_list = []  # 儲存地區新增人數
    for i in area_num_list:
        num_list.append(i.find(
            "span", style="font-size: 0.8em;").text.replace("\n", "").replace("\xa0", ""))
    new_list = []  # 有確診地區＋人數

    for i in range(len(num_list)):
        if num_list[i] != "":
            new_list.append(area_list[i]+" 新增人數："+num_list[i])
    interval_line = '=' * 23 + "\n"
    msg = "\n全國累計確診人數："+cc+"\n累計死亡："+cd+"\n增加死亡："+cd_add+"\n今日新增人數："+cr+"\n本土增加人數："+cr_tw + \
        f"\n{interval_line}"+"\n".join(new_list)
    text = open('timedate.txt', "r+")
    text.write(time)
    text.close()
    print(msg)
    return msg
