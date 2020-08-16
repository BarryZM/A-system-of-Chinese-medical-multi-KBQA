#__anthor__==Mingchen Li, GSU

from bs4 import BeautifulSoup
import requests
from urllib import request

"""
# this script is used to obtain---
--province
    --city 市
        -- the hospital in this city
            ----the tel of this hospital
            -----the address of this hospital
            ----the department (科室)
                ----doctor,etc
            ----good department (擅长科室)
the output file is all_information_end.txt, I obtained 1771 hospital's information
"""



def provience_w():
    fw=open("provience_and_web.txt","w",encoding="utf-8")
    html = requests.get('https://dxy.com/health/hospital/location/620000')
    # print(html.text)
    soup = BeautifulSoup(html.content,"html.parser")
    # print(soup.text)
    province_website=soup.find_all("ul",class_="nav-ul clearfix")

    web=[]
    province_name=[]
    for p in (province_website[0].find_all("li")):
        web.append("https://dxy.com"+(p.find_all("a")[0]["href"]))
        province_name.append(p.get_text())

    PW=dict(zip(province_name,web))
    for key, value in PW.items():
        fw.write(key+"\t"+value+"\n")

    # return PW

def read_proviecne_web():
    pro=[]
    web=[]
    with open("provience_and_web.txt","r",encoding="utf-8") as fr:
        for line in fr.readlines():
            line=line.strip().split("\t")
            pro.append(line[0])
            web.append(line[1])
    dic_=dict(zip(pro,web))
    return  dic_

def city_hospivcal():
    fw=open("procinece_city_hospital_web.txt","w",encoding="utf-8")
    PW=read_proviecne_web()
    for key, value in PW.items():
        provience_name=key
        provience_web=value
        # print(provience_web)
        # provience_web=request.urlopen(provience_web)
        html = request.urlopen(provience_web)
        # print(html.text)
        soup = BeautifulSoup(html, "html.parser")
        all_citys=soup.find_all("ul", class_="content-region j-hospital-region ")[0].find_all("li",class_="clearfix")

        for ci in all_citys:
            city=ci.find_all("h4")[0].get_text().strip()
            hospitals=ci.find_all("ul")
            # print(hospitals)
            for hospital in hospitals:
                print(hospital)
                hospital_name_webs=hospital.find_all("a")
                for hnw in hospital_name_webs:
                    name =provience_name.strip()+"|"+city+"|"+hnw.get_text()
                    web="https://dxy.com"+hnw["href"]
                    fw.write(name+"|"+web+"\n")


def obtain_department(id):
    """
    this script is used to obtain the deparment name
    :param id:  id is the hopital id
    :return:
    """
    all_ds = ""
    for i in range(5):
        i = i + 1
        URL = "https://dxy.com/view/i/hospital/section/list?page_index=%s&items_per_page=20&id=%s" % (str(i),str(id))
        html = request.urlopen(URL)
        soup = BeautifulSoup(html, "html.parser")

        if "error" in str(soup):
            continue
        else:
            dic_ = eval(soup.text)
            all_departments = (dic_["data"]["items"])
            for ds in all_departments:
                # print(ds)
                all_ds=all_ds+(ds["name"] + "&" +str(ds["hospital_id"])+"&" + str(ds["section_id"])+"&"+str(ds["doctor_number"]))+"**"
    return all_ds


def hospital_information():
    fw=open("all_information_1.txt","w",encoding="utf-8")
    i=0
    with open("procinece_city_hospital_web.txt","r",encoding="utf-8") as fr:
        for line in fr.readlines():
            i=i+1
            print(i)
            L=line.strip().split("|")
            hospital_web=L[-1].strip()

            fw.write(L[0]+"|"+L[1]+"|"+L[2]+"|")
            # print(hospital_web)

            html = request.urlopen(hospital_web)
            # try:
            #     html = request.urlopen(hospital_web)
            # except urllib.error.URLError as e:
            #     print(e)
            # print(html)

            hospital_content = BeautifulSoup(html, "html.parser")

            # grade such as 三级甲等
            grade=hospital_content.find_all("span",class_="grade")[0].get_text().strip().replace("(","").replace(")","")

            fw.write(grade+"|")
            #ensure 医保定点
            ensure=hospital_content.find_all("span",class_="ensure")[0].get_text().strip()
            fw.write(ensure + "|")
            # site  地址
            site= hospital_content.find_all("span", class_="hospital-basic__info")[0].get_text().strip()
            fw.write(site+"|")
            # tel 电话
            tel = hospital_content.find_all("span", class_="hospital-basic__info")[1].get_text().strip()
            fw.write(str(tel) + "|")
            # print(tel)
            # print(site)
            if "擅长专长" in str(hospital_content):
                good_department = hospital_content.find_all("div", class_="hospital-detail-intro")[0].get_text().strip()
                # print(good_department
            else:
                good_department="擅长专长未登录"
            fw.write(good_department+"|")
            hospital_id=hospital_web.split("/")[-1]
            # print(hospital_id)
            # 科&1666&11&11  hospital_id section_id, doctor_number
            department_name=obtain_department(hospital_id)
            fw.write(department_name+"\n")
            fw.flush()


def obtain_doctor_information(hospital_id,section_id):
    all_ds = ""
    for i in range(5):
        i = i + 1
        # print(i)
        URL = "https://dxy.com/view/i/section/doctor/list?hospital_id=%s&section_id=%s&page_index=%s&items_per_page=6" % (str(hospital_id),str(section_id),str(i))
        # print(URL)
        html = request.urlopen(URL)
        soup = BeautifulSoup(html, "html.parser")

        if "error" in str(soup):
            continue
        else:
            dic_ = eval(soup.text)
            all_doctors = (dic_["data"]["items"])
            for doctor in all_doctors:
                doctor_name = doctor["name"]
                jobtile = doctor["jobtitle_type_name"]
                all_ds = all_ds + (doctor_name + "-NJ-" + jobtile) + "$"
    return all_ds



def department_information():
    fw=open("all_information_end_4.txt","w",encoding="utf-8")
    with open("all_information_4.txt","r",encoding="utf-8") as fr:
        i=0
        for line in fr.readlines():
            i=i+1
            print(i)
            line=line.strip().split("|")
            fw.write(line[0]+"|"+line[1]+"|"+line[2]+"|"+line[3]+"|"+line[4]+"|"+line[5]+"|"+line[6]+"|"+line[7]+"|")
            department=line[8]
            departments=department.split("**")[:-1]
            for de in  departments:

                de=de.split("&")
                department_name=de[0]
                fw.write(department_name+"-DD-")
                hospital_id=de[1]
                section_id=de[2]
                doctors=obtain_doctor_information(hospital_id,section_id)
                fw.write(doctors+"&")
            fw.write("\n")
            fw.flush()


if __name__=="__main__":
    # hospital_information()
    department_information()
