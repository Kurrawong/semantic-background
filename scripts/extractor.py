import os
from pathlib import Path
from rdflib import Graph
from rdflib.namespace import DCTERMS, RDFS, SDO, SKOS

parent_dir = Path(__file__).parent.parent

# use the original or, if it exists, an override
for f in Path(parent_dir / "originals").glob("*.ttl"):
    if Path(str(f).replace("originals", "overrides")).is_file():
        f = Path(str(f).replace("originals", "overrides"))

    print(f"extracting labels for {f}")
    parts = os.path.splitext(str(f))
    new_file_path = Path(str(f).replace("originals", "labels").replace("overrides", "labels").replace(".ttl", "-labels.ttl"))
    print(f"writing {new_file_path}")

    g = Graph().parse(f)

    g2 = Graph()
    for s, o in g.subject_objects(
        RDFS.label | SKOS.prefLabel | SDO.name | DCTERMS.title
    ):
        g2.add((s, RDFS.label, o))

    g2.serialize(destination=new_file_path, format="longturtle")
