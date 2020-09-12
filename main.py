# coding: utf-8
# author: MasterPan
# email:  i@hvv.me

import re
import time
import json
import datetime
import logging
import requests.cookies
from bs4 import BeautifulSoup
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode, b64encode

PUBLIC_KEY = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDWuY4Gff8FO3BAKetyvNgGrdZM9CMNoe45SzHMXxAPWw6E2idaEjqe5uJFjVx55JW" \
             "+5LUSGO1H5MdTcgGEfh62ink/cNjRGJpR25iVDImJlLi2izNs9zrQukncnpj6NGjZu" \
             "/2z7XXfJb4XBwlrmR823hpCumSD1WiMl1FMfbVorQIDAQAB "

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/76.0.3809.100 Safari/537.36 "
}
session = requests.Session()
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# 国内热门城市数据(广州 长沙 香港 上海 武汉 重庆 北京 东莞 深圳 海外 郑州 天津 淮南)
cities = [
    {
        "name": "广州",
        "cityId": "2918"
    },
    {
        "name": "长沙",
        "cityId": "3274"
    },
    {
        "name": "香港",
        "cityId": "3314"
    },
    {
        "name": "上海",
        "cityId": "3306"
    },
    {
        "name": "武汉",
        "cityId": "3276"
    },
    {
        "name": "重庆",
        "cityId": "3316"
    },
    {
        "name": "北京",
        "cityId": "2912"
    },
    {
        "name": "东莞",
        "cityId": "2920"
    },
    {
        "name": "深圳",
        "cityId": "5"
    },
    {
        "name": "海外",
        "cityId": "6145"
    },
    {
        "name": "郑州",
        "cityId": "3242"
    },
    {
        "name": "天津",
        "cityId": "3308"
    },
    {
        "name": "淮南",
        "cityId": "3014"
    }
]
weeks_list = [
    {
        "name": "星期一",
        "value": "1",
        "alias": "一"
    },
    {
        "name": "星期二",
        "value": "2",
        "alias": "二"
    },
    {
        "name": "星期三",
        "value": "3",
        "alias": "三"
    },
    {
        "name": "星期四",
        "value": "4",
        "alias": "四"
    },
    {
        "name": "星期五",
        "value": "5",
        "alias": "五"
    },
    {
        "name": "星期六",
        "value": "6",
        "alias": "六"
    },
    {
        "name": "星期天",
        "value": "7",
        "alias": "日"
    }
]
day_list = [
    {
        "name": "上午",
        "value": ["am"]
    },
    {
        "name": "下午",
        "value": ["pm"]
    },
    {
        "name": "全天",
        "value": ["am", "pm"]
    }
]


def login(username, password) -> bool:
    url = "https://user.91160.com/login.html"
    rsa_key = RSA.importKey(b64decode(PUBLIC_KEY))
    cipher = Cipher_PKCS1_v1_5.new(rsa_key)
    username = b64encode(cipher.encrypt(username.encode())).decode()
    password = b64encode(cipher.encrypt(password.encode())).decode()
    data = {
        "username": username,
        "password": password,
        "target": "https://www.91160.com",
        "error_num": 0,
        "token": tokens()
    }
    headers["Referer"] = url
    r = session.post(url, data=data, headers=headers, allow_redirects=False)
    if r.status_code == 302:
        redirect_url = r.headers["location"]
        session.get(redirect_url, headers=headers)
        logging.info("登录成功")
        return True
    else:
        logging.error("登录失败: {}".format(check_user(data)))
        return False


def check_user(data) -> json:
    url = "https://user.91160.com/checkUser.html"
    r = session.post(url, data=data, headers=headers)
    return json.loads(r.content.decode('utf-8'))


def tokens() -> str:
    url = "https://user.91160.com/login.html"
    r = session.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find("input", id="tokens").attrs["value"]


