# Skills

Portable agent Skills with RDF descriptions, shared as examples for review and reuse. Each Skill has its own directory containing a `SKILL.md` instruction entry point and a `metadata.ttl` semantic description.

## Examples

- [VocPub Definition Skill](vocpub-definition/SKILL.md) — investigate missing SKOS concept definitions and propose evidence-backed definitions with provenance. [RDF metadata](vocpub-definition/metadata.ttl).

The first example explores describing a Skill as `schema:HowTo` and `prov:Plan`, with a separate `prof:ResourceDescriptor` offering it in the role of profile guidance. The proposed Skill IRI is `https://linked.data.gov.au/def/vocpub/skill/definition`; registration, resolution and adoption by the VocPub publisher are not asserted.

Review the evidence ranking, proposal provenance, class choices, PROF relationship and identifier pattern before treating this draft as established practice. The repository's default licensing policy applies unless a resource states otherwise; attribution and explicit licence metadata remain review points for the draft.

Use sibling directories for additional Skills. The `vocpub-` prefix groups related packages while preserving each package's portable directory name.
