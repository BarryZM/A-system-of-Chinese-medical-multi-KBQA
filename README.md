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
 <img src="https://github.com/ToneLi/Some-charts-about-my-research/blob/master/medical_KG.png" width="600"/>
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
 ##### Prepare CSV files
