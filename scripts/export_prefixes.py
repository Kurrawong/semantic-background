import json
from pathlib import Path
from rdflib import Graph
import re

parent_dir = Path(__file__).parent.parent
output_dir = parent_dir / "gh-pages/ns"
output_dir.mkdir(parents=True, exist_ok=True)

for item in output_dir.glob('**/*'):
    if item.is_file:
        item.unlink()

g = Graph()
for f in Path(parent_dir / "originals").glob("*.ttl"):
    g.parse(f)

protocolRegex = re.compile(r"^(https:\/\/|http:\/\/)", re.IGNORECASE)
specialRegex = re.compile(r"\W", re.IGNORECASE)

for ns_prefix, namespace in g.namespaces():
    # Empty prefixes are valid, only run with prefixes that have a value.
    if ns_prefix:
        print(ns_prefix, namespace)

        with open(output_dir / f"{ns_prefix}.file.json", "w") as f:
            json.dump({ns_prefix: namespace}, f)
        
        safe_file_name = specialRegex.sub("-", protocolRegex.sub("",namespace))
        with open(output_dir / f"{safe_file_name}.file.json", "w") as f:
            json.dump({namespace: ns_prefix}, f)
