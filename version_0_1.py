# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import datetime
import configparser
import os, sys, time

TODAY = datetime.date.today()
config = configparser.RawConfigParser()

if os.path.isfile('output.cfg') == False:
    config.add_section('kidskids')

    config.set('kidskids', 'id', 'id')
    config.set('kidskids', 'pw', 'pw')
    config.set('kidskids','age', 'age')
    config.set('kidskids','month', 'month')

    with open('output.cfg', 'w') as configfile:
        config.write(configfile)

    print("output.cfg 파일을 열어 키드키즈의 ID와 PW를 입력해주세요")
    time.sleep(3)
    sys.exit(1)

config.read('output.cfg')
ID = config.get('kidskids','id')
PW = config.get('kidskids','pw')
Age = config.get('kidskids','age')
M = config.get('kidskids','month')

exit = 0
if ID == "id":
    print("output.cfg 파일의 id 항목을 새롭게 입력해주세요")
    exit = 1

if PW == "pw":
    print("output.cfg 파일의 pw 항목을 새롭게 입력해주세요")
    exit = 1

if Age == "age":
    print("output.cfg 파일의 age 항목을 새롭게 입력해주세요")
    exit = 1

if M == "month":
    print("output.cfg 파일의 month 항목을 새롭게 입력해주세요")
    exit = 1

if exit == 1:
    time.sleep(3)
    sys.exit(1)

TODAY = datetime.date.today()

Y = int(TODAY.year)
#M = TODAY.month
#D = TODAY.day

month_daynum = [31,28,31,30,31,30,31,31,30,31,30,31]
month_day = []

for i in range(month_daynum[M-1]):
    weekend_num = int(datetime.date(Y,M,i+1).weekday())

    if (weekend_num == 5) or (weekend_num == 6):
        continue
    month_day.append(i+1)

LOGIN_INFO = {
    'member_id': ID,
    'pw': PW
}

s = requests.Session()
first_page = s.get('http://www.kidkids.net')
html = first_page.text
soup = bs(html, 'html.parser')

enc_key = soup.find(attrs={"name": "enc_key"})
refererURL = soup.find(attrs={"name": "refererURL"})

LOGIN_INFO["enc_key"] = enc_key["value"]
LOGIN_INFO["refererURL"] = refererURL["value"]

login_req = s.post('https://www.kidkids.net/regist/login_ck_file.php', data=LOGIN_INFO)
if login_req.status_code == 200:
    print("Login Success")
else:
    print("Login Fail")
    sys.exit(1)

for Day in month_day:
    D = Day
    file_name = "./output/" + str(Y)+"-"+str(M)+"-"+str(D)+".txt"
    f = open(file_name, "w")
    print(str(Y)+"년 "+str(M)+"월 "+str(D)+"일 의 자료를 output 폴더로 출력하고 있습니다.")

    base_string =  "http://www.kidkids.net/eduinfo_new/eduplan_day.htm?"
    age_string = "CUR_AGE="+str(Age)+"&"
    y_string = "SEL_YEAR="+str(Y)+"&"
    m_string = "CUR_MONTH="+str(M)+"&"
    d_string = "CUR_DAY="+str(D)+"&"

    # ------------------------------------------------------------------------------------------------

    impormation_URL = base_string + age_string + y_string + m_string + d_string
    second_page = s.get(impormation_URL)
    html_scd = second_page.content
    soup_scd = bs(html_scd, 'html.parser')

    header_parser = str(soup_scd.find("table", attrs={"class": "ep_info"}))
    header_bs = bs(header_parser, 'html.parser')
    Header_list = header_bs.find_all("tr")
    Header = []

    for paragraph in Header_list:
        process = bs(str(paragraph),'html.parser')
        title = str(process.find("th").get_text())
        contents = str(process.find("td").get_text()).replace("\t","").replace("\n","").replace("\r",", ")
        Header.append([title, contents])

    for write_file in Header:
        write_sen = str(write_file[0]) + " : " + str(write_file[1]) + "\n"
        f.write(write_sen)

