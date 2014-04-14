
#
# Read CouchDB entires as JSON and spit out CSV
#
#
#
#

import couchdb
import re

total_w_na = 0
final_list = open("data/md_built/complete_data.csv","w")
break_list = open("data/md_built/break_list_author_affil.csv","w")
couch = couchdb.Server()
db = couch['econ_data']
map_fun = '''function(doc) {
  if (doc.Document_Type == "Article" && doc.Authors != null && doc.Author_Affiliations != null)
  emit(doc.id, {ACCESSION : doc.id, ISSN : doc.ISSN, DATE : doc.Source_Clean, AFFILS : doc.Author_Affiliations_Clean, AFFIL_RAW : doc.Author_Affiliations, AUTHORS_RAW : doc.Authors});
}'''

results = db.query(map_fun)
print "Computing List of matched Authors & Affiliations..."
for r in results:
    print "."
    art_obj = r["value"]
    accession = art_obj['ACCESSION']
    date = art_obj['DATE']
    affil_raw = art_obj['AFFIL_RAW']
    autho_raw = art_obj['AUTHORS_RAW']
    issn = art_obj['ISSN']

    au_left = dict()
    af_list = dict()

    for af in range(0,len(affil_raw)):
        caf = re.sub(r'<[^>]*?>','',affil_raw[af])
        caf = re.sub(r'\n', '', caf)
        try:
            af_list[int(caf.strip())] = affil_raw[af+1]
        except:
            pass




    a_moving = []

    for ak in autho_raw:
        if (not re.search(r'<cite>',ak)):
            a_moving.append(ak)


    count = 0
    stopper = False
    while(stopper == False):
        try:
            a_moving[count+1]
            #print "IT :::",a_moving,"count",count,
            if (re.search(r'NA',a_moving[count])):
                break
            elif (not re.search(r'<sup>',a_moving[count+1])and not re.search(r'NA',a_moving[count+1])):
                total_w_na += 1
                a_moving.insert(count+1,"NA")
            count += 2
        except:
            stopper = True


    #Last element in author list needs to be a sup, indicating affiliations, if not NA
    if (not re.search(r'<sup>',a_moving[-1])):
        a_moving.append("NA")

##    count = 0
##    stopper = False
##    while(stopper == False):
##        print "IT :::",a_moving,"count",count,"a_moving",a_moving[count+1]
##        if (count == (len(a_moving))):
##            if(not re.search(r'<sub>',a_moving[count])):
##                print "1"
##                a_moving.append("NA")
##            stopper = True
##            break
##        elif (re.search(r'NA',a_moving[count])):
##            print "2"
##            count += 1
##            continue
##        elif (not re.search(r'<sup>',a_moving[count+1])):
##            print "3"
##            a_moving.insert(count+1,"NA")
##        else:
##            count += 1
##        
    
##    for a_index in range(0,len(a_moving)):
##        if (a_index == len(a_moving) - 1):
##            break
##        if (a_index % 2 == 0 and not re.search(r'<sup>',a_moving[a_index+1])):
##            a_moving.insert(a_index+1,"NA")

    
    for au in range(0,len(a_moving)):
        if (au == len(a_moving) -1):
            break
        if(a_moving[au + 1] == "NA"):
            #Spit out
            #print str(accession[0])+','+str(issn[0])+','+str(date[0]),',\"'+str(a_moving[au])+'\",\"No Affiliation\"\n'
            final_list.write(str(accession[0])+','+str(issn[0])+','+str(date[0])+',\"'+str(a_moving[au])+'\",\"No Affiliation\"\n')
            final_list.flush()
        elif(au % 2 == 0):
            au_vals = re.sub(r'<sup>','',a_moving[au+1])
            au_vals = re.sub(r'</sup>','',au_vals)
            au_vals = re.sub(r'\n','',au_vals).strip()
            for e in au_vals.split(','):
                #print str(accession[0])+','+str(issn[0])+','+str(date[0])+',\"'+str(a_moving[au])+'\"',',\"'+af_list[int(e)]+'\"\n'
                try:
                    final_list.write(str(accession[0])+','+str(issn[0])+','+str(date[0])+',\"'+str(a_moving[au])+'\",\"'+af_list[int(e)]+'\"\n')
                except:
                    break_list.write(r['id']+"\n")
                final_list.flush()
                break_list.flush()
final_list.close()
break_list.close()
print ".fin"
print "Total articles with NA components ",total_w_na

        
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
