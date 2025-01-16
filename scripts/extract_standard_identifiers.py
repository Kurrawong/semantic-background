from pathlib import Path
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, SKOS

MADS = Namespace("http://www.loc.gov/mads/rdf/v1#")

g = Graph().parse(Path(__file__).parent / "standard_identifiers.nt")

cs = URIRef("http://id.loc.gov/vocabulary/identifiers")
g2 = Graph()
g2.bind("cs", cs)
g2.bind("", str(cs) + "/")

g2.parse(
    data=f'''   
    # from https://id.loc.gov/vocabulary/identifiers.skos.nt
    <http://id.loc.gov/vocabulary/identifiers> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2004/02/skos/core#ConceptScheme> .
    <http://id.loc.gov/vocabulary/identifiers> <http://www.w3.org/2000/01/rdf-schema#label> "Standard Identifiers"@en .
    <http://id.loc.gov/vocabulary/identifiers> <http://www.w3.org/2004/02/skos/core#definition> "The Standard Identifiers Scheme lists standard number or code systems and assigns a URI to each database or publication that defines or contains the identifiers. The purpose of these source codes is to enable the type of standard numbers or codes in resource descriptions to be indicated by URI."@en .
    ''',
    format="turtle",
)

for c in g.subjects(predicate=RDF.type, object=MADS.Authority):
    print(c)
    g2.add((c, RDF.type, SKOS.Concept))
    g2.add((c, SKOS.inScheme, cs))
    g2.add((c, RDFS.isDefinedBy, cs))
    g2.add((cs, SKOS.hasTopConcept, c))
    for o in g.objects(subject=c, predicate=MADS.authoritativeLabel):
        g2.add((c, SKOS.prefLabel, o))
        g2.add((c, SKOS.definition, o))

g2.serialize(destination=Path(__file__).parent.parent / "originals/standard_identifiers.ttl", format="longturtle")