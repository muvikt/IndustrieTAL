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
	""" (list of str tuple) --> str
	"""
	
	for tp in email_header:
		









#anonymize the email body
def anonymize_body(email_body):
	pass



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




