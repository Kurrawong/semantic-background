f="survey-provenance"
sed '/^#/d' "$f.ttl" > "$f.2.ttl"
sed '/^$/d' "$f.2.ttl" > "$f.3.ttl"
kurra file reformat "$f.3.ttl" -o "$f.4.ttl"
kurra sparql "$f.4.ttl" 01-name.sparql > "$f.5.ttl"
kurra sparql "$f.5.ttl" 02-description.sparql > "$f.6.ttl"
kurra sparql "$f.6.ttl" 04-isDefinedBy.sparql > "$f.7.ttl"
kurra sparql "$f.7.ttl" 03-count-name.sparql
kurra sparql "$f.7.ttl" 04-count-desc.sparql
rm "$f.ttl"
rm "$f.2.ttl"
rm "$f.3.ttl"
rm "$f.4.ttl"
rm "$f.5.ttl"
rm "$f.6.ttl"
mv "$f.7.ttl" "$f.ttl"
kurra shacl validate "$f.ttl" 9 -hw
