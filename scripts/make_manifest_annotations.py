# makes the manifest-annotations.ttl file
from pathlib import Path
from rdflib import Graph, BNode, URIRef, Literal
from rdflib.namespace import OWL, PROF, RDF, SDO, SKOS

FILES_DIR = Path(__file__).parent.parent.resolve() / "ontologies"
MANIFEST_ROOT = Path(__file__).parent.parent.resolve()

g = Graph().parse(
    data="""
PREFIX ex: <http://example.com/>
PREFIX mrr: <https://prez.dev/ManifestResourceRoles/>
PREFIX prez: <https://prez.dev/>
PREFIX prof: <http://www.w3.org/ns/dx/prof/>
PREFIX schema: <https://schema.org/>

<https://kurrawong.ai/semantic-bankground/annotations-manifest>
    a prez:Manifest ;
    prof:hasResource
        [
            prof:hasArtifact "catalogue-annotations.ttl" ;
            prof:hasRole mrr:CatalogueData ;
            schema:description "The definition of, and medata for, the container which here is a dcat:Catalog object" ;
            schema:name "Catalogue Definition"
        ] ,
        ex:label-resources ;
.

ex:label-resources
    prof:hasRole mrr:ResourceData ;
    schema:description "Collections of labels for ontologies and vocabularies" ;
    schema:name "Resource Data"
.
""",
    format="turtle"
)

for f in sorted(FILES_DIR.glob("*.ttl")):
    gf = Graph().parse(f)
    iri = gf.value(predicate=RDF.type, object=SKOS.ConceptScheme) or gf.value(predicate=RDF.type, object=OWL.Ontology)

    if iri is None:
        raise ValueError(f"No IRI extracted from {f}")

    f_new = str(f).replace(str(MANIFEST_ROOT), "").replace("/ontologies", "annotations").replace(".ttl", "-annotations.ttl")
    bn = BNode()

    g.add((
        URIRef("http://example.com/label-resources"),
        PROF.hasArtifact,
        bn
    ))
    g.add((
        bn,
        SDO.mainEntity,
        iri
    ))
    g.add((
        bn,
        SDO.contentLocation,
        Literal(f_new)
    ))


g.serialize(destination=Path(__file__).parent.parent / "manifest-annotations.ttl", format="longturtle")