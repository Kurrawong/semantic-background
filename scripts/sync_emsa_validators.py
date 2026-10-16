"""Replace EMSA validators and reconcile their ShapesGraph IRIs in the catalogue.

Run from any directory with ``uv run scripts/sync_emsa_validators.py``.
Requires rdflib and kurra (provided by this project's dependencies).
"""

import argparse
from datetime import date
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from kurra.file import reformat
from rdflib import Graph, Literal, RDF, URIRef, XSD, Namespace


SH = Namespace("http://www.w3.org/ns/shacl#")
SCHEMA = Namespace("https://schema.org/")
ROOT = Path(__file__).resolve().parents[1]


def shapes_graph_iris(files: list[Path]) -> set[URIRef]:
    iris = set()
    for path in files:
        graph = Graph().parse(path, format="turtle")
        for subject in graph.subjects(RDF.type, SH.ShapesGraph):
            if not isinstance(subject, URIRef):
                raise ValueError(f"ShapesGraph without an IRI in {path}")
            iris.add(subject)
    return iris


def sync(source: Path, destination: Path, catalogue: Path) -> bool:
    source, destination, catalogue = (
        path.resolve() for path in (source, destination, catalogue)
    )
    print("source:", source)
    print("destination:", destination)
    print("catalogue:", catalogue)
    if not source.is_dir():
        raise ValueError(f"Source directory does not exist: {source}")
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("Source and destination directories must not overlap")
    if destination == catalogue or destination in catalogue.parents:
        raise ValueError("Catalogue must be outside the replacement directory")
    files = sorted(source.rglob("sg.ttl"))
    if not files:
        raise ValueError(f"No sg.ttl files found in {source}; refusing to clear destination")
    print(f"Syncing {len(files)} sg files to {destination}")
    old_iris = shapes_graph_iris(sorted(destination.rglob("sg.ttl")))
    new_iris = shapes_graph_iris(files)
    graph = Graph().parse(catalogue, format="turtle")
    catalogues = set(graph.subjects(RDF.type, SCHEMA.DataCatalog))
    if len(catalogues) != 1:
        raise ValueError("Expected exactly one schema:DataCatalog in the catalogue")
    subject = catalogues.pop()
    existing = set(graph.objects(subject, SCHEMA.hasPart))
    desired = (existing - old_iris) | new_iris
    changed = desired != existing
    if changed:
        versions = list(graph.objects(subject, SCHEMA.version))
        if len(versions) != 1 or not str(versions[0]).isdigit():
            raise ValueError("Expected one nonnegative integer schema:version")
        version = versions[0]
        graph.remove((subject, SCHEMA.hasPart, None))
        for iri in desired:
            graph.add((subject, SCHEMA.hasPart, iri))
        graph.set((subject, SCHEMA.dateModified, Literal(date.today(), datatype=XSD.date)))
        graph.set((subject, SCHEMA.version, Literal(
            str(int(str(version)) + 1), datatype=version.datatype, lang=version.language
        )))

    # Validate and format everything before deleting existing destination files.
    with TemporaryDirectory(prefix="emsa-sync-") as temporary:
        stage = Path(temporary) / "items"
        stage.mkdir()
        for index, path in enumerate(files, start=1):
            target = stage / path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            print(
                f"Formatting {index}/{len(files)}: {path.relative_to(source)}",
                flush=True,
            )
            reformat(target, check=False)
        staged_catalogue = Path(temporary) / "catalogue.ttl"
        if changed:
            graph.serialize(staged_catalogue, format="turtle")
            print(f"Formatting catalogue: {catalogue}", flush=True)
            reformat(staged_catalogue, check=False)
        if destination.exists():
            shutil.rmtree(destination)
        for path in files:
            relative = path.relative_to(source)
            staged_file = stage / relative
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(staged_file, target)
            for iri in sorted(shapes_graph_iris([target]), key=str):
                print(f"Copied {relative}: {iri}")
        if changed:
            shutil.copy2(staged_catalogue, catalogue)
    print(f"Copied {len(files)} sg.ttl files to {destination}")
    print("Catalogue updated" if changed else "Catalogue unchanged")
    return changed


def main() -> None:
    print("syncing EMSA validators")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(
        "/Users/nick/work/bdr/dawe-rlp-spec/shapes"
    ))
    parser.add_argument("--destination", type=Path,
                        default=ROOT / "resources/validators/items/emsa")
    parser.add_argument("--catalogue", type=Path,
                        default=ROOT / "resources/validators/catalogue.ttl")
    args = parser.parse_args()
    sync(args.source, args.destination, args.catalogue)


if __name__ == "__main__":
    main()
