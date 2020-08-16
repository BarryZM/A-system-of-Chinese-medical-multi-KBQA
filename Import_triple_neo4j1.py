from py2neo import Graph,Node,Relationship,NodeMatcher,RelationshipMatcher
graph = Graph("http://localhost:7474",auth=("neo4j","111111"))

def sub_entity(files):
    dic_=[]
    with open(files,"r",encoding="utf-8") as fr:
        for line in fr.readlines():
            line=line.strip()
            dic_.append(line)
    return set(dic_)

acompany=sub_entity("acompany.txt")
chech=sub_entity("check.txt")
cure_way=sub_entity("cure_way.txt")
department=sub_entity("departments.txt")
diease=sub_entity("diease.txt")
doctors=sub_entity("doctors.txt")
drugs=sub_entity("drug.txt")
food=sub_entity("food.txt")
hospitals=sub_entity("hospitals.txt")
province=sub_entity("province.txt")
symptoms=sub_entity("symptom.txt")


def creat_node():
    d=[]
    with open("MKG_triple.txt","r",encoding="utf-8") as fr:
        i=0
        for line in fr.readlines():

            line=line.strip().split("|")
            head=line[0]
            realtion=line[1]
            tail=line[2]
            d.append(head)
            d.append(tail)
    for head in set(d):
        i = i + 1
        print(i)
        if head in acompany:
            a = Node("acompany", name=head)
            graph.create(a)
        elif head in chech:
            a = Node("check", name=head)
            graph.create(a)
        elif head in cure_way:
            a = Node("cure_way", name=head)
            graph.create(a)
        elif head in department:
            a = Node("department", name=head)
            graph.create(a)
        elif head in diease:
            a = Node("diease", name=head)
            graph.create(a)
        elif head in doctors:
            a = Node("doctors", name=head)
            graph.create(a)
        elif head in drugs:
            a = Node("drugs", name=head)
            graph.create(a)
        elif head in food:
            a = Node("food", name=head)
            graph.create(a)
        elif head in hospitals:
            a = Node("hospitals", name=head)
            graph.create(a)
        elif head in province:
            a = Node("province", name=head)
            graph.create(a)
        elif head in symptoms:
            a = Node("symptoms", name=head)
            graph.create(a)
        else:
            a = Node("others", name=head)
            graph.create(a)


def build_relation():
    with open("MKG_triple.txt","r",encoding="utf-8") as fr:
        i=0
        for line in fr.readlines():
            i=i+1
            print(i)
            line=line.strip().split("|")
            head=line[0]
            realtion=line[1]
            tail=line[2]
            if head in acompany:
                a = graph.nodes.match("acompany", name=head).first()
            elif head in chech:
                a =graph.nodes.match("check", name=head).first()
            elif head in cure_way:
                a = graph.nodes.match("cure_way", name=head).first()
            elif head in department:
                a = graph.nodes.match("department", name=head).first()
            elif head in diease:
                a = graph.nodes.match("diease", name=head).first()
            elif head in doctors:
                a = graph.nodes.match("doctors", name=head).first()
            elif head in drugs:
                a = graph.nodes.match("drugs", name=head).first()
            elif head in food:
                a = graph.nodes.match("food", name=head).first()
            elif head in hospitals:
                a = graph.nodes.match("hospitals", name=head).first()
            elif head in province:
                a = graph.nodes.match("province", name=head).first()
            elif head in symptoms:
                a = graph.nodes.match("symptoms", name=head).first()
            else:
                a = graph.nodes.match("others", name=head).first()

            if tail in acompany:
                b = graph.nodes.match("acompany", name=tail).first()
            elif tail in chech:
                b = graph.nodes.match("check", name=tail).first()
            elif tail in cure_way:
                b = graph.nodes.match("cure_way", name=tail).first()
            elif tail in department:
                b = graph.nodes.match("department", name=tail).first()
            elif tail in diease:
                b = graph.nodes.match("diease", name=tail).first()
            elif tail in doctors:
                b = graph.nodes.match("doctors", name=tail).first()
            elif tail in drugs:
                b=graph.nodes.match("drugs", name=tail).first()
            elif tail in food:
                b = graph.nodes.match("food", name=tail).first()
            elif tail in hospitals:
                b = graph.nodes.match("hospitals", name=tail).first()
            elif tail in province:
                b= graph.nodes.match("province", name=tail).first()
            elif tail in symptoms:
                b = graph.nodes.match("symptoms", name=tail).first()
            else:
                b = Node("others", name=tail)

            rel_a = Relationship(a, realtion, b)
            graph.create(rel_a)

# graph.delete_all()



# graph.delete_all()
if __name__=="__main__":
    graph.delete_all()
    # creat_node()

    # build_relation()
