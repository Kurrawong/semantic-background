from pathlib import Path
from kurra.file import reformat

d = Path(__file__).parent / "tests"

for f in sorted(d.rglob("*.ttl")):
    print(f)
    reformat(f, check=False, output_format="longturtle")
