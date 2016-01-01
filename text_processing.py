# -*- coding: utf-8 -*-
#!/usr/bin/env python


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




# get the mail header 
def get_header_email(src):
	""" (str) --> list of str tuple
	"""
	parser = HeaderParser()
	h = parser.parsestr(src)
	print h.items()
	return h.items()




# get the mail body text
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




#anonymize the email adresses (from & to)
def anonymize_header(email_header):
	""" (list of str tuple) --> list of str tuple
	"""
	print email_header
	dico_mapping = {}
	patterns = { 'From' : str, 'To' : str, 'Subject' : str}
	for item in email_header:
		string = str(item).replace("(",'').replace(")",'').replace('\'','').replace("\\n\\",'')
		for p in patterns:
			if re.match(p, string):
				string = string.replace(p+",","")
				patterns[p]=(string.split(","))
	for p in patterns:
		if str(p) == 'From' or str(p) == 'To':
			i =0
			for item in patterns[p]:
				i+=1
				if item not in dico_mapping:
					dico_mapping[item] = 'adresse'+str(i)+ "@got.com"
		if str(p) == 'Subject':
			print patterns[p]
			
		


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