def brush_ticket(unit_id, dep_id, weeks, days) -> list:
    now_date = datetime.date.today().strftime("%Y-%m-%d")
    url = "https://www.91160.com/dep/getschmast/uid-{}/depid-{}/date-{}/p-0.html".format(unit_id, dep_id, now_date)
    r = session.get(url, headers=headers)
    json_obj = r.json()
    if "week" not in json_obj:
        raise RuntimeError("刷票异常: {}".format(json_obj))
    week_list: list = json_obj["week"]
    week_arr = []
    for week in weeks:
        week_arr.append(str(week_list.index(week)))
    doc_ids = json_obj["doc_ids"].split(",")
    result = []
    for doc in doc_ids:
        _doc = json_obj["sch"][doc]
        for day in days:
            if day in _doc:
                sch = _doc[day]
                if isinstance(sch, list) and len(sch) > 0:
                    for item in sch:
                        result.append(item)
                else:
                    for index in week_arr:
                        if index in sch:
                            result.append(sch[index])
    return [element for element in result if element["y_state"] == "1"]


def brush_ticket_new(doc_id, dep_id, weeks, days) -> list:
    now_date = datetime.date.today().strftime("%Y-%m-%d")
    url = "https://www.91160.com/doctors/ajaxgetclass.html"
    data = {
        "docid": doc_id,
        "date": now_date,
        "days": 6
    }
    headers["Referer"] = "https://www.91160.com"
    r = session.post(url, headers=headers, data=data)
    json_obj = r.json()

    if "dates" not in json_obj:
        raise RuntimeError("刷票异常: {}".format(json_obj))

    date_list: dict = json_obj["dates"]
    week_arr = []
    for week in weeks:
        val = convert_week(week)
        key = list(date_list.keys())[list(date_list.values()).index(val)]
        week_arr.append(key)
    if len(week_arr) == 0:
        raise RuntimeError("刷票异常: {}".format(json_obj))

    doc_sch = json_obj["sch"][dep_id + "_" + doc_id]
    result = []
    for day in days:
        key = dep_id + "_" + doc_id + "_" + day
        if key in doc_sch:
            doc_sch_day = doc_sch[key]
            for week in week_arr:
                result.append(doc_sch_day[week])
    return [element for element in result if element["y_state"] == "1"]


def convert_week(w):
    for week in weeks_list:
        if week["value"] == w:
            return week["alias"]
    return ""


def get_ticket(ticket, unit_id, dep_id):
    schedule_id = ticket["schedule_id"]
    url = "https://www.91160.com/guahao/ystep1/uid-{}/depid-{}/schid-{}.html".format(unit_id, dep_id, schedule_id)
    r = session.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    data = {
        "sch_data": soup.find(attrs={"name": "sch_data"}).attrs["value"],
        "mid": soup.find(attrs={"name": "mid"}).attrs["value"],
        "accept": 1,
        "unit_id": soup.find("input", id="unit_id").attrs["value"],
        "schedule_id": ticket["schedule_id"],
        "dep_id": ticket["dep_id"],
        "time_type": ticket["time_type"],
        "doctor_id": ticket["doctor_id"],
        "detlid": soup.select('#delts li')[0].attrs["val"],
        "detlid_realtime": soup.find("input", id="detlid_realtime").attrs["value"],
        "level_code": soup.find("input", id="level_code").attrs["value"]
    }
    headers["host"] = "www.91160.com"
    headers["referer"] = url
    headers["origin"] = "https://www.91160.com"
    url = "https://www.91160.com/guahao/ysubmit.html"
    r = session.post(url, data=data, headers=headers, allow_redirects=False)
    if r.status_code == 302:
        # redirect_url = r.headers["location"]
        # if get_ticket_result(redirect_url):
        logging.info("预约成功，请留意短信通知！")
    else:
        logging.info(r.text)
        logging.info("预约失败")


def get_ticket_result(redirect_url) -> bool:
    r = session.get(redirect_url, headers=headers)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    result = soup.find(attrs={"class": "sucess-title"}).text
    return result == "预约成功"


