
#
# Read CouchDB entires as JSON and spit out CSV
#
#
#
#

import couchdb
import re

#final_list = open("complete_data_easy.csv","w")
sub_list = open("data/md_built/subject_list.csv","w")
couch = couchdb.Server()
db = couch['econ_data']
map_fun = '''function(doc) {
  if (doc.Document_Type == "Article" && doc.Authors != null && doc.Author_Affiliations != null)
  emit(doc.id, {ACCESSION : doc.id, ISSN : doc.ISSN, SUBJECT: doc.Subject_Terms_Clean});
}'''

count = 0

results = db.query(map_fun)
for r in results:
    count += 1
    art_obj = r["value"]
    accession = art_obj['ACCESSION']
    issn = art_obj['ISSN']

    line_out = str(accession[0])+","+str(issn[0])
    if 'SUBJECT' in art_obj.keys():
        for s in art_obj['SUBJECT']:
            sub_list.write(line_out + "," + s + "\n")
    else:
        sub_list.write(line_out + ", NO_SUBJECTS\n")
        
    #sub_list.write(line_out+"\n")
    sub_list.flush()

##    for af in affil_clean:
##        print count," ::: ",str(accession[0])+','+str(issn[0])+','+str(date[0])+',\"'+str(af)+'\"'
##        final_list.write(str(accession[0])+','+str(issn[0])+','+str(date[0])+',\"'+str(af)+'\"\n')
##        final_list.flush()
##        count +=1

#final_list.close()


        
##        if (not re.search(r'<sup>',a_moving[au])):
##            au_vals = re.sub(r'<sup>','',a_moving[au+1])
##            au_vals = re.sub(r'</sup>','',au_vals)
##            au_vals = re.sub(r'\n','',au_vals).strip()
##            if (a_moving[au] == "NA"):
##                print a_moving[max(0,au-1)],"NA"
##            else:
##                for e in au_vals.split(','):
##                    print a_moving[au],af_list[int(e)]
        
        
        

    #        print str(accession[0]),str(issn[0]),str(date[0]),'\"'+a+'\"'