#--------------------------------------------------------------------------------------------------------------

    main_parser = str(bs(str(soup_scd.find("table", attrs={"class": "plan_table mgtop_low"})), 'html.parser').find("tbody", class_="th_normal"))
    line_split = main_parser.split("\n")
    line_list = []

    if str(main_parser).find("준비중 입니다.") != -1:
        f.close()
        continue

    for readline in line_split:
        if (readline.find("<th ") == 0) or (readline.find("<h4 ") == 0):
            readline = readline.replace('<h4 style="margin-bottom:5px;">' , '')
            line_list.append(readline)

    TOTAL = []
    for readline in line_list:
        ready_parser = bs(readline, 'html.parser')
        if ready_parser == None:
            TOTAL.append(readline)
            continue
        LIST = ready_parser.find_all("th")
        if len(LIST) <= 1:
            TOTAL.append(readline)
            continue
        for JJ in LIST:
            TOTAL.append(JJ)

    root = None
    weak_root = None
    w_weak_root = []
    root_colspan = None
    weak_root_rowspan = 0

    total = []
    object = []

    for ii in TOTAL:
        A = bs(str(ii), 'html.parser')

        if weak_root_rowspan <= len(w_weak_root):
            w_weak_root = []
        if A.find("th", class_="left_none") != None:
            root_colspan = A.find("th", class_="left_none").get('colspan')
            if root_colspan != None:
                weak_root_rowspan = int(A.find("th", class_="left_none").get('rowspan'))
                weak_root = None
            root = A.find("th", class_="left_none").get_text()
        elif A.find("th", class_=False) != None and root_colspan == None:
            weak_root_rowspan = int(A.find("th", class_=False).get('rowspan'))
            weak_root = A.find("th", class_=False).get_text()
        elif A.find("a") != None:
            list_num = len(w_weak_root)
            if list_num < weak_root_rowspan:
                hab = []
                hab.append(A.find("a").get_text())
                address = "http://www.kidkids.net" + str(A.find("a").get("href"))

                third_page = s.get(address)
                html_thd = third_page.content
                soup_thd = bs(html_thd, 'html.parser')
                panel = soup_thd.find("table", class_="ep_info actdetail")

                TH = []
                TD = []

                th = bs(str(panel), 'html.parser').find_all("th")
                td = bs(str(panel), 'html.parser').find_all("td")
                for i in range(len(th)):
                    if str(th[i].get_text()).find("활동자료") != -1:
                        continue
                    TH.append(th[i].get_text())
                    TD.append(td[i].get_text())

                hab.append(TH)
                hab.append(TD)

                w_weak_root.append(hab)

            if len(w_weak_root) == weak_root_rowspan:
                object = [root, weak_root, w_weak_root]
                total.append(object)

    f.write("\n")

    Loot = str(total[0][0]) + "\n"
    f.write(Loot)

    if total[0][1] != None:
        w_Loot = "\t" + str(total[0][1]) + "\n"
        f.write(w_Loot)

    w_w_Loot = total[0][2]
    SENTENSE = []
    for zz in w_w_Loot:
        for asd in range(len(zz[2])):
            zz[2][asd] = zz[2][asd].replace("\r","").replace("\n","")
        sentense = "\t\t" + str(zz[0]) + "\n"
        f.write(sentense)
        for NI in range(len(zz[1])):
            f.write("\t\t\t" + str(zz[1][NI]) + "  :  " + str(zz[2][NI]) + "\n")
        SENTENSE = []

    f.write("\n")

    for iiii in range(1,len(total)):
        compare = str(total[iiii][0]) + "\n"
        if compare != Loot:
            Loot = str(total[iiii][0]) + "\n"
            f.write(Loot)

        if total[iiii][1] != None:
            w_Loot = "\t" + str(total[iiii][1]) + "\n"
            f.write(w_Loot)

        w_w_Loot = total[iiii][2]
        SENTENSE = []
        for zz in w_w_Loot:
            for asd in range(len(zz[2])):
                zz[2][asd] = zz[2][asd].replace("\r", "").replace("\n", "")
            sentense = "\t\t" + str(zz[0]) + "\n"
            f.write(sentense)
            for NI in range(len(zz[1])):
                f.write("\t\t\t" + str(zz[1][NI]) + "  :  " + str(zz[2][NI]) + "\n")
            SENTENSE = []

        f.write("\n")

    print(str(Y) + "년 " + str(M) + "월 " + str(D) + "일 의 자료 출력성공")
    f.close()