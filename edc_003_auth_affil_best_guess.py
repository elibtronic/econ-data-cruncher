
#
# Attempts to normalize Author affiliation data by grepping
# puts results in Author_Affliations_Best_Guess
#
#
#

import couchdb
import re

count = 0

#Magic grep function that will attempt to create a standard affiliation name
def best_guess(dirty_affil):

    bg = dirty_affil



    if (re.search(" University of (.+?)[,.]",bg)):
        bg = re.search(" University of (.+?)[,.]",bg)
        bg = bg.group(0)
    if (re.search("(.+?) University[,. ]",bg)):
        bg = re.search("(.+?) University[,. ]",bg)
        bg = bg.group(0)

    if(re.search("and",bg)):
       return bg

    #Remove Dept Affils
    bg = re.sub("Department of Economics, ","",bg)
    bg = re.sub("Dept of Economics, ","",bg)
    bg = re.sub("Department of Finance, ","",bg)
    bg = re.sub("Department of Statistics, ","", bg)
    bg = re.sub("Department of Telecommunications", "",bg)
    bg = re.sub("Dept. of Economics, ","",bg)
    bg = re.sub("Economics Department, ","",bg)
    bg = re.sub("Department of Mathematics, ","",bg)
    bg = re.sub("Faculty of Economics, ","",bg)
    bg = re.sub("Departments of Mathematics and Statistics, ","",bg)

    #trim leading & trailing , ' ' . if still there
    bg = re.sub(",$","",bg)
    bg = re.sub(" $","",bg)
    bg = re.sub("^,","",bg)
    bg = re.sub("^ ","",bg)
    #remove " that were already in the affil statement
    bg = re.sub("\"","",bg)
    #bg = re.sub("^.","",bg)
    #bg = re.sub(".$","",bg)

    return bg




couch = couchdb.Server()
db = couch['econ_data']
map_fun = '''function(doc) {
  if (doc.Document_Type == "Article" && doc.Authors != null && doc.Author_Affiliations != null)
  emit(doc.id, {ACCESSION : doc.id, AUTHORS_CLEAN : doc.Authors_Clean, ISSN : doc.ISSN, DATE : doc.Source_Clean, AFFILS : doc.Author_Affiliations_Clean, AFFIL_RAW : doc.Author_Affiliations, AUTHORS_RAW : doc.Authors});
}'''

print "Working on best guesses..."
results = db.query(map_fun)
for r in results:
    print "."
    art_obj = r["value"]
    accession = art_obj['ACCESSION']
    date = art_obj['DATE']
    affil_raw = art_obj['AFFIL_RAW']
    affil_clean = art_obj['AFFILS']
    autho_raw = art_obj['AUTHORS_RAW']
    issn = art_obj['ISSN']
    bglist = list()
    for df in affil_clean:
        if re.search("and",df):
            count += 1
        bglist.append(best_guess(df))
    doc = db[r.id]
    doc['Author_Affliations_Best_Guess'] = bglist
    db.save(doc)   
#        print bglist
    
print ".fin"
print count

        
