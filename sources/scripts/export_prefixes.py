import json
from pathlib import Path
from rdflib import Graph

parent_dir = Path(__file__).parent.parent.parent
output_dir = parent_dir / "sources/gh-pages/ns"
output_dir.mkdir(parents=True, exist_ok=True)

for item in output_dir.glob('**/*'):
    if item.is_file:
        item.unlink()

g = Graph()
for f in Path(parent_dir / "ontologies").glob("*.ttl"):
    g.parse(f)

for ns_prefix, namespace in g.namespaces():
    # Empty prefixes are valid, only run with prefixes that have a value.
    if ns_prefix:
        print(ns_prefix, namespace)

        with open(output_dir / f"{ns_prefix}.file.json", "w") as f:
            json.dump({ns_prefix: namespace}, f)
