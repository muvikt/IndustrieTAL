# -*- coding: utf-8 -*-
#!/usr/bin/env python

#title           : 
#description     : anonymize a sample of enron corpus 
#authors         : anca boca, victoria musatova 
#date            : 30/12/15
#usage           : 
#python_version  : 2.7


#imports
import os
import nltk
import re
import email
from os import listdir
from os.path import isfile, join
from nltk.data import load
from nltk.chunk.api import ChunkParserI
from nltk.chunk.util import (ChunkScore, accuracy, tagstr2tree, conllstr2tree,
                             conlltags2tree, tree2conlltags, tree2conllstr, tree2conlltags,
                             ieerstr2tree)
from nltk.chunk.regexp import RegexpChunkParser, RegexpParser
from email.parser import HeaderParser


""" description program: 
"""



# get the email header 
def get_header_email(src):
	""" (str) --> list of str tuple
	"""
	parser = HeaderParser()
	h = parser.parsestr(src)
	print h.items()
	return h.items()


# get the email body text
def get_body_mail(src):
	""" (str) --> str
	"""	
	complet_email = email.message_from_string(src)	
	body_email = complet_email.get_payload()
	return body_email


# split the email intp header and body
def filter_email(src):
	""" (src) --> list of str tuple, str
	"""
	return get_header_email(src),get_body_mail(src)


# anonymize the email adresses (from & to)
def anonymize_header(email_header):
	""" (list of str tuple) --> list of str tuple
	"""
	return_file = open("retour.txt","w")
	# dict  patterns :  patterns values 
	patterns_header = fill_patternsDico_header(email_header)
	# mapping to, from adresses to anonymized adresses 
	mapping_dict = fill_mapping_dict(patterns_header)
	# transformer le tuple(renvoye par le parseur d'email) en str 
	for item in email_header:
		line_email = str(item).replace("(",'').replace(")",'').replace('\'','').replace("\\n\\",'')
		to_write_line = set_anonymized_line(line_email, mapping_dict)
		return_file.write(to_write_line+"\n")
	return  "results en retour.txt"
				
			
		
def set_anonymized_line(line_email, mapping_dict):
	"""
	"""
	return_line = ""
	for item in  line_email.replace(",","").split():
			if item in mapping_dict:
				#print item, mapping_dict[item]
				return_line += " "+mapping_dict[item]
			else:
				return_line += " "+item
	return return_line 


# fills the mapping dict, from adresses to anonymize to anonymized adresses
def fill_mapping_dict(patterns_header):
	""" (dict) --> dict
	"""

	dico_mapping = {}
	i = 0
	for p in patterns_header:
		if str(p) == 'From' or str(p) == 'To':
			for item in patterns_header[p]:
				print item
				if item not in dico_mapping:
					i+=1
					dico_mapping[item] = 'adresse'+ str(i)+"@got.com"
				else:
					continue
	return dico_mapping
	

# fill the patterns dict : from pattern to pattern value
def fill_patternsDico_header(email_header):
	""" (str) --> dico 
	"""
	patterns = { 'From' : [], 'To' : [], 'Subject' : []}
	for item in email_header:
		line_email = str(item).replace("(",'').replace(")",'').replace('\'','').replace("\\n\\",'')
		for pattern in patterns:
			if re.match(pattern, line_email):
				# ici on recupere la deuxieme partie de la ligne lue
				# exemple: From, amy.chandler@enron.com, on recupere juste amy.chandler@enron.com
				match_string = line_email.replace(pattern+", ","")
				# si plusieurs valeurs, on a besoin de decouper au niveau de la virgule
				vals = match_string.split(",")
				
				if len(vals) >= 2:
					for val in vals:
						
						if val not in patterns[pattern]:
							patterns[pattern].append(val)
				else:
					patterns[pattern] = vals	
	return patterns		
		

#anonymize the email body
def anonymize_body(email_body):
	print email_body	
	tokenized_body = tokenize(email_body)
 	print tokenized_body
 	tagged_body = tag(tokenized_body)
 	print tagged_body
 	get_EN_body = get_EN(tagged_body)
 	print get_EN_body




#return a string without punctuation
def remove_PUNCT(tokens):
	""" (str) --> str 
	"""
	no_punct = [w for w in tokens if w.isalnum()]
	return no_punct



# return tokenized string
def tokenize(contentFile):
	""" (str) --> str
	"""
	print "Tokenize ..."
	#remove punctuation
	tokens = nltk.word_tokenize(contentFile)
	no_punct_tokens = remove_PUNCT(tokens)
	return no_punct_tokens



# return tagged string
def tag(tokenized_content):
	""" (str) --> str
	"""
	print "Tagging ..."
	tagged = nltk.pos_tag(tokenized_content)
	return tagged



#return a list of tuples(name_entity, str)
def get_EN(tagged_content):
	""" (str) --> list of str
	"""
	print "Names entity recognition..."
	lst_EN = list()
	for item in nltk.ne_chunk(tagged_content, binary=True):
		lst_EN.append(item)
	return lst_EN 	