def init_data():
    while True:
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        print("登录中，请稍等...")
        if login(username, password):
            result = {"username": username, "password": password}
            break
        else:
            print("用户名或密码错误，请重新登录！")

    print("=====请选择就医城市=====")
    print()
    for index, city in enumerate(cities):
        print("{}{}. {}".format(" " if index < 9 else "", index + 1, city["name"]))
    print()
    while True:
        city_index = input("请输入城市序号: ")
        is_number = True if re.match(r'^\d+$', city_index) else False
        if is_number and int(city_index) in range(1, len(cities) + 1):
            break
        else:
            print("输入有误，请重新输入！")

    print("=====请选择医院=====")
    print()
    url = "https://www.91160.com/ajax/getunitbycity.html"
    data = {
        "c": cities[int(city_index) - 1]["cityId"]
    }
    headers["Referer"] = "https://www.91160.com"
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    r = session.post(url, headers=headers, data=data)
    hospitals = json.loads(r.content.decode('utf-8'))
    for index, hospital in enumerate(hospitals):
        print("{}{}. {}".format(" " if index < 9 else "", index + 1, hospital["unit_name"]))
    print()
    while True:
        hospital_index = input("请输入医院序号: ")
        is_number = True if re.match(r'^\d+$', hospital_index) else False
        if is_number and int(hospital_index) in range(1, len(hospitals) + 1):
            result["unit_id"] = hospitals[int(hospital_index) - 1]["unit_id"]
            break
        else:
            print("输入有误，请重新输入！")

    print("=====请选择科室=====")
    print()
    url = "https://www.91160.com/ajax/getdepbyunit.html"
    data = {
        "keyValue": result["unit_id"]
    }
    r = session.post(url, headers=headers, data=data)
    departments = r.json()
    dep_id_arr = []
    for department in departments:
        print(department["pubcat"])
        for child in department["childs"]:
            dep_id_arr.append(child["dep_id"])
            print("    {}. {}".format(child["dep_id"], child["dep_name"]))
    print()
    while True:
        department_index = input("请输入科室序号: ")
        is_number = True if re.match(r'^\d+$', department_index) else False
        if is_number and int(department_index) in dep_id_arr:
            result["dep_id"] = department_index
            break
        else:
            print("输入有误，请重新输入！")
    headers["Referer"] = ""
    headers["Content-Type"] = ""

    print("=====请选择哪天的号=====")
    print()
    for week in weeks_list:
        print("{}. {}".format(week["value"], week["name"]))
    print()
    while True:
        week_str = input("请输入需要周几的号[可多选，如(6,7)](默认不限制): ")
        week_str = week_str if len(week_str) > 0 else ",".join(map(lambda x: str(x), list(range(1, 8))))
        result["weeks"] = week_str.split(",")
        break

    print("=====请选择时间段=====")
    print()
    for index, day in enumerate(day_list):
        print("{}. {}".format(index + 1, day["name"]))
    print()
    while True:
        day_index = input("请输入时间段序号: ")
        is_number = True if re.match(r'^\d+$', day_index) else False
        if is_number and int(day_index) in range(1, len(day_list) + 1):
            result["days"] = day_list[int(day_index) - 1]["value"]
            break
        else:
            print("输入有误，请重新输入！")

    return result


def run():
    result = init_data()
    logging.info(result)
    unit_id = result["unit_id"]
    dep_id = result["dep_id"]
    doc_id = result["doc_id"]
    weeks = result["weeks"]
    days = result["days"]
    # 刷票休眠时间，频率过高会导致刷票接口拒绝请求
    sleep_time = 10

    logging.info("刷票开始")
    while True:
        try:
            tickets = brush_ticket(unit_id, dep_id, weeks, days)
            # TODO 通过医生挂号
            if doc_id != "":
                tickets = brush_ticket_new(doc_id, dep_id, weeks, days)
        except Exception as e:
            logging.error(e)
            break
        if len(tickets) > 0:
            logging.info(tickets)
            logging.info("刷到票了，开抢了...")
            get_ticket(tickets[0], unit_id, dep_id)
            break
        else:
            logging.info("努力刷票中...")
        time.sleep(sleep_time)
    logging.info("刷票结束")


if __name__ == '__main__':
    run()
