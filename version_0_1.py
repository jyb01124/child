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


    header_parser = soup_scd.find("table", attrs={"class": "ep_info"})
    main_parser = soup_scd.find("table", attrs={"class": "plan_table mgtop_low"})

    #print(header_parser)
    #print(main_parser)



    A = soup_scd.find("table", attrs={"summary": "일간교육계획안 정보"}).find_all("th")
    B = soup_scd.find("table", attrs={"summary": "일간교육계획안 정보"}).find_all("td")

    main_important = {}
    for i,j in zip(A,B):
        main_important[i.get_text()] = str(j.get_text()).replace("\n\t","").replace("\t","").replace(".\r\n",", ")

    print(main_important)

    C = soup_scd.find("tbody", attrs={"class": "th_normal"})
    D = soup_scd.find("tbody", attrs={"class": "th_normal"}).find_all("h4", style="margin-bottom:5px;")

    Left_0 = C.find_all("th", attrs={"class": "left_none"})
    Left_1 = C.find_all("th", class_=False)

    Left_1.insert(4, bs('<th rowspan="0" scope="row">수/조작영역</th>', 'html.parser').find('th'))
    Left_1.append(bs('<th rowspan="1" scope="row">실외</th>', 'html.parser').find('th'))
    Left_1.append(bs('<th rowspan="1" scope="row">실외대체</th>', 'html.parser').find('th'))

    i_rowspan = 0
    j_rowspan = 0
    cnt = 0

    title = {}

    for i in range(len(Left_0)):
        i_rowspan = int(Left_0[i]['rowspan'])
        Z = []
        tmp = cnt
        AAA = len(Left_1)
        for j in range(tmp, AAA):
            j_rowspan += int(Left_1[j]['rowspan'])
            if i_rowspan >= j_rowspan:
                AA = {}
                AA[Left_1[j].get_text()] = [str(D[j].get_text()).replace("\n",""), "http://www.kidkids.net"+str(bs(str(D[j]), 'html.parser').find('a').get("href"))]

                third_page = s.get(str(AA[Left_1[j].get_text()][1]))
                html_thd = third_page.content
                soup_thd = bs(html_thd, 'html.parser')
                DDD = soup_thd.find(string='활동개요')
                AA[Left_1[j].get_text()].append(DDD.find_parent("tr").find("td").get_text())

                Z.append(AA)
                cnt += 1
            else:
                break

        j_rowspan = 0
        title[Left_0[i].get_text()] = Z

    print(title)


f = codecs.open("output.txt", 'w', encoding='utf8')
f.write("연령/기간 : " + str(main_important['연령/기간'])+"\n")
f.write("생활주제 : " + str(main_important['생활주제'])+"\n")
f.write("주제 : " + str(main_important['주제'])+"\n")
f.write("소주제 : " + str(main_important['소주제'])+"\n")
f.write("목표 : " + str(main_important['목표'])+"\n")
f.write("\n")
f.write("자유선택활동 : ")
f.write("\n쌓기 영역 : " + str(title['자유선택활동'][0]['쌓기영역'][0])+"\n")
f.write(str(title['자유선택활동'][0]['쌓기영역'][2])+"\n")
f.write("\n역할 영역 : " + str(title['자유선택활동'][1]['역할영역'][0])+"\n")
f.write(str(title['자유선택활동'][1]['역할영역'][2])+"\n")
f.write("\n언어 영역 : " + str(title['자유선택활동'][2]['언어영역'][0])+"\n")
f.write(str(title['자유선택활동'][2]['언어영역'][2])+"\n")
f.write("\n수/조작 영역 : " + str(title['자유선택활동'][3]['수/조작영역'][0])+"\n")
f.write(str(title['자유선택활동'][3]['수/조작영역'][2])+"\n")
f.write("\n수/조작 영역 : " + str(title['자유선택활동'][4]['수/조작영역'][0])+"\n")
f.write(str(title['자유선택활동'][4]['수/조작영역'][2])+"\n")
f.write("\n음률 영역 : " + str(title['자유선택활동'][5]['음률영역'][0])+"\n")
f.write(str(title['자유선택활동'][5]['음률영역'][2])+"\n")
f.write("\n미술 영역 : " + str(title['자유선택활동'][6]['미술영역'][0])+"\n")
f.write(str(title['자유선택활동'][6]['미술영역'][2])+"\n")
f.write("\n과학 영역 : " + str(title['자유선택활동'][7]['과학영역'][0])+"\n")
f.write(str(title['자유선택활동'][7]['과학영역'][2])+"\n")
f.write("\n")
f.write("대소집단활동 : ")
print("--------------------------------------")
print()
f.write("\n이야기 나누기 : " + str(title['대소집단활동'][0][list(title['대소집단활동'][0].keys())[0]][0])+"\n")
f.write(str(title['대소집단활동'][0]['이야기나누기'][2])+"\n")
f.write("\n음악 : " + str(title['대소집단활동'][1]['음악'][0])+"\n")
f.write(str(title['대소집단활동'][1]['음악'][2])+"\n")
f.write("\n")
f.write("실외 놀이 : ")
f.write("\n실외 : " + str(title['실외놀이'][0]['실외'][0])+"\n")
f.write(str(title['실외놀이'][0]['실외'][2])+"\n")
f.write("\n실외 대체 : " + str(title['실외놀이'][1]['실외대체'][0])+"\n")
f.write(str(title['실외놀이'][1]['실외대체'][2])+"\n")



f.close()


