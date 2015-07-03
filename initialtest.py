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

subnetping = os.popen('nmap -sP 192.168.1.0/24')
#print subnetping
known = pickle.load(open(fileKnown, "rb"))
seen = pickle.load(open(fileSeen, "rb"))
abnormal = pickle.load(open(fileAbnormal, "rb"))


allDevices = []
device = {}
knownCount = 0
unknownCount = 0
newCount = 0
issues = 0
unknownMACs = []

ar = os.popen('arp -a -v')
time.sleep(.25)
for line in ar.readlines():
    #print line
    item = line.split()
    if item[3] in known:
        print 'I know MAC ', item[3], ' is ', known[item[3]]
        knownCount = knownCount+1
    elif item[3] in seen:
        print 'I have seen ', item[3], ' but I do not have more info.  IP=', item[1], " it idenbtifies as: ", item[0]
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
print "There are ", unknownCount, " systems that I have seen before, but cannot name."
print "There are ", newCount, " systems that I have not seen before."
print "And there are ", issues, "systems with issues."

seen = unknownMACs

pickle.dump(known, open(fileKnown, "wb"))
pickle.dump(seen, open(fileSeen, "wb"))
pickle.dump(abnormal, open(fileAbnormal,"wb"))

finish = time.time()
elapsed = finish - start
print "Report completed in ", elapsed, " seconds."


    



