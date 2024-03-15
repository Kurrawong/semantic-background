# Semantic Background

This repository contains Semantic Web ontologies and vocabularies frequently used by members of [KurrawongAI](https://kurrawong.ai). 

We maintain the currency of these artifacts as best we can so this is a one-stop-shop for most of our daily Semantic Web reference object needs!


## Content

* `originals/` - original RDF files from elsewhere
* `overrides/` - versions of files from `originals/` with processing done to them to improve labels 
* `labels/` - RDF elements' labels only, extracted from `originals/`
* `scripts/` - Python scripts to process RDF files
** `generate.py` - extracts labels from files in `originals/` or their override versions in `overrides/` and places them in `labels/`

## License

Almost all the objects in this repository are licensed by/to others and indicate their licenses within them.

For objects that do not explicitly declare licensing details within them, assume that the [BSD 3-Clause license](https://opensource.org/license/BSD-3-clause/) is in force with the YEAR being this year and the OWNER being [KurrawongAI](https://kurrawong.ai), as per LICENSE.

Yes indeed, there is a copy of the BSD 3-Clause license in RDF in this repository: LICENSE.ttl.

## Contact

See [KurrawongAI's Contact Page](https://kurrawong.ai/contact)
