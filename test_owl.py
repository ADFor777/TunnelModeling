from owlready2 import get_ontology

onto = get_ontology("http://test.org/onto.owl")
print("OWLReady2 导入成功，空本体已创建：", onto)
