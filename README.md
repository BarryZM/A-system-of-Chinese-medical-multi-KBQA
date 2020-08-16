# Chinese-Medical-Multi-Hop-Question-Answering
This project is about how to create a Chinese medical knowledge graph and generate the templates to answer the multi-hop question, I just use the rules to find the answer of a question in the first, more model will update.
## Introduction
Recently, many work focus on how to use knowledge graph to solve the simple question, few work about complex relations (1hop, 2hop, or more hops), expecially in Chinese. It's very important in the real application. So in this project, I build a Chinese medical knowledge graph in the first, and then create some templates for training the deep learning model or answer the question by the rules, I will provide the method about how to use rule to answer the question, at the same time the training set for deep learning model will also be provided. By this project, you will learn how to create a knowledge graph, visualize them by neo4j, and use rules to answer the complex question.
## Create Chinese medical knowledge graph
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

In the below, there are five subgraphs, they are a part of CMKG,
 <img src="https://github.com/ToneLi/Some-charts-about-my-research/blob/master/medical_KG.png" width="600"/>
 I use it to explain the complex relations and how to genarate the template. In these graphs, hospital, disease, food, drug are the center node.
