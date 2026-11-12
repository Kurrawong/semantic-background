---
name: vocpub-definition
description: Investigate missing SKOS concept definitions for VocPub requirement 2.3.01 and propose evidence-backed definitions with provenance. Use for definition enrichment or remediation of definition validation results.
metadata:
  version: "0.1.0-draft"
  semantic-metadata: "metadata.ttl"
---

# VocPub Definition Skill

Produce defensible proposals for missing `skos:definition` values on `skos:Concept` instances. A successful investigation can conclude that evidence is insufficient. Conformance alone does not establish that a proposed definition is accurate.

## Establish the task

Identify the input vocabulary, affected concept IRIs, target language, and applicable VocPub specification and validator versions. Use supplied validation results where available; inspect their focus node, result path, source shape and constraint component rather than relying on message text. For a missing definition, confirm that the concept actually has no definition in the supplied graph. A missing requested translation is an enrichment request, not necessarily a VocPub violation.

The [current requirement 2.3.01](https://agldwg.github.io/vocpub-profile/specification.html#2.3.01) requires at least one textual definition and permits only one per language. It also constrains preferred labels; this Skill addresses definitions. Verify the chosen release and validator rather than assuming every release or variant is identical. Report a specification/validator discrepancy instead of silently changing the rule. Multiple, nontextual or otherwise invalid existing definitions need separate diagnosis; do not overwrite them as if they were absent.

## Gather and assess evidence

Read existing documentation and the immediate concept neighbourhood first. Inspect concept-level and scheme-level `schema:citation`, `dcterms:source`, `prov:wasDerivedFrom`, `rdfs:isDefinedBy` and relevant history/provenance notes. A scheme citation is a search lead, not evidence that a particular passage defines every concept. Follow cited resources when accessible within the task; record inaccessible resources without claiming to have read them. Handle literal citations and resource-valued documentation as well as direct text.

Use this default preference order for candidate evidence. It is editorial guidance, not a VocPub rule or a numerical confidence scale. Explain departures when local evidence is more authoritative or better matches the intended meaning.

1. **A directly applicable definition in the vocabulary's authoritative source.** Establish the concept correspondence and capture the exact passage, edition and locator. Preserve its intended scope.
2. **Definition-bearing documentation already attached to the concept.** Evaluate `skos:note` and `skos:scopeNote` by their content. Propose the same wording as a definition when it already explains the meaning adequately; preserve the original property and record the duplication. Otherwise identify the adaptation required. Usage restrictions and examples alone need more evidence.
3. **A definition on a mapped external concept, especially `skos:exactMatch`.** Check the external authority, domain, scope, version and wording against the local concept. A mapping is a discovery aid, not an instruction to copy. `skos:exactMatch` does not entail inheritance of documentation; weaker mappings justify less confidence. Check reuse terms and attribution before proposing verbatim reuse; record unresolved terms for review.
4. **A synthesis from several documented sources.** Combine local notes, examples and corroborating sources only where they support the same interpretation. Trace each substantive claim to evidence. Label translations and adaptations explicitly.
5. **A tentative formulation from labels and semantic relations.** Use `skos:prefLabel`, `skos:altLabel`, broader/narrower concepts and related concepts to constrain an interpretation. Do not treat `skos:broader` as necessarily a genus: SKOS hierarchies can include partitive and instance relationships. Examples do not establish exhaustive boundaries. State assumptions and missing distinguishing characteristics; abstain if the graph leaves the intended meaning ambiguous.

Assess authority, semantic fit, evidence completeness, language, currency and reuse conditions separately. Source rank describes an evidence route; it does not determine confidence. Check conflicting evidence even after finding a plausible candidate. Present unresolved conflicts for editorial decision.

## Propose a definition

Prefer a concise explanation of the concept's meaning in its vocabulary context. Include distinguishing characteristics only when supported. Avoid circular restatements of a label, unexplained specialist terms, and facts introduced merely to make the wording sound complete. Do not turn a usage instruction into an asserted defining characteristic.

Keep the original graph intact while investigating. Supply a proposed addition and its evidence record. Apply changes when the user has authorised editing; otherwise return proposals. A request for public publication requires its own task scope. Revalidate edited data against the selected validator and report remaining results. Keep semantic adequacy and validation outcome distinct.

For each affected concept, return:

- Concept IRI, preferred label, target language and triggering requirement or enrichment request.
- Proposed definition, or an explicit insufficient-evidence outcome with the missing evidence identified.
- Evidence resources and relevant passages or triples, including page/section or property, source version and access date for fetched material.
- Method: verbatim reuse, duplication of local documentation, adaptation, translation, synthesis or tentative formulation.
- Rationale, conflicting evidence, uncertainties and reuse/attribution considerations.
- Proposed RDF addition, editorial review status, and validation outcome if the proposal was applied.

Keep proposal provenance separate from established provenance of the concept. If recording execution in RDF, describe the run as a `prov:Activity`, the responsible agent through `prov:qualifiedAssociation`, this Skill as its `prov:hadPlan`, and each proposal as a `prov:Entity` generated by that activity and derived from the evidence actually used. A run may also record evidence inspected but rejected using `prov:used` with explanatory notes. Do not imply an editor approved a proposal merely because it was generated.

## Semantic publication

[metadata.ttl](metadata.ttl) describes this draft using existing vocabularies. Its proposed Skill IRI is `https://linked.data.gov.au/def/vocpub/skill/definition`; registration and resolution are not asserted. Establish creator/maintainer attribution and a licence before public release. It supplies an example PROF guidance descriptor but does not assert that VocPub has adopted it. This package is a working instance, not a proposed Skill ontology or conformance profile.

The portable directory follows the [Agent Skills format](https://agentskills.io/specification). [DASH Suggestions](https://datashapes.org/suggestions.html) is a relevant RDF precedent for representing proposed repairs; no DASH execution support is required by this Skill. [SKOS documentation properties](https://www.w3.org/TR/skos-reference/#notes) and [mapping properties](https://www.w3.org/TR/skos-reference/#mapping) retain their existing semantics.
