# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import time
from tree import Tree
import sys

print(sys.version)
Age = 5
Y = time.localtime().tm_year
#M = time.localtime().tm_mon
M=5
#D = time.localtime().tm_mday
D=31

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
    header_bs = bs(header_parser, 'html.parser')
    Header_list = header_bs.find_all("tr")
    Header = []

    for paragraph in Header_list:
        process = bs(str(paragraph),'html.parser')
        title = str(process.find("th").get_text())
        contents = str(process.find("td").get_text()).replace("\t","").replace("\n","").replace("\r",", ")
        Header.append([title, contents])

#--------------------------------------------------------------------------------------------------------------

    main_parser = str(bs(str(soup_scd.find("table", attrs={"class": "plan_table mgtop_low"})), 'html.parser').find("tbody", class_="th_normal"))
    line_split = main_parser.split("\n")
    line_list = []

    for readline in line_split:
        if (readline.find("<th ") == 0) or (readline.find("<h4 ") == 0):
            readline = readline.replace('<h4 style="margin-bottom:5px;">' , '')
            line_list.append(readline)

    front = line_list[0].find("</th>") 
    back_string = "<th "
    space = " "
    locate = 0

    for space_num in range(10):
        locate = line_list[0].find(">" + back_string)
        if locate != -1:
            break
        back_string = space + back_string

    rtn = (">" + back_string).replace("th ","")

    for value in line_list:
        INDEX = line_list.index(value)

        if value.find(rtn) == -1:
            continue
        tmp = value.split(rtn)
        del line_list[INDEX]
        line_list.insert(INDEX, tmp[0]+">")
        line_list.insert(INDEX+1, "<"+tmp[1])

    for ii in line_list:        
        A = bs(ii,'html.parser')
        A.
    



    '''
                readlines = readline.split('> <')
            if len(readlines) == 2:
                line_list.append(readlines[0] + ">")
                line_list.append("<" + readlines[1])
            elif len(readlines) == 1:
                line_list.append(readline)
    '''
    


    




'''

main_parser = bs(main_parser, 'html.parser')

    root = main_parser.find("th", class_="left_none")
    week_root = None
    week_week_root = None

    past = None
    present = None

    present = root

    if present.find_next("th").get('class') == None:
        print("소주제")
        week_root = present.find_next("th")
        past = present
        present = week_root
    else:
        print("주제")
        root = present.find_next("th")
        past = present
        present = root
        continue
    
    if present.find_next()
    
    print(root.find_next("h4"))

    first = bs(main_parser,'html.parser').find("th", class_="left_none")
    first_span = first.get('rowspan')

    tmp = first.find_next("th")
    while True:
        if tmp.get('class') != None:
            break
        tmp_num = tmp.get('rowspan')
        if tmp_num == 1:
            pass

    print(first.find_next("th").get('rowspan'))
    print(first.find_next("h4").get_text())





'''
























'''

    main_bs = bs(main_parser, 'html.parser')
    Main_list = main_bs.find_all("tr")
    main_num = len(Main_list) + 1
    Main = []

    gubun = 0
    young = 0

    gubun_list = []
    young_list = []
    address_list = []

    past = 0
    present = 0

    for paragraph, cnt in zip(Main_list, range(main_num)):
        
        if cnt == 0:
            continue

        needs = bs(str(paragraph), 'html.parser')

        th = needs.find_all('th')
        th_num = len(th)

        h4 = needs.find_all('h4', style="margin-bottom:5px;")
        for h4_indi in h4:
            a = bs(str(h4_indi),'html.parser').find('a')
            a_address = a.get('href')
            a_text = a.get_text()
            #print(a_text)
            #print(a_address)
        #a_num = len(a)

        print("th_num: {}".format(th_num))


        #print("a_num: {}".format(a_num))


'''






'''
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
            
        try:
            tmp_2.append([A])
            print(tmp_2)
        except:
            pass

        if (young == 1) or (young == 0):
            try:
                address_list.append(tmp_2)
                tmp_2 = []
            except NameError:
                pass









#print(gubun_list)
#print(young_list)
print(address_list)

'''