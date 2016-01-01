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
from os import listdir
from os.path import isfile, join
from text_processing import *


# List all the subdirs of rootd
# returns a list of string
def listSubDirs(rootd):
	""" (str) --> lst of str
	"""
	subdirs = list()
	for subd in os.listdir(rootd):
		orgd=rootd+"/"+subd
		if os.path.isdir(orgd):
		  subdirs.append(orgd)
	return subdirs


def listFiles(subdirs):
  files=[]
  for subd in subdirs:
    for file in os.listdir(subd):
      filename=subd+"/"+file
      files.append(filename)
  return files


def main():
	#print listSubDirs('scott-s')
	contentFile = open("mail.txt",'r').read()
	header_email,body_email = filter_email(contentFile)
	anonymize_header(header_email)
	print anonymize_header(header_email)

 	


if __name__ == '__main__':
	main()