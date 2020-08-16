
import csv
def sub_entity(files):
    dic_=[]
    with open(files,"r",encoding="utf-8") as fr:
        for line in fr.readlines():
            line=line.strip()
            dic_.append(line)
    return set(dic_)
def entity_dic():
    word=[]
    ids=[]
    with open("entity_id.txt","r",encoding="utf-8") as fr:
        for line in fr.readlines():
            line=line.strip().split("\t")
            word.append(line[0])
            ids.append(line[1])
    return dict(zip(word,ids))

def creat_node():
    csvf_entity = open("entity.csv", "w", newline='', encoding='utf-8')
    w_entity = csv.writer(csvf_entity)
    d=[]
    combine=[]
    with open("MKG_triple.txt","r",encoding="utf-8") as fr:
        i=0
        for line in fr.readlines():
            line=line.strip().split("|")
            head=line[0]
            realtion=line[1]
            tail=line[2]
            d.append(head)
            d.append(tail)


    d=set(d)
    for word in d:
        if word in acompany:
            combine.append(word+"@"+"acompany")
        elif word in chech:
            combine.append(word + "@" + "check")
        elif word in cure_way:
            combine.append(word + "@" + "cure_way")
        elif word in department:
            combine.append(word + "@" + "department")
        elif word in diease:
            combine.append(word + "@" + "diease")
        elif word in doctors:
            combine.append(word + "@" + "doctors")
        elif word in drugs:
            combine.append(word + "@" + "drugs")
        elif word in food:
            combine.append(word + "@" + "food")
        elif word in hospitals:
            combine.append(word + "@" + "hospitals")
        elif word in province:
            combine.append(word + "@" + "province")
        elif word in symptoms:
            combine.append(word + "@" + "symptoms")
        else:
            combine.append(word + "@" + "others")
    entity_dict={}
    i=0
    # print(combine)
    w_entity.writerow((":ID", "name", ":LABEL"))
    for i in range(len(combine)):
        entity = combine[i].split("@")[0]
        pro = combine[i].split("@")[1]
        w_entity.writerow(("e" + str(i), entity, pro))
        entity_dict[entity] = "e" + str(i)
    csvf_entity.close()
    fw2=open("entity_id.txt","w",encoding="utf-8")
    for key, value in entity_dict.items():
        fw2.write(key+"\t"+value+"\n")
        fw2.flush()
if __name__=="__main__":
    acompany = sub_entity("acompany.txt")
    chech = sub_entity("check.txt")
    cure_way = sub_entity("cure_way.txt")
    department = sub_entity("departments.txt")
    diease = sub_entity("diease.txt")
    doctors = sub_entity("doctors.txt")
    drugs = sub_entity("drug.txt")
    food = sub_entity("food.txt")
    hospitals = sub_entity("hospitals.txt")
    province = sub_entity("province.txt")
    symptoms = sub_entity("symptom.txt")
    # creat_node()
    csvf_entity = open("relation.csv", "w", newline='', encoding='utf-8')
    w_entity = csv.writer(csvf_entity)
    d = []

    w_entity.writerow((":START_ID", "name", ":END_ID",":TYPE"))
    entity_dict=entity_dic()
    with open("MKG_triple.txt","r",encoding="utf-8") as fr:
        i=0
        for line in fr.readlines():
            i=i+1
            print(i)
            line=line.strip().split("|")
            head=line[0]
            relation=line[1]
            tail=line[2]
            if head not in entity_dict or tail not in entity_dict:
                continue
            else:

                w_entity.writerow((entity_dict[head], relation, entity_dict[tail],relation))