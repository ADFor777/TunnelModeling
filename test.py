from owlready2 import *

# 加载本体
onto = get_ontology("G:/TUNNEL/Tunnel.owl").load()

# 查看已有规则（可选）
for rule in list(onto.rules):
    print(rule)

