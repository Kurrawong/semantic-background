# TERN instrument-type test, 26 November 2026

This case study records one difficult test of the VocPub Definition Skill. It distinguishes observed characteristics of a supplied vocabulary export from generally useful procedure. It is not a quality assessment of all TERN vocabularies or a claim about vocabularies in general.

## Scope and outcome

The test used `terncv-instrument-type.ttl`, a 3.2 MB export of the Instrument Type scheme, identified by `http://linked.data.gov.au/def/tern-cv/a3088b5c-622d-4e25-8a75-4c4961b0dfe8`. The input SHA-256 was `9e26b4aeeb25b6c2677720144306f72502702b0ad69590ce27109fca9ef53f37`. Instructions came from commit `454e39c5b3eba7b7d43c9ba9fe927b878caefd90` of `Kurrawong/semantic-background`; the proposed Skill IRI did not resolve through the retrieval tool. This test predates version 0.2.0's explicit history-note procedure.

Of 3,928 concepts, 3,675 lacked a correctly named `skos:definition`. The test added 3,646 English definitions to a local copy: 10 assessed as high confidence and 3,636 as medium confidence. It held 28 low-confidence candidates and produced no candidate for one unidentified record. Definitions already present on 253 concepts were preserved. The extracted VocPub 5.9 concept-definition shape reported 3,675 missing-definition results before and 29 after. This was not full VocPub validation, publisher approval or a live data update. No history note was added, because the authorised test was limited to definition data.

A proposed retrospective history event for that test reads:

> 2026-11-26: Codex added 3,646 English concept definitions to a test copy using https://linked.data.gov.au/def/vocpub/skill/definition at commit 454e39c5b3eba7b7d43c9ba9fe927b878caefd90. Model: GPT-6.1 Sol; reasoning effort: Medium, confirmed retrospectively by the operator. Application version and exact model snapshot were not captured. Most additions were synthesised from camera-model and sensor-size records; 29 concepts remained unresolved. Vocabulary-editor review pending. The VocPub 5.9 definition-only check retained 29 missing-definition results. Run: urn:vocpub-definition-test:2026-11-26:run. Detailed evidence is held in the accompanying local report, decision log and proposal provenance.

This is a history-note proposal, not a claim that the test used the revised Skill or that its graph has been updated. The URN identifies the actual run in the local provenance graph; it is not a publicly resolvable report link.

The operator subsequently confirmed the model label and reasoning effort. This confirmation is distinct from metadata captured by the execution environment; it does not establish an exact serving identifier or deployment revision. A separate [AgentPub](https://github.com/leskneebone/AgentPub) example develops the run-resource, agent/model and validation-record packaging.

## Particular characteristics of this export

- **Camera-model concentration:** 3,651 missing definitions were on `tern:DigitalCamera` records. Most had model, manufacturer and sensor-size notes derived from the openMVG Camera Sensor Size Database. This made batching effective but favoured concise inventory descriptions over independently verified manufacturer definitions. It does not establish a typical vocabulary workload.
- **Questionable hierarchy:** all those camera records had a broader concept labelled DSLR, including phones, a tablet and camera modules. The local graph already contained a separate Digital camera concept. Deciding whether to use that existing category or introduce another requires clarification of whole-device versus camera-component scope; the enrichment did not reparent records or create concepts.
- **Definition-bearing predicates outside SKOS:** CTD and wet pitfall trap used `skos:definition:`; Campbell Scientific CR1000X used `skos:defintion`. CR1000X and basal wedge also carried text under `skos:description`, which is not a defined SKOS property. Similar-looking predicates were inspected rather than treated as automatic equivalents. Original triples were preserved while appropriate definitions were added.
- **Incomplete or conflicting records:** “Olympus nan” did not identify a model. Six camera notes contained missing-value placeholders. Canon EOS 650D had conflicting sensor-width fields. RaspberryPi RP_imx219 conflicted with official sensor image-area dimensions. The DJI FC6310 sensor/model correspondence remained unresolved. These observations are not a general blacklist of those products or sources.
- **Sparse mapping evidence:** four of 16 distinct fetched GCMD records supplied definitions. Some local categories had overlapping or broader mapped labels, or children inconsistent with an obvious label-based interpretation. The available definitions and mappings did not justify every proposed scope.
- **Access limitations:** some cited product URLs failed; other information was available through web extraction or primary-source indexed excerpts. The audit distinguished these from full-document inspection. It did not claim inaccessible full pages or manuals had been read.

## Lessons used in the general Skill

Inventory before fetching sources; cache shared evidence; match individual source records and inspect exceptions before repeating a formulation. Separate authority and evidence route from confidence. Treat uncertain identity, scope and substantive facts as reasons to hold a candidate. Inspect definition-bearing local properties without silently repairing an unrelated data model. Record an applied enrichment as a dated, versioned, attributable history event with a link to detailed run evidence. Keep changes to hierarchy, mappings and new concepts in a separate editorial proposal.

The general Skill does not require every vocabulary to undergo a camera audit, a comprehensive predicate audit or a fixed number of external lookups. The test's conservative high/medium/low decisions are qualitative editorial assessments, not calibrated probabilities or proof of definition correctness.

## Tool observations

The input's UTF-8 byte-order mark was accepted by RDFLib but rejected by the installed `rapper`. Only the enriched copy dropped that leading mark; the original download and all original graph triples remained intact. Captured Kurra CLI RDF output wrapped long messages into invalid Turtle. Valid reports were regenerated with the same environment's pySHACL 0.40.2 API. These are environment observations and fallbacks, not universal limitations of RDF tools.

The deterministic generation and graph-preservation check took approximately 2.4 seconds; the definition-only before/after validations each took approximately one second. These timings exclude source retrieval and editorial analysis. Most effort went into assessing meaning, conflicting context and evidence access, so those times must not be presented as end-to-end agent performance.

## Sources and follow-up boundary

The [camera database](https://github.com/openMVG/CameraSensorSizeDatabase) was inspected at commit `07da7acbf97348405cf859ce76a00ac642ba1fc5`; the [GCMD KMS API](https://gcmd.earthdata.nasa.gov/kms/) supplied mapped records from version 25.3. Additional manufacturer and field-method sources were recorded in the local test audit.

Publisher feedback should identify the exact concept, predicate or relationship, evidence and suggested correction. Check the published data before attributing an export defect to the publisher. Typographical fixes and definition enrichment are distinct from a proposal to restructure categories or mint new concepts. Technical endpoint capabilities do not establish editorial authority to alter a publication.
