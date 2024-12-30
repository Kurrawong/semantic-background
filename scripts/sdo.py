pattern = r"rdfs:label \"(.*[a-z])([A-Z])(.+)\""

replace = 'rdfs:label "$1 \L$2$3"'

# run until none found
