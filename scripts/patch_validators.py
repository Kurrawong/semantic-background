from rdflib import Graph
from srl.parser import SRLParser
from srl.engine import RuleEngine
from kurra.utils import load_graph
from pathlib import Path
from rdflib import DC, DCTERMS, RDF, RDFS, SDO, SKOS

def srl_evaluate(data: Graph, rule_text: str):
    return RuleEngine(SRLParser().parse(rule_text)).evaluate(data, inplace=False, results_only=True)

def add_namespaces(q: str, namespaces: dict) -> str:
    preamble = ""
    for k, v in namespaces.items():
        preamble += f"PREFIX {k}: <{v}>\n"
    preamble += "\n"
    return preamble + q

namespaces = {
    "dc": DC,
    "dcterms": DCTERMS,
    "rdf": RDF,
    "rdfs": RDFS,
    "schema": SDO,
    "skos": SKOS,
}

r_names = \
    """
    RULE {
        ?x schema:name ?y .
    } WHERE {
        ?x skos:prefLabel ?y .
    }
    
    RULE {
        ?x schema:description ?y .
    } WHERE {
        ?x skos:definition ?y .
    }    
    """
# dc:title|dcterms:title|rdfs:label|skos:prefLabel
r_names = add_namespaces(r_names, namespaces)

for f in Path(Path(__file__).parent.parent / "resources/validators/items").glob("*.ttl"):
    if str(f.name).startswith("geo"):
        d = load_graph(f)
        o = srl_evaluate(d, r_names)
        print(o.serialize(format="longturtle"))
        break