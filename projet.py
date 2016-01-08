# -*- coding: utf-8 -*-
#!/usr/bin/env python

#title           : projet.py
#description     : anonymize a sample of enron corpus 
#authors         : anca boca, victoria musatova 
#date            : 08/01/15
#usage           : python projet.py
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


#List files
def listFiles(directory):
  subdirs=listSubDirs(directory)
  files=[]
  for subd in subdirs:
    for file in os.listdir(subd):
      filename=subd+"/"+file
      files.append(filename)
  return files


def anonymize(directory):
	files=listFiles(directory)
	i=0
	lim=10
	print "Total:", len(files), u"fichiers à anonymiser"
	for file in files:
	    i+=1
	    if i==lim:
		  print i, "fichiers traités"
		  lim+=10
	    outputFileName="anonymized/"+file
	    outputFolder=outputFileName.split("/")
	    outputFolder="/".join(x for x in outputFolder[:-1])
	    if not os.path.exists(outputFolder):
    		os.makedirs(outputFolder)
	    outputFile=open(outputFileName, "w")
	    fileIN=open(file,'r')
	    contentFile = fileIN.read()
	    header_email,body_email = filter_email(contentFile)
	    #anonymize_header(header_email)
	    outputFile.write(anonymize_header(header_email))
	    outputFile.write(anonymize_body(body_email))
	    fileIN.close()
	    outputFile.close()
	
	#print anonymize_header(header_email)



if __name__ == '__main__':
	#anonymize('scott-s')
	contentFile = open("mail.txt",'r').read()
	header_email,body_email = filter_email(contentFile)
	print anonymize_header(header_email)
	
	
