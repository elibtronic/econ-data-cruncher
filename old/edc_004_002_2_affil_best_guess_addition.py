
import csv
from edc_003_auth_affil_best_guess import best_guess

print "adding column of 'best guesses' of affiliation data"
f = csv.reader(open('data/md_built/complete_data.csv','rb'))
csvfile = open ("data/md_built/data_with_best_guess.csv","wb")
o = csv.writer(csvfile , delimiter=',',quotechar='\"',quoting=csv.QUOTE_ALL)
for dline in f:
    print "."
    dline.append(best_guess(dline[4]))
    o.writerow(dline)    
print ".fin"
