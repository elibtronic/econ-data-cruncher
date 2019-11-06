import urllib2

from array import array
from bs4 import BeautifulSoup
from types import *
from random import randint
from time import sleep

data_col = open("author_data.csv","w")
bad_an = open("bad_an.csv","w")
sub_data = open("subject_data.csv","w")
abs_data = open("abstract_data.csv","w")

#Metadatr from article into arrays
au_d = []
so_d = []
dt_d = []
sb_d = []
go_d = []
ce_d = []
ab_d = []
aa_d = []
is_d = []
an_d = []
db_d = []

data_elements = ["Authors",
                       "Source",
                       "Document Type",
                       "Subject Terms",
                       "Geographic Terms",
                       "Company/Entity",
                       "Abstract",
                       "Author Affiliations",
                       "ISSN",
                       "Accession Number",
                       "Database"]

    
au_d = [] #0
so_d = [] #1
dt_d = [] #2
sb_d = [] #3
go_d = [] #4
ab_d = [] #5
aa_d = ["placeholder"] #6
is_d = [] #7
an_d = [] #8
db_d = [] #9

soup =  BeautifulSoup(open("47797887.htm"))
brick = soup.find("dl")
i = -1
for d in brick.stripped_strings:
    print d
    if(d=="Authors:"):
        i = 0
    elif(d=="Source:"):
        i = 1
    elif(d=="Document Type:"):
        i = 2
    elif(d=="Subject Terms:"):
        i = 3
##    elif(d=="Geographic Terms:"):
##        i = 4
##    elif(d=="Abstract:"):
##        i = 5
##    elif(d=="Database:"):
##        i = 9
##    elif(d=="Author Affiliations:"):
##        i = 6
##    elif(d=="ISSN:"):
##        i = 7
##    elif(d=="Accession Number:"):
##        i = 8
##    elif(d=="Database:"):
##        i = 9
##    elif(d=="Company/Entity:"):
##        continue
##    elif(d=="Full Text Word Count:"):
##        continue
    else:
        if(i==0):
            au_d.append(d)
        elif(i==1):
            so_d.append(d)
        elif(i==2):
            dt_d.append(d)
        elif(i==3):
            sb_d.append(d)
##        elif(i==4):
##            go_d.append(d)
##        elif(i==5):
##            ab_d.append(d)
##        elif(i==6):
##            try:
##                int(d)
##            except:
##                aa_d.append(d)
##        elif(i==7):
##            is_d.append(d)
##        elif(i==8):
##            an_d.append(d)
##        elif(i==9):
##            db_d.append(d)
##            
##    date = so_d[1].split(',')
##    fd = date[0]
##
##if(len(au_d) == 0):
##    print "nope, no authors"
##    bad_an.write(str(an_index)+"\n")
##    bad_an.flush()
##
##if(len(aa_d) == 1):
##    print "nope, no author affil"
##    bad_an.write(str(an_index)+"\n")
##    bad_an.flush()
##
###Match Author name with associatied affiliation
##oc = 0
##for ad in au_d:
##    if (oc % 2 == 0):
##        #print ad
##        ead = au_d[oc+1].split(",")
##        for e in ead:
##            if((e.encode('ascii')).isdigit() == True):
##                data_line = ",".join([an_d[0],is_d[0],fd.lstrip('\n\r. ').lstrip(),'\"'+ad.rstrip(', ')+'\"','\"'+aa_d[int(e)]+'\"'])
##                print data_line
##                data_col.write(data_line.encode('utf8')+"\n")
##                data_col.flush()
##            else:
##                print "nope,bad author affil"
##    oc += 1
##
###Tabulate Subject terms with associated Accession
##
##for s in sb_d:
##    data_line = ",".join([an_d[0],s])
##    sub_data.write(data_line.encode('utf8')+"\n")
##    sub_data.flush()
##
###Write out Abstract
##data_line = ",".join([an_d[0],'\"'+ab_d[0]+'\"'])
##abs_data.write(data_line.encode('utf8')+"\n")
##abs_data.flush()
##
##sub_data.close()
##data_col.close()
##bad_an.close()
##abs_data.close()
##
##
