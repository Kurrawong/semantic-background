import os
from pathlib import Path
from pyshacl import validate
from rdflib import Graph
from kurra.sparql import query
from rdflib.namespace import SH

BCRP_DATA_DIR = Path(__file__).parent / "bcrp"
BCRP_VALIDATOR = Graph().parse(Path(__file__).parent.parent.resolve() / "items/bcrp.ttl")

VOCPUB_DATA_DIR = Path(__file__).parent / "vocpub"
VOCPUB_VALIDATOR = Graph().parse(Path(__file__).parent.parent.resolve() / "items/vocpub.ttl")

VOCPUB_GA_DATA_DIR = Path(__file__).parent / "vocpub-ga"
VOCPUB_GA_VALIDATOR = Graph().parse(Path(__file__).parent.parent.resolve() / "items/vocpub-ga.ttl")


def _validate_files(data_dir, validator):
    for f in sorted(list(data_dir.glob("*.ttl"))):
        resp = f"Testing {f.name}"
        validity = False if "invalid" in str(f.name) else True

        allow_warnings = False if "warnings" in str(f.name) else True

        data_graph = Graph().parse(f)

        v = validate(data_graph, shacl_graph=validator, allow_warnings=allow_warnings, advanced=True,
                     inference="rdfs")

        if v[0] and validity:
            resp += " ok"
        elif not v[0] and validity:
            resp += f" should be valid but is invalid: {v[2]}"
        elif not v[0] and not validity:
            # if invalid, extract the expected failure info and compare messages and focus nodes
            r = query(data_graph,
                      "SELECT ?node ?msg WHERE { <http://example.com/test/error> sh:node ?node ; sh:message ?msg }",
                      {"sh": SH}, return_format="python", return_bindings_only=True)
            if len(r) > 0:
                if r[0]["msg"] in v[2]:
                    resp += " ok"
                else:
                    resp += f" is invalid, as expected, but the error message \'{r[0]['msg']}\' was not found in the error report: {v[2]}"

                r2 = query(v[1],
                          "SELECT ?node WHERE { ?x sh:focusNode ?node }",
                          {"sh": SH}, return_format="python", return_bindings_only=True)
                assert r[0]["node"] == r2[0]["node"], f'{r[0]["node"]} was found, test indicated {r2[0]["node"]}'

        else:  # not [v0] and validity
            resp += f" should be invalid but is valid"

        print(resp)

    if "PYTEST_CURRENT_TEST" in os.environ:
        print("Running via pytest")


def test_bcrp():
    print("Testing BCRP\n")
    _validate_files(BCRP_DATA_DIR, BCRP_VALIDATOR)


def test_vocpub():
    print("Testing VocPub\n")
    _validate_files(VOCPUB_DATA_DIR, VOCPUB_VALIDATOR)


def test_vocpub_ga():
    print("Testing VocPub GA\n")
    _validate_files(VOCPUB_GA_DATA_DIR, VOCPUB_GA_VALIDATOR)


if __name__ == "__main__":
    print("------------\n")
    test_bcrp()
    print("------------\n")
    test_vocpub()
    print("------------\n")
    test_vocpub_ga()