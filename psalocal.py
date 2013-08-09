#!/usr/local/bin/python
#
# MOD salocal.in of {zimbra}
#
__author__ = 'SebastianBatalla'


import re
import sys
import shutil
import datetime
import os
import argparse

input = open('salocal.cf.in','r+')
output = open('salocal.cf.in.tmp','w')

def count_match(string_match):
	i=0;
	for lines in input.readlines():
		if re.match(string_match, lines):
			i+=1;
	return str(i+1) 

def valid_email(email):
    if email==None:
        return False
    return re.match(r"^[a-zA-Z0-9._%-+]+\@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,}$", email)!=None

def add_spam_words(meta,body,fmeta,rule_sa):
	match_count=count_match(body)
	input.seek(0)
	pattern = re.compile(meta)

	for line in input:	
		a_match = pattern.search( line )
		if ( a_match ): 
			output.write (body+match_count+" /\\b"+rule_sa+"\\b/i"+ '\n' +line[:-1] + " || "+ fmeta + match_count+")\n\n" )
		else:
			output.write(line)
	print "-- Rule added -- \n"

def add_to_blacklist(email_bl):
	if not valid_email(email_bl):
		print "\nNo es un e-mail valido"
		sys.exit()
	else:
		
		for line in input:
			output.write(line)
		output.write ("\nblacklist_to "+ email_bl+"\n")
		
		print "-- Blacklist added -- \n"


def main(n):
	
	parser = argparse.ArgumentParser(description='Admin salocal Zimbra.')
	parser.add_argument('-o','--option', help='\n Agregar a Spam  0 - Palabra de spam (Nivel normal) 1 - Palabra de spam (Nivel alto)  2 - Agregar cuenta a blacklist  3 - Salir',required=True)
	parser.add_argument('-p','--param',help='Palabra de spam / e-mail', required=True)
	n = parser.parse_args()
	
	## Backup
	today = str(datetime.date.today())
	shutil.copy2('salocal.cf.in', 'salocal.in.'+today)

	### Menu ###

	if n.option=="0":
		add_spam_words("meta SPAM_WORDS","body __WORDS","__WORDS",n.param)
	elif n.option=="1":
		add_spam_words("meta SPAM_AGGRESSIVE_WORDS","body __AGGWORDS","__AGGWORDS",n.param)
	elif n.option=="2":
		add_to_blacklist(n.param);
	else:
		sys.exit();

	input.close()
	output.close()

	shutil.copy2('salocal.cf.in.tmp','salocal.cf.in')

if __name__ == '__main__':
	main(sys.argv)
