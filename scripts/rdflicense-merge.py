"""
This script acquires and then merges individual RDF License files from ODRL's Best Practice:

https://github.com/w3c/odrl/tree/master/bp/license/rdflicense

API at https://api.github.com/repos/w3c/odrl/contents/bp/license/rdflicense
"""

import rdflib
import creds
from github import Github
from github import Auth

# # acquire all licenses
# auth = Auth.Token(creds.gh_token)
#
# g = Github(auth=auth)
# repo = g.get_repo("w3c/odrl")
# for f in repo.get_contents("bp/license/rdflicense"):
#     c = repo.get_contents(f.path)
#     raw_rdf = c.decoded_content
#     pretty_rdf = rdflib.Graph().parse(data=raw_rdf).serialize(format="longturtle").replace("\\r", "").replace("\n\n", "\n")
#     with open(f"individual-licenses/{c.name}", "w") as x:
#         print(f"Save {c.name}")
#         x.write(pretty_rdf)


# combined licenses
import glob
g = rdflib.Graph()
for f in glob.glob("individual-licenses/*.ttl"):
    g.parse(f)
    print(len(g))

g.serialize(format="longturtle", destination="rdflicenses.ttl")
