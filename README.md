# Chinese-Medical-Multi-Hop-Question-Answering
This project is about how to create a Chinese medical knowledge graph and generate the templates to answer the multi-hop question, I just use the rules to find the answer of a question in the first, more model will update.
## Introduction
Recently, many work focus on how to use knowledge graph to solve the simple question, few work about complex relations (1hop, 2hop, or more hops), expecially in Chinese. It's very important in the real application. So in this project, I build a Chinese medical knowledge graph in the first, and then create some templates for training the deep learning model or answer the question by the rules, I will provide the method about how to use rule to answer the question, at the same time the training set for deep learning model will also be provided. By this project, you will learn how to create a knowledge graph, visualize them by neo4j, and use rules to answer the complex question.
## Create Chinese medical knowledge graph
### Overview
[QASystemOnMedicalKG](https://github.com/liuhuanyong/QASystemOnMedicalKG) builds the first open Chinese medical knowledge graph for medical KGQA. Unfortunately, it just consider one hop relation and has low entity coverage.  In order to use knowledge graph in medical multi-KBQA in a more efficient way, I developed the first generation Chinese medical knowledge graph (CMKG) for multi-KBQA by expanding the relations in QASystemOnMedicalKG and  [ownthinkKG](https://github.com/ownthink/KnowledgeGraphData). For futher improving the coverage of CMKG, we fetch the relevent information about hospital and department in [DingXingYiSheng](https://dxy.com/). There are 48 relations, 305500 entities in our KG. The entities include 31 proviences, 312 citities, 1771 hospitals, 257809 doctors, 54 departments, 2205 accompanies, 3353 checks, 544 cure ways, 8806 diseases, 3800 drugs, 366 foods, 5998 symptoms, 4506 recipes, 15945 others. And the 48 relations are labeled in Graph. Given the relations and entities, I transformed them into a set of 2087309 triples. Based on these triplets , I created a dataset for Chinese medical multi-KBQA. The answer and topic entity are always the entities in CMKG. The queston can involve one, two or three triplets. 
| Entity | number|Entity | number|
| ------ | ------ |------ | ------ |
| proviences| 31 |checks| 3353  |
| citities| 312 |cure ways| 544 |
|  hospitals| 1771|diseases|8806 |
| doctors|  257809|drugs|3800 |
| departments| 54 |foods|366 |
| accompanies| 2205 |symptoms|5998 |
|recipes|4506 | others|15945 |
### Obtain infomation from DingXiangYiSheng
By BeautifulSoup and request to obtain the relevent data, full script in obtain_information_from_web.py. The triple file is Hopistal_trple.txt. little part:
```
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
```
### Triple combimation
OK, until now, I have there triple files, triple in ownthinkKG, triple in QASystemOnMedicalKG and Hopistal_trple.txt from me. I used entity in (QASystemOnMedicalKG: food.txt, department.txt, etc) at the head or tail to search the triple in ownthinkKG, by this way, I can get two hops relation. Combining the Hopistal_trple.txt  to get the CMKG file, the last triple file is MKG_triple.txt.
### Graph
In the below, there are five subgraphs, they are a part of CMKG, I use it to explain the complex relations and how to genarate the template. In these graphs, hospital, disease, food, drug are the center node.
 <img src="https://github.com/ToneLi/Some-charts-about-my-research/blob/master/MKG.png" width="1000"/>
### Visualization, Store by Neo4j
In the first , you should config the JavaJdk [Refer](https://blog.csdn.net/luobo_666/article/details/82794819), and download neo4j from [Here](https://neo4j.com/), the full progress, you can refer [Here](https://blog.csdn.net/luobo_666/article/details/82794202)
### How to import MKG_triple.txt in Neo4J
#### Method 1
In the first, I try use "for loop" in python to import the triples to Neo4J, but it failed:
```
    with open("MKG_triple.txt","r",encoding="utf-8") as fr:
        i=0
        for line in fr.readlines():

            line=line.strip().split("|")
            head=line[0]
            realtion=line[1]
            tail=line[2]
            b = Node("entity", name=head)
            c = Node("entity", name=tail)
            rel_a=Relationship(a,relation,b)
            graph.create(rel_a)
   ```
   This way can create the repeat node. For solving this, we can create the nodes in graph and then match them, add relation, full script in import_triple_neo4j1.py, this way will consume many times. So I must choose a quick method!!!
   ```
    a = Node("acompany", name=head)
     graph.create(a)
    a = graph.nodes.match("symptoms", name=tail).first()
    b = graph.nodes.match("department", name=head).first() 
    
     rel_a = Relationship(a, realtion, b)
            graph.create(rel_a)  
   ```
 #### Method 2: import CSV in to Neo4j
 In the first, we should download Neo4j server version (it's hard to download it , you can obtain it from [HERE](https://pan.baidu.com/s/1lJD57y-o3qRI-GmBxbnXNQ), code: wl9t), Note: we do not use [Desktop version](https://pan.baidu.com/s/1npJ2giwN48xX1E5hSxeenw), code:niuh. [How tp pip Neo4J in Win](https://blog.csdn.net/huanxuwu/article/details/80785986)
 ##### (1) Prepare CSV files
 Neo4j has its  unique format, if we want to input triple in Neo4j, we just use two file entity.csv and relation.csv, their for format:
 ```
 entity.csv ：
 :ID,name,:LABEL
entity0,姚明,ENTITY
entity1,周润发,ENTITY
entity2,YaoMing,ENTITY1
entity3,男,ENTITY1

relation.csv
:START_ID,name,:END_ID,:TYPE
entity0,英文名,entity2,RELATIONSHIP
entity0,性别,entity3,RELATIONSHIP

 ```
 Ok, I have given my script about how to map triple.txt into below forms. Full script in Csv_change.py
  ##### (2) Prepare database
  please choose a name for your graph database, my database is called graph1.db, the default database is "graph.db" in "neo4j-community-3.5.6\data\databases". In the next, there is a very important things, please correct your  "neo4j.conf" in neo4j-community-3.5.6\conf, the change content is:
  ```
  change before:
  #dbms.active_database=graph.db
  change after:
  dbms.active_database=graph1.db
  ```
  ##### (2) Import your relation.csv and entity relation.csv to Neo4j.
  --enter this contents: "neo4j-community-3.5.6\bin"
  ---please run:
  ```
  neo4j-admin import --mode csv --database graph1.db --nodes G:\1_Project_Li\2020_Multi_hop_KGQA\medical_data\project\entity.csv --relationships G:\1_Project_Li\2020_Multi_hop_KGQA\medical_data\project\relation.csv
  neo4j start
  neo4j stop
  neo4j.bat console
  ```
  And then, It will appear:
  ```
------
2020-08-16 09:37:06.944+0000 INFO  Started.
2020-08-16 09:37:08.129+0000 INFO  Remote interface available at http://localhost:7474/
2020-08-16 09:37:13.706+0000 WARN  The client is unauthorized due to authentication failure.
2020-08-16 10:12:45.972+0000 WARN  The client is unauthorized due to authentication failure.
  ```
In the last, we just open http://localhost:7474/. When you first open it, the default password is neo4j. Ok, it's done.
### My KG in Neo4j
<img src="https://github.com/ToneLi/Some-charts-about-my-research/blob/master/medical_KG_neo4j.png" width="800"/>
You can by "match(n) return n" to check overall graph

## Answer complex questions
I create more than 90 templates to answer the question, we all know in multi-KBQA, the first step is to make sure how to go (what's the direction of next hop), on the other hand is to choose the relation which most relevent to the question, for easy using, I labeled these templates, one template  corresponds to one relation (one hop) or two relations (two hops). So Given a question, I use entity dic to seacher the entity in sentence, make sure which template corresponds this question, at last, by topic entity and relation to get the answer. There are many work about how to choose the relations in each hop, how to stop, my work is focus on solving these problems. Please follow me about multi-KBQA!!
  
 
 
