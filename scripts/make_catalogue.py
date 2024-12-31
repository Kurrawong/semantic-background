from pathlib import Path
from rdflib import Graph
from rdflib.namespace import OWL, RDF, SKOS
from textwrap import dedent

FILES_DIR = Path(__file__).parent.parent.resolve() / "ontologies"

iris = []

for f in sorted(FILES_DIR.glob("*.ttl")):
    g = Graph()
    g.parse(f)
    iri = g.value(predicate=RDF.type, object=SKOS.ConceptScheme) or g.value(predicate=RDF.type, object=OWL.Ontology)

    if iri is None:
        raise ValueError(f"No IRI extracted from {f}")

    iris.append(iri)

hasParts = "<" + "> ,\n    \t\t<".join(iris) + "> ;"

template = \
    f"""\
    PREFIX astatus: <https://linked.data.gov.au/def/reg-statuses/>
    PREFIX catns: <https://example.com/demo-vocabs/>
    PREFIX dcat: <http://www.w3.org/ns/dcat#>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX reg: <http://purl.org/linked-data/registry#>
    PREFIX schema: <https://schema.org/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    
    <https://kurrawong.ai/semantic-bankground/annotations>
        a dcat:Catalog ;
        dcterms:hasPart
            {hasParts}
        schema:codeRepository "https://github.com/kurrawong/demo-vocabs" ;
        schema:creator <https://kurrawong.ai> ;
        schema:dateCreated "2023"^^xsd:gYear ;
        schema:dateModified "2024-10-16"^^xsd:date ;
        schema:description "A testing catalogue for the Prez Manifest Loader tool" ;
        schema:name "Demo Vocabularies" ;
        schema:publisher <https://kurrawong.ai> ;
        reg:status astatus:experimental ;
    ."""

print(dedent(template))