# Semantic Background

This repository contains tidy versions of Semantic Web ontologies and vocabularies frequently used by members of [KurrawongAI](https://kurrawong.ai). 

We keep copies of them all here, so they are in one pace, and we tidy up labels etc., without altering any ontological content.

We maintain the currency of these artifacts as best we can, so this is a one-stop-shop for most of our daily Semantic Web reference object needs!



## Content

Most users of this repo will only need the `annotations/` & `ontologies/` folders.

* `annotations/` - labels, descriptions and seeAlso links only from all ontologies
  * `annotations.trig` - a trig (quads) file containing all the annotation RDF file contents
* `ontologies/` - full ontologies, either originals or with annotation updates only (neater labels etc.)
* `originals/` - the original ontologies, manual overrides and scripts needed to generate the content of the `annotations/` & `ontologies/` folders 
* `overrides/` - manually edited versions of the original ontology files, only altering stylistic aspects of annotations

There are two Catalogue declarations too:

* `catalogue-annotations.ttl` - definition of the 'Semantic Background Ontologies' catalogue
  * `manifest-annotations.ttl` - the manifest for the catalogue using `annotations.trig` for all Resources
* `catalogue-ontologies.ttl` - definition of the 'Semantic Background Annotations' catalogue
  * `manifest-ontologies.ttl` - the manifest for the catalogue using `annotations.trig` for all Resources

## License

Almost all the objects in this repository are licensed by/to others and indicate their licenses within them.

For objects that do not explicitly declare licensing details within them, assume that the [BSD 3-Clause license](https://opensource.org/license/BSD-3-clause/) is in force with the YEAR being this year and the OWNER being [KurrawongAI](https://kurrawong.ai), as per LICENSE.

Yes indeed, there is a copy of the BSD 3-Clause license in RDF in this repository: LICENSE.ttl.

## Contact

See [KurrawongAI's Contact Page](https://kurrawong.ai/contact)
