# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import time
import codecs
import sys

print(sys.version)
Age = 5
Y = time.localtime().tm_year
M = time.localtime().tm_mon
D = time.localtime().tm_mday

day = [31,28,31,30,31,30,31,31,30,31,30,31]

base_string =  "http://www.kidkids.net/eduinfo_new/eduplan_day.htm?"
age_string = "CUR_AGE="+str(Age)+"&"
y_string = "SEL_YEAR="+str(Y)+"&"
m_string = "CUR_MONTH="+str(M)+"&"
d_string = "CUR_DAY="+str(D)+"&"



LOGIN_INFO = {
    'member_id': 'sj0326',
    'pw': 'sjcd0326'
}

for i in range(1, day[M] + 1):
    pass
with requests.Session() as s:
    first_page = s.get('http://www.kidkids.net')
    html = first_page.text
    soup = bs(html, 'html.parser')

    enc_key = soup.find(attrs={"name": "enc_key"})
    refererURL = soup.find(attrs={"name": "refererURL"})

    LOGIN_INFO["enc_key"] = enc_key["value"]
    LOGIN_INFO["refererURL"] = refererURL["value"]

    login_req = s.post('https://www.kidkids.net/regist/login_ck_file.php', data=LOGIN_INFO)
    if login_req.status_code == 200:
        print("OK")

# ------------------------------------------------------------------------------------------------

    impormation_URL = base_string + age_string + y_string + m_string + d_string
    second_page = s.get(impormation_URL)
    html_scd = second_page.content
    soup_scd = bs(html_scd, 'html.parser')

    header_parser = str(soup_scd.find("table", attrs={"class": "ep_info"}))
    main_parser = str(soup_scd.find("table", attrs={"class": "plan_table mgtop_low"}))

    header_bs = bs(header_parser, 'html.parser')
    Header_list = header_bs.find_all("tr")
    Header = []

    for paragraph in Header_list:
        process = bs(str(paragraph),'html.parser')
        title = str(process.find("th").get_text())
        contents = str(process.find("td").get_text()).replace("\t","").replace("\n","").replace("\r",", ")
        Header.append([title, contents])

    main_bs = bs(main_parser, 'html.parser')
    Main_list = main_bs.find_all("tr")
    main_num = len(Main_list) + 1
    Main = []

    gubun = 0
    young = 0

    gubun_list = []
    young_list = []
    address_list = []

    for paragraph, cnt in zip(Main_list, range(main_num)):
        if cnt == 0:
            continue

        process = bs(str(paragraph), 'html.parser')
        start_level_list = process.find_all("th")
        b_parser = bs(str(process.find("h4")), 'html.parser').find("a")

        for parser in start_level_list:
            One = bs(str(parser), 'html.parser')
            if One.find(class_=True) != None:
                gubun_list.append(One.get_text())
                gubun += 1

                young = 0
                tmp = []

                try:
                    young_list.append(tmp)
                except NameError:
                    pass
            else:
                tmp.append(One.get_text())
                young += 1

        print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
        print("구분 : {}".format(gubun))
        print("영역 : {}".format(young))
        A = b_parser.get_text()
        B = "http://www.kidkids.net" + str(b_parser.get("href"))
        print(A)
        print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")

        if (gubun == 1) and (young == 1):
            tmp_2 = []

        tmp_2.append([A])
        print(tmp_2)

        if (young == 1) or (young == 0):
            try:
                address_list.append(tmp_2)
            except NameError:
                pass









print(gubun_list)
print(young_list)
print(address_list)