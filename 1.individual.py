from rdflib import Graph, Namespace, RDF, RDFS, Literal
from rdflib.namespace import OWL

# 加载本体
g = Graph()
g.parse("Tunnel_RDF.owl", format="xml")

# 命名空间（务必加 #）
MY = Namespace("http://www.semanticweb.org/lenovo/ontologies/2025/5/untitled-ontology-10")
XSD = Namespace("http://www.w3.org/2001/XMLSchema")

# 要提取的类型，比如你的实际个体可能属于 UrbanTunnelProject 等
TARGET_CLASSES = {"TunnelProject"}  # 可根据你的本体扩展

# 存储结构
individuals = {}

# Step 1: 提取你的真实个体（排除 swrl:Variable）
for s, p, o in g.triples((None, RDF.type, None)):
    s_str = str(s)
    o_str = str(o)

    if s_str.startswith(MY) and o_str.startswith(MY):
        class_name = o_str.split("#")[-1]

        # ✅ 只提取指定类型的个体（比如 UrbanTunnelProject）
        if class_name in TARGET_CLASSES:
            name = s_str.split("#")[-1]
            individuals[name] = {
                "uri": s,
                "type": [class_name],
                "obj_props": {},
                "data_props": {}
            }

# Step 2: 遍历三元组，填充属性
for s, p, o in g:
    s_str = str(s)
    if s_str.startswith(MY):
        name = s_str.split("#")[-1]
        if name not in individuals:
            continue

        p_str = str(p).split("#")[-1]

        if isinstance(o, Literal):
            individuals[name]["data_props"][p_str] = str(o)
        elif str(o).startswith(MY):
            individuals[name]["obj_props"][p_str] = str(o).split("#")[-1]

# Step 3: 打印结果
for ind, data in individuals.items():
    print(f"\n🧱 个体: {ind}")
    print(f"📌 类型: {data['type']}")
    print(f"🔗 对象属性: {data['obj_props']}")
    print(f"🔢 数据属性: {data['data_props']}")
