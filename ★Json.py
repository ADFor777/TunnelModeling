from rdflib import Graph, Namespace, RDF, RDFS, Literal
from rdflib.namespace import OWL
import json
import os

# ====== Step 1: 加载本体 ======
filename = "Tunnel_RDF.owl"
if not os.path.exists(filename):
    print("⚠️ 文件未找到，请检查路径！当前路径：", os.getcwd())
    exit()

g = Graph()
g.parse(filename, format="xml")

# ====== Step 2: 定义命名空间 ======
SWRL  = Namespace("http://www.w3.org/2003/11/swrl#")
SWRLA = Namespace("http://swrl.stanford.edu/ontologies/3.3/swrla.owl#")
MY    = Namespace("http://www.semanticweb.org/lenovo/ontologies/2025/5/untitled-ontology-10/")  
RDFNS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# ====== Step 3: 提取规则 ======
rules = []

for rule in g.subjects(RDF.type, SWRL.Imp):
    label = g.value(rule, RDFS.label)
    comment = g.value(rule, RDFS.comment)
    enabled = g.value(rule, SWRLA.isRuleEnabled)
    enabled_str = str(enabled).lower() == "true"

    body_atoms = []
    head_atoms = []

    # Body
    for list_node in g.items(g.value(rule, SWRL.body)):
        atom_type = g.value(list_node, RDF.type)
        pred = g.value(list_node, SWRL.argument1)
        obj  = g.value(list_node, SWRL.argument2)
        prop = g.value(list_node, SWRL.propertyPredicate) or g.value(list_node, SWRL.classPredicate) or g.value(list_node, SWRL.dataPropertyPredicate)

        if atom_type:
            predicate = prop.split("#")[-1] if prop else "UnknownPredicate"
            subj = pred.split("#")[-1] if pred else "?x"
            obj_ = obj.split("#")[-1] if obj else "?y"
            body_atoms.append(f"{predicate}({subj}, {obj_})")

    # Head
    for list_node in g.items(g.value(rule, SWRL.head)):
        pred = g.value(list_node, SWRL.argument1)
        obj  = g.value(list_node, SWRL.argument2)
        prop = g.value(list_node, SWRL.dataPropertyPredicate)
        if prop:
            predicate = prop.split("#")[-1]
            subj = pred.split("#")[-1] if pred else "?x"
            val  = str(obj)
            head_atoms.append(f"{predicate}({subj}, {val})")

    rules.append({
        "label": str(label),
        "enabled": enabled_str,
        "comment": str(comment),
        "body": body_atoms,
        "head": head_atoms
    })

# ====== Step 4: 写入 JSON 文件 ======
output_path = "rules_output.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(rules, f, indent=2, ensure_ascii=False)

print(f"✅ 成功写入 JSON 文件：{output_path}")

