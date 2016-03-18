#!/bin/bash python
import os,time
import cPickle as pickle

start = time.time()


fileSeen = 'MACSeen.txt'
fileKnown = 'MACKnown.txt'
newSeen = 'NewMACSeen.txt'
newKnown = {}
name = ""
try:
	seen = list(pickle.load(open(fileSeen, "ab+")))
except:
	print "New Seen File!"
	seen = open(fileSeen, "ab+")
try:
	known = pickle.load(open(fileKnown, "ab+"))
except:
	print "New Known File!"
	known = open(fileKnown, "ab+")

print "Valid names are at least 5 characters, without spaces"
print " "

for item in seen:
	print "Do you have a name for this MAC? ", item
	name = raw_input('Name>>>  ')
	if len(name) > 5:
		newKnown[item] = name
		seen.remove(item)
print known
print "-------------------------------------"
print newKnown
print "The above item(s) are going to be added to the pool of known MAC addresses, ok?"
confirmation = raw_input('Confirm yes, otherwise changes will be discarded> ')
confirmation.lower()
if confirmation == "y":
	confirmation = "yes"
if confirmation == "yes":
	print type(known)
	newKnown = pickle.dumps(newKnown)
	try:
		known.write(newKnown)
	except:
		known = pickle.dumps(newKnown)
		
else:
	print "Changes discarded"
print "-------------------------------------"

#known.close()



finish = time.time()
elapsed = finish - start
print "Report completed in ", elapsed, " seconds."

