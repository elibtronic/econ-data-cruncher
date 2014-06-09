
#
# Read CouchDB entires and spit out abs data
#
#
#
#

import couchdb
import re

abs_list = open("data/md_built/abs_list.csv","w")
couch = couchdb.Server()
db = couch['econ_data']
map_fun = '''function(doc) {
  if (doc.Document_Type == "Article" && doc.Authors != null && doc.Author_Affiliations != null)
  emit(doc.id, {ACCESSION : doc.id, ISSN : doc.ISSN, ABSTRACT: doc.Abstract});
}'''

count = 0

results = db.query(map_fun)
for r in results:
    count += 1
    art_obj = r["value"]
    accession = art_obj['ACCESSION']
    issn = art_obj['ISSN']

    #DEBUG
    #line_out = str(r.id) + "," + str(accession[0])+","+str(issn[0])+","

    line_out = str(accession[0])+","+str(issn[0])+","
    
    if 'ABSTRACT' in art_obj.keys():
        ab_total = ' '.join(art_obj['ABSTRACT'])
        ab_total = re.sub('<[^<]+?>', '', ab_total)
        ab_total = re.sub('\n','',ab_total)
        ab_total = re.sub('\"','\""',ab_total)
        ab_total = re.sub(',','"",',ab_total)
        line_out += "\"" + ab_total + "\""
    else:
        line_out += "\"NO_ABSTRACT\""
        
    abs_list.write(line_out+"\n")
    abs_list.flush()
