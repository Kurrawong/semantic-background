import json
from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef

parent_dir = Path(__file__).parent.parent.parent

g = Graph()
for f in Path(parent_dir / "ontologies").glob("*.ttl"):
    g.parse(f)


for ns_prefix, namespace in g.namespaces():
    print(ns_prefix, namespace)

    with open(f'ns/{ns_prefix}.file.json', 'w') as f:
        json.dump({ns_prefix: namespace}, f)