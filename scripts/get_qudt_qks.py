from datetime import datetime
import httpx
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS
QUDT = Namespace("http://qudt.org/schema/qudt/")
QK = Namespace("http://qudt.org/vocab/quantitykind/")

# # Get Quantity Kinds
# r = httpx.get("http://qudt.org/2.1/vocab/quantitykind", headers={"Accept": "text/turtle"}, follow_redirects=True)
#
# with open("../originals/quantitykinds.ttl", "wb") as f:
#     f.write(r.content)
#
# # Reformat to long turtle
# Graph().parse("../originals/quantitykinds.ttl").serialize(destination="../originals/quantitykinds.ttl", format="longturtle")

# Extract a Defined Namespace
qks = []

g = Graph().parse("../originals/quantitykinds.ttl")

for s in g.subjects(RDF.type, QUDT.QuantityKind):
    # label = None
    # for lang_label in g.objects(s, RDFS.label):
    #     if lang_label._language == "en":
    #         label = lang_label

    desc = g.value(s, DCTERMS.description)
    if desc is None:
        desc = g.value(s, RDFS.comment)
    if desc is None:
        desc = g.value(s, RDFS.label)

    desc = str(desc).replace("\n", "") if desc is not None else ""

    qks.append("    " + str(s).replace(str(QK), "").replace("-", "_") + ": URIRef  # " + desc)

qks_str = "\n".join([x for x in sorted(qks)])

ont_desc = g.value(subject=URIRef("http://qudt.org/2.1/vocab/quantitykind"), predicate=RDFS.label)

file_text = f'''from rdflib.term import URIRef
from rdflib.namespace import DefinedNamespace


class QKS(DefinedNamespace):
    """
    {ont_desc}

    Generated from: http://qudt.org/2.1/vocab/quantitykind
    Date: {datetime.utcnow()}
    """
    
    _fail = True
    
{qks_str}
    
'''

open("QKS.py", "w").write(file_text)



