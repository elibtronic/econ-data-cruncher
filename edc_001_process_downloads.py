#
# Step 1 in Z
#
#
from settings import *
from bs4 import BeautifulSoup
import os,sys
import shutil
import urllib2
from array import array
from bs4 import BeautifulSoup
from types import *
from random import randint
from time import time

html_data_in = DATA_BASE+TOC_IN
html_data_out = DATA_BASE+TOC_OUT
data_in = DATA_BASE+AN_IN
error_dir = DATA_BASE+TOC_ERROR

uagents = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
           'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
           'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0',
           'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14',
           'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52',
           'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
           'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
           'Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)']

log_file = open(LOG_BASE+TOC_PROCESS+"log.txt","a")


can_files = os.listdir(html_data_in+"/")
for html_c in can_files:
    val_count = 0
    soupAN = BeautifulSoup(open(html_data_in+"/"+html_c))
    ans = []
    #build list of ANs found in html candidate document
    for s in soupAN.findAll('cite'):
        ans.append(s.text[4:])
        #ans.sort()
    print "\nProcessing...\n"+html_c+"\n"+ans[0]," : ",len(ans)
    #do the downloading
    tss = time()
    for an_index in ans:
        ua_string = uagents[randint(0,len(uagents)-1)]
        headers = {'User-agent': ua_string }
        req = urllib2.Request(E_URL+str(an_index), None, headers)
        html_result = urllib2.urlopen(req).read()
        soupMD = BeautifulSoup(html_result)
        brick = soupMD.find("dl")
        val_count += 1
        ofile = open(data_in+"/"+str(an_index)+".htm","w")
        ofile.write(brick.prettify().encode('utf8'))
        ofile.flush()
        ofile.close()
    time_delta = time() - tss
    print"Downloaded in: "+str(time_delta)+" sec"
    report = "\n"+html_c+" : "+"Start AN: "+str(ans[0])+" offset of "+str(len(ans))+" records downloaded in "+str(time_delta)
    log_file.write(report)
    log_file.flush()
    try:
        shutil.move(html_data_in+"/"+html_c,html_data_out)
    except:
        print html_data_in+"/"+html_c+" has already been processed"
        shutil.move(html_data_in+"/"+html_c,error_dir)

log_file.close()
print "\nfin"
