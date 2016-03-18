#!/bin/bash python
##import nmap
import os, time
import cPickle as pickle
##nm = nmap.PortScanner()
##scan = nm.scan('192.168.1.1-254', arguments='-sP -sS')
##print scan
start = time.time()
fileKnown = 'MACKnown.txt'
fileSeen = 'MACSeen.txt'
fileAbnormal = 'MACAbnormal.txt'

subnetping = os.popen('nmap -PR 192.168.1.0/24')
#print subnetping
try:
	known = pickle.load(open(fileKnown, "ab+"))
except:
	known = open(fileKnown, "ab+")
try:
	seen = pickle.load(open(fileSeen, "ab+"))
except:
	seen = open(fileSeen, "ab+")
try:
	abnormal = pickle.load(open(fileAbnormal, "ab+"))
except:
	abnormal = open(fileSeen, "ab+")

allDevices = []
device = {}
knownCount = 0
unknownCount = 0
newCount = 0
issues = 0
unknownMACs = []

ar = os.popen('arp -a -v')
time.sleep(1)
for line in ar.readlines():
    #print line
    item = line.split()
    if item[3] in known:
        print 'I know MAC ', item[3], ' is ', known[item[3]], ' with an IP address of ', item[1]
        knownCount = knownCount+1
    elif item[3] in seen:
        print 'I have seen ', item[3], ' but I do not have more info.  IP=', item[1], " it identifies as: ", item[0]
        unknownCount = unknownCount+1
        unknownMACs.append(item[3])
    elif item[3] in abnormal:
        print 'There is something wrong at IP ', item[1], 'the MAC is ', item[3]
        issues = issues + 1
    else:
        if item[0] != 'Entries:':
            print 'I do not know MAC ', item[3] , ' at ', item[1]
            newCount = newCount + 1
            unknownMACs.append(item[3])

print "------------------------------------------------------"
print " "
print "There are ", knownCount, " recognized systems."
print "There are ", unknownCount, " systems that I have seen before, but have not been given names."
print "There are ", newCount, " systems that I have not seen before."
print "And there are ", issues, "systems with issues."

#pickle.dump(unknownMACs,fileSeen)
#seen.write(unknownMACs)
#fileSeen.close()
#print "Seen pickled and closed"



#pickle.dump(known, open(fileKnown, "wb"))
#print seen
pickle.dump(unknownMACs, open(fileSeen, "wb"))
#pickle.dump(abnormal, open(fileAbnormal,"wb"))

finish = time.time()
elapsed = finish - start
print "Report completed in ", elapsed, " seconds."


    



