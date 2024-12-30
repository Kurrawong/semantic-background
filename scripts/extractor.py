"""
This script extracts annotations - labels, descriptions & seeAlso links - from originals in files in the `originals/`
folder and puts them in files in the `annotations/` folder.

This script will preference versions of originals in the `sources/overrides/` folder over those in the
`sources/originals/` folder, if they exist. This allows for manually-edited versions of common originals to be used.
"""

import os
import shutil
from pathlib import Path

from rdflib import Graph, Namespace, BNode, Literal
from rdflib.namespace import DC, DCTERMS, RDF, RDFS, SDO, SKOS

MADS = Namespace("http://www.loc.gov/mads/rdf/v1#")

repo_root = Path(__file__).parent.parent.resolve()

print(f"Working in {repo_root}")

# make annotations & copy originals
for f in Path(repo_root / "originals").glob("*.ttl"):
    print(f"Processing {f}")
    if Path(str(f).replace("originals", "overrides")).is_file():
        f = Path(str(f).replace("originals", "overrides"))

    # place a copy of the original or an override, if we have one, in ontologies/
    new_ontology_file = Path(
        str(f)
        .replace("originals", "ontologies")
        .replace("overrides", "ontologies")
    )
    print(f"Copying the original or overridden ontology to {new_ontology_file}")
    shutil.copy(f, new_ontology_file)

    new_annotation_file = Path(
        str(new_ontology_file)
        .replace("ontologies", "annotations")
        .replace(".ttl", "-annotations.ttl")
    )
    print(f"Copying annotations to {new_annotation_file}")


    g = Graph().parse(f)

    g2 = Graph()
    for s, o in g.subject_objects(
        RDFS.label
        | SKOS.prefLabel
        | SDO.name
        | DCTERMS.title
        | MADS.authoritativeLabel
    ):
        if not isinstance(s, BNode):  # prevents creating labels for BNs like contributors to originals
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

    g2.serialize(destination=new_annotation_file, format="longturtle", )
