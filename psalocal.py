#!/usr/local/bin/python
#
# MOD salocal.in of {zimbra}
#
import re
import sys
import shutil
import datetime
import os

## Backup
today = str(datetime.date.today())
shutil.copy2('salocal.cf.in', 'salocal.in.'+today)

input = open('salocal.cf.in','r+')
output = open('salocal.cf.in.tmp','w')

def count_match(string_match):
	i=0;
	for lines in input.readlines():
		if re.match(string_match, lines):
			i+=1;
	return str(i+1) 


def add_spam_words(meta,body,fmeta):
	match_count=count_match(body)
	input.seek(0)
	rule_sa=raw_input('Rule: ')
	pattern = re.compile(meta)

	for line in input:	
		a_match = pattern.search( line )
		if ( a_match ): 
			output.write (body+match_count+" /\\b"+rule_sa+"\\b/i"+ '\n' +line[:-1] + " || "+ fmeta + match_count+")\n\n" )
		else:
			output.write(line)
	print "-- Rule added -- \n"

def add_to_blacklist():
	bl_sa=raw_input('Blacklist to: ')
	
	for line in input:
		output.write(line)
	output.write ("\nblacklist_to "+ bl_sa+"\n")
	
	print "-- Blacklist added -- \n"
	
### Menu ###

n=raw_input("\n Agregar a Spam \n 0 - Palabra de spam (Nivel normal) \n 1 - Palabra de spam (Nivel alto) \n 2 - Agregar cuenta a blacklist \n 3 - Salir \n")


if n=='0':
	add_spam_words("meta SPAM_WORDS","body __WORDS","__WORDS");
elif n=='1':	
	add_spam_words("meta SPAM_AGGRESSIVE_WORDS","body __AGGWORDS","__AGGWORDS");
elif n=='2':
	add_to_blacklist();
else:
	sys.exit();

input.close()
output.close()

shutil.copy2('salocal.cf.in.tmp','salocal.cf.in')
