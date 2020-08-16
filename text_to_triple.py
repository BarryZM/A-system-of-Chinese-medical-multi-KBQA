#__anthor__==Mingchen Li, GSU
"""
this script is used the change the file all_information_end.txt into triple
output file
"""
def To_triple():
    fw=open("Hospital_triple.txt","w",encoding="utf-8")
    with open("all_information_end.txt","r",encoding="utf-8") as fr:
        provience_all=[]
        city_all=[]
        hospital_all=[]
        doc_all_=[]
        departments_all=[]
        i=0
        for line in fr.readlines():
            i=i+1
            print(i)
            line=line.strip().split("|")
            provience=line[0]
            provience_all.append(provience)
            city=line[1]
            city_all.append(city)
            hospital=line[2]
            hospital_all.append(hospital)
            # city_all
            level=line[3]
            Yibao=line[4]
            site=line[5]
            tel=line[6]

            fw.write(provience+"|"+"市"+"|"+city+"\n")
            fw.write(city + "|" + "所属省份" + "|" + provience + "\n")

            fw.write(hospital + "|" + "医保定点" + "|" + Yibao + "\n")
            fw.write(hospital + "|" + "等级" + "|" + level + "\n")
            fw.write(hospital + "|" + "所属地区" + "|" + city + "\n")
            fw.write(city + "|" + "有医院" + "|" + hospital + "\n")

            fw.write(hospital + "|" + "电话" + "|" + tel + "\n")
            fw.write(hospital + "|" + "地址" + "|" + site + "\n")

            good_department=line[7].split("、")
            for gd in good_department:
                fw.write(hospital + "|" + "擅长" + "|" + gd + "\n")

            departments=[]
            doctors_all=[]
            department_doctors=line[8].split("&")[0:-1]
            # print(department_doctors)
            for DD in department_doctors:
                # print(DD)

                departmet=DD.split("-DD-")[0]
                departments.append(departmet)
                doctors=DD.split("-DD-")[1].split("$")[0:-1]
                department_doctor=[]
                for DZ in doctors:

                    DZ=DZ.split("-NJ-")
                    doctor=DZ[0]
                    doctors_all.append(doctor)
                    department_doctor.append(doctor)
                    position=DZ[1]
                    fw.write(doctor + "|" + "职位" + "|" + position + "\n")

                department_doctor=set(department_doctor)
                for dd in department_doctor:
                    fw.write(departmet + "|" + "有专家" + "|" + dd + "\n")
                    fw.write(dd + "|" + "所属科室" + "|" + departmet + "\n")


            departments=set(departments)
            for de in departments:
                departments_all.append(de)
                fw.write(hospital + "|" + "科室" + "|" + de + "\n")
                # fw.write(de + "|" + "所属医院" + "|" + hospital+ "\n")

            doctors_all=set(doctors_all)
            for dr in doctors_all:
                doc_all_.append(dr)
                fw.write(hospital + "|" + "专家" + "|" + dr + "\n")
                fw.write(dr + "|" + "所属医院" + "|" + hospital + "\n")

        print("the number of provience",len(set(provience_all)))
        print("the number of city",len(set(city_all)))
        print("the number of hospital",len(hospital_all))
        print("the number of doc",len(doc_all_))
        print("the number of department",len(set(departments_all) ))

def re_difine_jiuzheng_department():

    fw=open("Hospital_triple2.txt","w",encoding="utf-8")
    with open("diease_1hop.txt","r",encoding="utf-8") as fr:
        i=0
        for line in fr.readlines():
            i = i + 1
            # print(i)
            lin = line.strip().split("|")
            if lin[1]=="就诊科室":
                S=lin[2].replace("，","、")
                DP=S.split("、")
                for D in DP:
                    fw.write(D+ "|" + "疾病" + "|" + lin[0] + "\n")
                    fw.write(lin[0]+"|"+"就诊科室"+"|"+D+"\n")

if __name__=="__main__":
    # To_triple()
    re_difine_jiuzheng_department()