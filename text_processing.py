# -*- coding: utf-8 -*-
#!/usr/bin/env python

#title           : text_processinng.py
#description     : anonymize a sample of enron corpus 
#authors         : anca boca, victoria musatova 
#date            : 08/01/15
#usage           : python text_processinng.py
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

class Anonymizer():
 
  def __init__(self):
    self.entity2anonymized={} #dictionnaire des elements à anonymiser et leurs formes anonymes
    self.regex_mail_address = r'\w+\.?\w+@\w+\.[A-za-z]{2,3}'

  # get the email header 
  def get_header_email(self, src):
	  """ (str) --> list of str tuple
	  """
	  parser = HeaderParser()
	  h = parser.parsestr(src)
	  return h.items()


  # get the email body text
  def get_body_mail(self, src):
	  """ (str) --> str
	  """	
	  complet_email = email.message_from_string(src)	
	  body_email = complet_email.get_payload()
	  return body_email


  # split the email intp header and body
  def filter_email(self,src):
	  """ (src) --> list of str tuple, str
	  """
	  return self.get_header_email(src),self.get_body_mail(src)


  # anonymize the email adresses (from & to)
  def anonymize_header(self, email_header):
	  """ (list of str tuple) --> str
	  """
	  

	  # transform the  str tuple into str
	  string = ""
	  for tpl in email_header:
		  string+= tpl[0]+": "+tpl[1]+"\n"
	  all_adress_matches = re.findall(self.regex_mail_address, string)

	  
	  
	  # fill mapping dict
	  self.entity2anonymized = self.fill_mapping(all_adress_matches)
	  en2label = self.treeNLTK2Dic(self.get_EN(self.tag(self.tokenize(string))))
	  self.anonymizeEN(en2label)

	  #anonymization
	  string=re.sub(r"[0-9]", "*", string) #anonymization des chiffres
	  for en in self.entity2anonymized:
		  string = string.replace(en, self.entity2anonymized[en])
	  
	  return string
	  
	  
  # fills the mapping dict address_to_anonymize : anomynized_address 		
  def fill_mapping(self, adresses_lst):
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
  def anonymize_body(self, email_body):
	  """ str --> str
	  """
	  
	  new=re.sub(r"[0-9]", "*", email_body) #anonymize numbers
	  
	  #anonymize mails
	  all_adress_matches = re.findall(self.regex_mail_address, email_body)
	  self.entity2anonymized.update(self.fill_mapping(all_adress_matches))
	  
	  #anonymize NE
	  en2label = self.treeNLTK2Dic(self.get_EN(self.tag(self.tokenize(email_body))))
	  self.anonymizeEN(en2label)
	  for en in self.entity2anonymized:
	    new=re.sub(en, self.entity2anonymized[en],new)
	    
	  return new


  # return dictionary of NE {NE:type_NE}
  def treeNLTK2Dic(self, nltkTree):
	  """ Tree_EN_NLTK --> dict{entite_nommee:type_EN}
	  """
	  en2label={}
	  for el in nltkTree:
		  if isinstance (el, Tree):
			  en="".join(x+' ' for x, y in el).strip(" ")
			  en2label[en]=el.label()

	  return en2label

  #add recognized and anonymized NE in self.entity2anonymize
  def anonymizeEN(self, dicEN):
	  """ update self.entity2anonymized
	  """
	  i=1
	  for en in dicEN:
	      
		  if en not in self.entity2anonymized:
		    anon="_"+dicEN[en][:3]+str(i)
		    self.entity2anonymized[en]=anon
		    i+=1



  #return a string without punctuation
  def remove_PUNCT(self,tokens):
	  """ (str) --> str 
	  """
	  no_punct = [w for w in tokens if w.isalnum()]
	  return no_punct


  # return tokenized string
  def tokenize(self,contentFile):
	  """ (str) --> str
	  """
	  #remove punctuation
	  tokens = nltk.word_tokenize(contentFile)
	  no_punct_tokens = self.remove_PUNCT(tokens)
	  return no_punct_tokens


  # return tagged string
  def tag(self,tokenized_content):
	  """ (str) --> str
	  """
	  tagged = nltk.pos_tag(tokenized_content)
	  return tagged


  #return a list of tuples(name_entity, str)
  def get_EN(self, tagged_content):
	  """ (str) --> list of str
	  """
	  lst_EN = list()
	  for item in nltk.ne_chunk(tagged_content):
		  lst_EN.append(item)
	  return lst_EN 	




