from rdflib import Graph, Namespace, RDF, RDFS, Literal
from rdflib.namespace import OWL
import json

# 载入本体
g = Graph()
g.parse("Tunnel_RDF.owl", format="xml")

# 命名空间
SWRL  = Namespace("http://www.w3.org/2003/11/swrl#")
SWRLA = Namespace("http://swrl.stanford.edu/ontologies/3.3/swrla.owl#")
MY    = Namespace("http://www.semanticweb.org/lenovo/ontologies/2025/5/untitled-ontology-10/")  
RDFNS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# 结果列表
rules = []

# 遍历所有规则个体（类型为 swrl:Imp）
for rule in g.subjects(RDF.type, SWRL.Imp):
    label = g.value(rule, RDFS.label)
    comment = g.value(rule, RDFS.comment)
    enabled = g.value(rule, SWRLA.isRuleEnabled)
    enabled_str = str(enabled).lower() == "true"

    body_atoms = []
    head_atoms = []

    # 提取 body 中的 atom 列表
    for list_node in g.items(g.value(rule, SWRL.body)):
        atom_type = g.value(list_node, RDF.type)
        pred = g.value(list_node, SWRL.argument1)
        obj  = g.value(list_node, SWRL.argument2)
        prop = g.value(list_node, SWRL.propertyPredicate) or g.value(list_node, SWRL.classPredicate) or g.value(list_node, SWRL.dataPropertyPredicate)

        if atom_type:  # 转换为类似 "hasSoilType(?t, WeakSoil)"
            predicate = prop.split("#")[-1] if prop else "UnknownPredicate"
            subj = pred.split("#")[-1] if pred else "?x"
            obj_ = obj.split("#")[-1] if obj else "?y"
            body_atoms.append(f"{predicate}({subj}, {obj_})")

    # 提取 head（只允许一个 DataPropertyAtom）
    for list_node in g.items(g.value(rule, SWRL.head)):
        pred = g.value(list_node, SWRL.argument1)
        obj  = g.value(list_node, SWRL.argument2)
        prop = g.value(list_node, SWRL.dataPropertyPredicate)
        if prop:
            predicate = prop.split("#")[-1]
            subj = pred.split("#")[-1] if pred else "?x"
            val  = str(obj)
            head_atoms.append(f"{predicate}({subj}, {val})")

    # 保存规则
    rules.append({
        "label": str(label),
        "enabled": enabled_str,
        "comment": str(comment),
        "body": body_atoms,
        "head": head_atoms
    })

# 输出为 JSON
print(json.dumps(rules, indent=2, ensure_ascii=False))
