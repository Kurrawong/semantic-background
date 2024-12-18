import os
import shutil
from pathlib import Path

from rdflib import Graph, Namespace, BNode, Literal
from rdflib.namespace import DC, DCTERMS, RDF, RDFS, SDO, SKOS

MADS = Namespace("http://www.loc.gov/mads/rdf/v1#")

parent_dir = Path(__file__).parent.parent

print(f"Working in {parent_dir}")

# make annotations & copy originals
for f in Path(parent_dir / "originals").glob("*.ttl"):
    print(f"Processing {f}")
    if Path(str(f).replace("originals", "overrides")).is_file():
        f = Path(str(f).replace("originals", "overrides"))

    new_ontology_file_path = (
        str(f)
        .replace("originals", "ontologies")
        .replace("overrides", "ontologies")
        .replace("sources/", "")
    )

    print(f"Copying whole ontology to {new_ontology_file_path}")
    shutil.copy(f, new_ontology_file_path)

    parts = os.path.splitext(str(f))
    new_annotation_file_path = Path(
        str(f)
        .replace("originals", "annotations")
        .replace("overrides", "annotations")
        .replace("sources/", "")
        .replace(".ttl", "-annotations.ttl")
    )
    print(f"Copying annotations to {new_annotation_file_path}")


    g = Graph().parse(f)

    g2 = Graph()
    for s, o in g.subject_objects(
        RDFS.label
        | SKOS.prefLabel
        | SDO.name
        | DCTERMS.title
        | MADS.authoritativeLabel
    ):
        if not isinstance(s, BNode):  # prevents creating labels for BNs like contributors to ontologies
            # convert HTML literals to strings
            if "qudt" in f.name:
                if type(o) == Literal:
                    if o.datatype == RDF.HTML:
                        o = Literal(str(o))
            g2.add((s, RDFS.label, o))

    for s, o in g.subject_objects(
        SKOS.definition
        | SDO.description
        | DCTERMS.description
        | DC.description
        | RDFS.comment
    ):
        if not isinstance(s, BNode):
            if "qudt" in f.name:
                if type(o) == Literal:
                    if o.datatype == RDF.HTML:
                        o = Literal(str(o))
            g2.add((s, SDO.description, o))

    for s, o in g.subject_objects(RDFS.seeAlso):
        if not isinstance(s, BNode):
            g2.add((s, RDFS.seeAlso, o))

    g2.serialize(destination=new_annotation_file_path, format="longturtle", )
