from pathlib import Path
from pyshacl import validate
from rdflib import Graph
from kurra.sparql import query
from rdflib.namespace import SH

DATA_DIR = Path(__file__).parent

VOCPUB_GA_VALIDATOR = Graph().parse(Path(__file__).parent.parent.resolve().parent / "items/vocpub-ga.ttl")


def test_vocpub_ga():
    print()

    for f in sorted(list(DATA_DIR.glob("*.ttl"))):
        resp = f"Testing {f.name}"
        validity = False if "invalid" in str(f.name) else True

        allow_warnings = False if "warnings" in str(f.name) else True

        data_graph = Graph().parse(f)

        v = validate(data_graph, shacl_graph=VOCPUB_GA_VALIDATOR, allow_warnings=allow_warnings, advanced=True, inference="rdfs")

        if v[0] and validity:
            resp += " ok"
        elif not v[0] and validity:
            resp += f" {f.name} should be valid but is invalid: {v[2]}"
        elif not v[0] and not validity:
            # if invalid, extract the expected failure info
            r = query(data_graph,
                      "SELECT ?node ?msg WHERE { <http://example.com/test/error> sh:node ?node ; sh:message ?msg }",
                      {"sh": SH}, return_format="python", return_bindings_only=True)
            if len(r) > 0:
                if r[0]["msg"] in v[2]:
                    resp += " ok"
                else:
                    resp += f" {f.name} is invalid, as expected, but the error message was \'{r[0]['msg']}\' instead of {v[2]}"

        else:  # not [v0] and validity
            resp += f" {f.name} should be invalid but is valid"

        print(resp)


if __name__ == "__main__":
    test_vocpub_ga()