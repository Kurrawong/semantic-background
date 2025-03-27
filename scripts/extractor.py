"""
This script extracts annotations - labels, descriptions & seeAlso links - from originals in files in the `originals/`
folder and puts them in files in the `annotations/` folder.

This script will preference versions of originals in the `sources/overrides/` folder over those in the
`sources/originals/` folder, if they exist. This allows for manually-edited versions of common originals to be used.
"""

import shutil
import sys
from itertools import chain
from pathlib import Path

from rdflib import Graph, Namespace, BNode, Literal, Dataset, URIRef
from rdflib.namespace import DC, DCTERMS, OWL, RDF, RDFS, SDO, SKOS

MADS = Namespace("http://www.loc.gov/mads/rdf/v1#")

repo_root = Path(__file__).parent.parent.resolve()

def main(files: list[Path] = None):
    print(f"Working in {repo_root}")

    if files is not None:
        files = [Path(x) for x in files.split(",")]
    else:
        files = Path(repo_root / "originals").glob("*.ttl")

    d = Dataset()

    # make annotations & copy originals
    for f in files:
        print(f"{f}")
        if Path(str(f).replace("originals", "overrides")).is_file():
            f = Path(str(f).replace("originals", "overrides"))

        # place a copy of the original or an override, if we have one, in ontologies/
        new_ontology_file = Path(
            str(f)
            .replace("originals", "ontologies")
            .replace("overrides", "ontologies")
        )
        print(f"Copying to {new_ontology_file}")
        shutil.copy(f, new_ontology_file)

        new_annotation_file = Path(
            str(new_ontology_file)
            .replace("ontologies", "annotations")
            .replace(".ttl", "-annotations.ttl")
        )
        print(f"Annotations to {new_annotation_file}")

        g = Graph().parse(f)

        g2 = Graph()
        for s, o in g.subject_objects(
            RDFS.label
            | SKOS.prefLabel
            | SDO.name
            | DCTERMS.title
            | DC.title
            | MADS.authoritativeLabel
        ):
            if not isinstance(s, BNode):  # prevents creating labels for BNs like contributors to originals
                # convert HTML literals to strings
                if "qudt" in f.name:
                    if type(o) == Literal:
                        if o.datatype == RDF.HTML:
                            o = Literal(str(o))
                # only extract English or non-lang labels
                if isinstance(o, Literal):
                    if o.language in ["en", None]:
                        g2.add((s, SDO.name, o))

        # deduplicate elements that have both definitions & comments
        q = """
            PREFIX dc: <http://purl.org/dc/elements/1.1/>            
            PREFIX dcterms: <http://purl.org/dc/terms/>
            PREFIX schema: <https://schema.org/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
            CONSTRUCT {
                ?x schema:description ?lbl
            }
            WHERE {
                OPTIONAL { 
                    ?x skos:definition ?l1 
                    FILTER (lang(?l1) IN ("en", ""))
                }
                
                OPTIONAL { 
                    ?x rdfs:comment ?l2
                    FILTER (lang(?l2) IN ("en", ""))
                }
                
                OPTIONAL { 
                    ?x schema:description ?l3 
                    FILTER (lang(?l3) IN ("en", ""))
                }
                
                OPTIONAL { 
                    ?x dcterms:description ?l4
                    FILTER (lang(?l4) IN ("en", ""))
                }
                
                OPTIONAL { 
                    ?x dc:description ?l5 
                    FILTER (lang(?l5) IN ("en", ""))
                }
                
                BIND (COALESCE(?l1, ?l2, ?l3, ?l4, ?l5) AS ?lbl)
            }
            """

        for r in g.query(q):
            g2.add(r)

        for s, o in g.subject_objects(RDFS.seeAlso):
            if not isinstance(s, BNode):
                g2.add((s, RDFS.seeAlso, o))

        g2.serialize(destination=new_annotation_file, format="longturtle")

        # create a single Trig file of all content
        # find the IRI of the Ontology/ConceptScheme
        ont_iri = None
        for s in g.subjects(RDF.type, OWL.Ontology):
            ont_iri = str(s)
            print(f"{s}")
        if ont_iri is None:
            for s in g.subjects(RDF.type, SKOS.ConceptScheme):
                ont_iri = str(s)
                print(f"{s}")

        if ont_iri is not None:
            g3 = Graph(identifier=ont_iri + "-annotations")
            g3 += g2

            d.add_graph(g3)

    # only rewrite the trig file if multiple (all) files are being processed
    if len(list(d.graphs())) > 2:
        d.serialize(destination=repo_root / "annotations.trig", format="trig")



if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)