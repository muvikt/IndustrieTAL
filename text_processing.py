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
from nltk.tree import *



# get the email header 
def get_header_email(src):
	""" (str) --> list of str tuple
	"""
	parser = HeaderParser()
	h = parser.parsestr(src)
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
	regex_mail_adress = r'\w+\.?\w+@\w+\.[A-za-z]{2,3}'

	# transform the  str tuple into str
	string = ""
	for tpl in email_header:
		string+= tpl[0]+" "+tpl[1]+"\n"
	all_adress_matches = re.findall(regex_mail_adress, string)

	# fill mapping dict
	adresses_map = fill_mapping(all_adress_matches)
	
	# get anonymized text
	anonymized_string = get_anonymized_mail(string, adresses_map) 

	return anonymized_string

# produce anonymized text
def get_anonymized_mail(string, adresses_map):
	""" (str,dict) --> str
	"""
	string_to_return = ""
	new_line = ""
	for line in string.split("\n"):
		for address in adresses_map :
			if address in line:
				new_line = line.replace(address, adresses_map[address])
				string_to_return += new_line +"\n"
	return string_to_return


# fills the mapping dict address_to_anonymize : anomynized_address 		
def fill_mapping(adresses_lst):
	""" (lst of str) --> dict
	"""
	adresses_mapping = {}
	i = 0
	for adress in adresses_lst:
		if adress not in adresses_mapping:
			i+=1
			adresses_mapping[adress] =  "adress_"+ str(i)+ "@got.com"
	return adresses_mapping


# anonymize the email body
def anonymize_body(email_body):
	new=re.sub(r"[0-9]", "*", email_body) #anonymize numbers
	#print "EMAIL \n", new	
	#tokenized_body = 
	##print re.findall(regexs[0],email_body)
 	##print tokenized_body
 	#tagged_body = 
 	en2label = treeNLTK2Dic(get_EN(tag(tokenize(email_body))))
 	en_anonym=anonymizeEN(en2label)
 	for en in en_anonym:
	  new=re.sub(en, en_anonym[en],new)
	return new


# return dictionary of NE {NE:type_NE}
def treeNLTK2Dic(nltkTree):
  en2label={}
  for el in nltkTree:
    if isinstance (el, Tree):
      en="".join(x+' ' for x, y in el).strip(" ")
      en2label[en]=el.label()
  return en2label


def anonymizeEN(dicEN):
  en2anonym={}
  i=1
  for en in dicEN:
    anon="_"+dicEN[en][:3]+str(i)
    en2anonym[en]=anon
    i+=1
  return en2anonym


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
	#print "Tokenize ..."
	#remove punctuation
	tokens = nltk.word_tokenize(contentFile)
	no_punct_tokens = remove_PUNCT(tokens)
	return no_punct_tokens


# return tagged string
def tag(tokenized_content):
	""" (str) --> str
	"""
	#print "Tagging ..."
	tagged = nltk.pos_tag(tokenized_content)
	return tagged


#return a list of tuples(name_entity, str)
def get_EN(tagged_content):
	""" (str) --> list of str
	"""
	#print "Names entity recognition..."
	lst_EN = list()
	for item in nltk.ne_chunk(tagged_content):
		lst_EN.append(item)
	return lst_EN 	




