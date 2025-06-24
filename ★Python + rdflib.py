from rdflib import Graph, Namespace, URIRef

g = Graph()
g.parse("Tunnel_RDF.owl", format="xml")

SWRL = Namespace("http://www.w3.org/2003/11/swrl#")
SWRLA = Namespace("http://swrl.stanford.edu/ontologies/3.3/swrla.owl#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

for rule in g.subjects(predicate=RDFS.label):
    label = g.value(subject=rule, predicate=RDFS.label)
    comment = g.value(subject=rule, predicate=RDFS.comment)
    enabled = g.value(subject=rule, predicate=SWRLA.isRuleEnabled)
    print(f"规则: {label}, 启用: {enabled}, 注释: {comment}")
