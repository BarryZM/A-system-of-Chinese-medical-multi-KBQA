
from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher
import re

graph = Graph("http://localhost:7474",auth=("neo4j","111111"))
matcher_1= NodeMatcher(graph)
matcher_2 = RelationshipMatcher(graph)
def extract_content(r1):
    p1 = re.compile(r'[(](.*?)[)]', re.S)  #最小匹配
    freezer_kind = re.findall(p1, r1)
    return freezer_kind

def reload_dic():
    entity=[]
    ids=[]
    with open("entity_id.txt","r",encoding="utf-8") as fr:
        for line in fr.readlines():
            line=line.strip().split("\t")
            entity.append(line[0])
            ids.append(line[1])
    return dict(zip(entity,ids))

def tempalte_dic():
    t=[]
    r=[]
    with open("tempaltes.txt","r",encoding="utf-8") as fr:
        for line in fr.readlines():
            line=line.strip().split("@")
            t.append(line[0])
            r.append(line[1])
    return dict(zip(t,r))

def get_topic_entity_and_relation(sentence):
    D=reload_dic()
    topic_entity=[]
    for entity in D:
        if entity in sentence and len(entity)>1:
            topic_entity.append(entity)

    l=([len(entity) for entity in topic_entity ])

    TE=(topic_entity[l.index(max(l))])
    template=sentence.replace(TE,"")
    relation=tempalte_dic()[template]
    return TE, relation
def get_answer(sentence):

    topic_entity,relation=get_topic_entity_and_relation(sentence)
    relation=relation.split("|")[0:-1]

    # print(relation)
    node1 = matcher_1.match( name=topic_entity).first()
    r1 = matcher_2.match({node1}) # all triple which includes topic entity
    # r1=str(r1)
    # print(r1)
    d=""
    for i in list(r1):
        if relation[0] in str(i):
            i=extract_content(str(i).split("->")[1])

            d=d+i[0]+","

    d_=(d.strip(","))
    D=d_.split(",")
    end_=""
    for word in D:
        node2 = matcher_1.match(name=word).first()
        r2 = matcher_2.match({node2})

        L=""
        for j in list(r2):
            if relation[1] in str(j):
                j = extract_content(str(j).split("->")[1])

                L = L + j[0] + ","
        end_=end_+L
    end_=end_.strip(",")


    return end_.strip(",")



if __name__=="__main__":

    i=0
    sentence = ("什么人群容易患糖尿病心脏病的并发症？")

    # a=get_answer(sentence)

    while i<10:
        i=i+1
        sentence=("季惠翔在哪个医院？")
        a = input("用户:")
        a=get_answer(a)
        print("小晨:",a)
        print("*"*50)
