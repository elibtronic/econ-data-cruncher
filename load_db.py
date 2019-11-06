
#
# Parses AN HTML & Dumps into Couch
#
#
#

import json
import re
import numbers
import urllib
#import urllib2
import couchdb
import types
import os,sys
import shutil
from settings import *
from bs4 import BeautifulSoup


data_in_dir = DATA_BASE+AN_IN
data_out_dir = DATA_BASE+AN_OUT
data_er_dir = DATA_BASE+AN_ERROR
log_file = open(LOG_BASE+AN_PROCESS+"log.txt","a")


try:
    os.mkdir(data_out_dir)
    os.mkdir(data_er_dir)
except:
    print("Folders already exist")

couch = couchdb.Server(CDB_HOST)

try:
    db = couch.create(CDB_NAME)
except:
    db = couch[CDB_NAME]

can_files = os.listdir(data_in_dir+"/")
for meta_c in can_files:
    mid = dict()
    soup = BeautifulSoup(open(data_in_dir+"/"+meta_c))
    #print "\n"+meta_c

    for s in soup.find_all("dt"):
        elements = list()
        m_name = s.text.strip(' :\n')
        m_name = re.sub(r' ','_',m_name)
        for t in s.find_next("dd"):
            if (str(t.encode('utf8').decode('ascii','ignore')).strip() != ""):
                elements.append(str(t.encode('utf8').decode('ascii','ignore')).strip())
            mid[m_name] = elements

    #get the non numerials out
    if 'Accession_Number' in mid:
        temp_acc = re.sub(r'<[^>]*?>', '', str(mid['Accession_Number']).encode('utf8').decode('ascii','ignore'))
        temp_acc = re.sub(r'\\n', '', temp_acc)
        temp_acc = re.sub(r' ','', temp_acc)
        temp_acc = re.sub(r'\[\'','',temp_acc)
        temp_acc = re.sub(r'\'\]','',temp_acc)
        temp_el = list()
        temp_el.append(str(temp_acc).encode('utf8').decode('ascii','ignore').strip())
        mid['id'] = temp_el

    #Remove HTML elements from title
    if 'Title' in mid:
       temp_title = re.sub(r'<[^>]*?>', '', str(mid['Title']).encode('utf8').decode('ascii','ignore'))
       temp_title = re.sub(r'\\n','', temp_title)
       temp_title = re.sub(r'\[\'','',temp_title)
       temp_title = re.sub(r'\'\]','',temp_title)
       temp_title = temp_title.strip()
       temp_el = list()
       temp_el.append(str(temp_title).encode('utf8').decode('ascii','ignore').strip(" "))
       mid['Title_Clean'] = temp_el

    #Remove <br /> from various fields
    if 'Subject_Terms' in mid:
        temp_el = list()
        for sub in mid['Subject_Terms']:
            if (sub != "<br/>"):
                temp_el.append(sub)
        mid['Subject_Terms_Clean'] = temp_el

    if 'Authors' in mid:
        temp_el = list()
        for sub in mid['Authors']:
            if (sub != "<br/>"):
                temp_el.append(sub)
        del mid['Authors']
        mid['Authors'] = temp_el

    if 'Author_Affiliations' in mid:
        temp_el = list()
        for sub in mid['Author_Affiliations']:
            if (sub != "<br/>"):
                temp_el.append(sub)
        del mid['Author_Affiliations']
        mid['Author_Affiliations'] = temp_el


    #Create clean versions of lists
    if  'Author_Affiliations' in mid:
        temp_el = list()
        for sub in mid['Author_Affiliations']:
            if not(re.match('^<sup>',sub)):
                temp_el.append(sub)
        mid['Author_Affiliations_Clean'] = temp_el

    #Create short version of Source
    if 'Source' in mid:
        splits = str(mid['Source']).split(',')
        final = splits[0].split(".")
        temp_el = list()
        temp_el.append(final[1].strip())
        mid['Source_Clean'] = temp_el

    try:
        response = db.save(mid)
    except:
        report = meta_c + ":: couldn't save to couch\n"
        print(report)
        log_file.write(report)
        log_file.flush()
        shutil.move(data_in_dir+"/"+meta_c,data_er_dir)
        continue

    report = meta_c + ":: "+str(response)+"\n"
    print(report)
    log_file.write(report)
    log_file.flush()
    try:
        shutil.move(data_in_dir+"/"+meta_c,data_out_dir)
    except:
        print(data_in_dir+"/"+meta_c+" has already been processed")
        shutil.move(data_in_dir+"/"+meta_c,data_er_dir)

log_file.close()
print("\nfin")
