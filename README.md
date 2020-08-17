# Chinese-Medical-Multi-Hop-Question-Answering
This project is about how to create a Chinese medical knowledge graph and generate the templates to answer the multi-hop question, I just use the rules to find the answer of a question, more model will update. The relevant data in[Here](https://pan.baidu.com/s/1J8Ef5wRHlypB7u7SFIHWlQ), code:2kgx, if you find you cannot find the files, please contact me.
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
 In the first, we should download Neo4j server version (it's hard to download it , you can obtain it from [HERE](https://pan.baidu.com/s/1LgFwNNp5JWBQy-JwpZRMZA), code: dout, Note: we do not use [Desktop version](https://pan.baidu.com/s/1npJ2giwN48xX1E5hSxeenw), code:niuh. [How tp pip Neo4J in Win](https://blog.csdn.net/huanxuwu/article/details/80785986)
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
I create more than 90 templates to answer the question (you can check templates.pdf), we all know in multi-KBQA, the first step is to make sure how to go (what's the direction of next hop), on the other word, it is to choose the relation which most relevent to the question, for easy using, I labeled these templates, one template  corresponds to one relation (one hop) or two relations (two hops). So Given a question, I use entity dic to seacher the entity in sentence, make sure which template corresponds this question, at last, by topic entity and relation to get the answer. There are many work about how to choose the relations in each hop, how to stop, my work is focus on solving these problems. Please follow me about multi-KBQA!!
## One hop-Simple QA 
the code in Get_answer_1hop.py

```
用户:在哪个医院可以找到季惠翔？
小晨: 第三军医大学第一附属医院
**************************************************
用户:我住在兰州市，咱家乡有哪些医院呢
小晨: 甘肃省中医院,甘肃省康复中心医院,兰州西固区中医院,甘肃省劳改局兰州医院,甘肃中医学院附属医院,兰州军区总医院安宁分院,兰州军区总医院,兰州大学口腔医院,兰州市第二人民医院,兰州大学第二医院,甘肃省人民医院,甘肃省肿瘤医院,兰州第一人民医院,兰州大学第一医院,兰州市窑街煤电公司医院,兰州大学附属天浩医院,甘肃省第二人民医院
**************************************************
用户:我得了麻疹，该去哪个科？
小晨: 感染科
**************************************************
用户:兰州市窑街煤电公司医院比较好的科是什么？
小晨: 心血管内科,消化科,创伤骨科,神经内科
**************************************************
用户:兰州市窑街煤电公司医院是什么等级的？
小晨: 三级乙等
**************************************************
用户:兰州市窑街煤电公司医院是医保定点单位吗？
小晨: 医保定点
**************************************************
用户:兰州市有哪些医院？
小晨: 甘肃省中医院,甘肃省康复中心医院,兰州西固区中医院,甘肃省劳改局兰州医院,甘肃中医学院附属医院,兰州军区总医院安宁分院,兰州军区总医院,兰州大学口腔医院,兰州市第二人民医院,兰州大学第二医院,甘肃省人民医院,甘肃省肿瘤医院,兰州第一人民医院,兰州大学第一医院,兰州市窑街煤电公司医院,兰州大学附属天浩医院,甘肃省第二人民医院
**************************************************
用户:兰州大学第二医院的电话是多少？
小晨: 0931-8458109
**************************************************
用户:围绝经期综合征又可以叫做什么？
小晨: 更年期综合征
**************************************************
用户:麻疹传人吗？
小晨: 麻疹是儿童最常见的急性呼吸道传染病之一，其传染性很强，在人口密集而未普种疫苗的地区易发生流行，2～3年一次大流行。
**************************************************
用户:儿童孤独症最容易在哪些人群中发生？
小晨: 男性婴幼儿
**************************************************
用户:皮脂腺囊肿又可以叫做什么？
小晨: 粉瘤，粉刺
**************************************************
用户:血友病有什么现象？
小晨: 出血倾向,反复出血,骨质破坏,血尿,异常子宫出血,黑便,肌肉萎缩,腹痛,鼻衄
**************************************************
用户:百日咳不可以吃什么食物？
小晨: 海螺,螃蟹,海虾,海蟹
**************************************************
用户:外阴纤维瘤，可以吃什么食物？
小晨: 芝麻,咸鸭蛋,白酒,干腌菜,乌骨鸡,油豆腐,杏仁,鸡血
**************************************************
用户:可以吃什么药来缓解百日咳？
小晨: 红霉素肠溶片,环酯红霉素片,百咳静糖浆,琥乙红霉素片,琥乙红霉素颗粒,穿心莲内酯片
**************************************************
用户:喘息样支气管炎吃什么药？
小晨: 蛇胆川贝液,氨茶碱片,胸腺肽肠溶片,布地奈德气雾剂,二羟丙茶碱片,硫酸沙丁胺醇片,硫酸沙丁胺醇气雾剂,小青龙颗粒,喷托维林氯化铵糖浆,小青龙合剂,枸橼酸喷托维林片
**************************************************
```
## Two hop-complex QA 
In Get_answer_2hop.py

```
用户:什么人群容易患糖尿病心脏病的并发症？
小晨: 40岁以上男性,心脏病患者
**************************************************
用户:什么人群容易患由糖尿病心脏病引起的疾病？
小晨: 40岁以上男性,心脏病患者
**************************************************
用户:手外伤的并发症传染吗？
小晨: 无
**************************************************
用户:医生我得了炭疽推荐的食物中含有防腐剂吗？
小晨: 否
**************************************************
用户:当患有锁骨下动脉-腋动脉瘤时，医生推荐的食物都适合什么人群？
小晨: 体质虚弱，食欲不振，发热，水肿,老少皆宜
**************************************************
用户:治疗骶骨骨折的药有什么化学成分？
小晨: 三七
**************************************************
用户:治疗蛋白丢失性胃肠病的药有什么化学成分？
小晨: 木香、砂仁、醋香附、槟榔、甘草、陈皮、厚朴、枳壳(炒,太子参，陈皮，山药，麦芽（炒），山楂,木香，砂仁，白术，陈皮，茯苓，半夏（制），醋香附，枳实（炒），豆蔻（去壳），姜厚朴，广藿香，甘草
**************************************************
用户:治疗蛋白丢失性胃肠病的药，有什么规格的？
小晨: 每100丸重6g,片剂，每片重（1）0.8克或（2）0.5克,口服，可以咀嚼。规格（1）一次3片，一日3次。规格（2）成人一次4-6片，儿童二岁至四岁一次2片，五岁至八岁一次3片，九岁至十四岁一次4片；一日三次。小儿酌减,水丸，每袋9克；9g*10袋
**************************************************
用户:如何使用治疗小儿肺出血-肾炎综合征的药？
小晨: 口服，一次15～20毫升.一日3次，用时摇匀,口服，一次6～9克，一日2次
**************************************************
用户:治疗卵泡发育不良的药是处方药吗？
小晨: 处方药
**************************************************
```
 ## Conclution
 By this project, you can learn how to use rule to complete the medical multi-KBQA. It is worth noting that, this method only answer the one type complex question, two topic entity, the answer in the middle of reasoning path cannot be solved. I have made a Chinese medical multi-KBQA, for training the data to solve above problem, if you are interested in this topic, you can contact me anytime!
 
