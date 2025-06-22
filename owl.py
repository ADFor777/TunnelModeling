from rdflib import Graph, Namespace

g = Graph()
g.parse("G:/TUNNEL/Tunnel.owl")

SWRL = Namespace("http://www.w3.org/2003/11/swrl#")

for rule in g.subjects(predicate=None, object=SWRL["Imp"]):
    print(f"📘 找到 SWRL 规则：{rule}")

