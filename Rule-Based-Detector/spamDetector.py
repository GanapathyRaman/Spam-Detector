"""@Author: Ganapathy Raman Madanagopal
   File description: Python program to dectect a email parsed as a text file
                     is a spam or not """

from __future__ import division
from rules import *
import os
import sys
import re

# Global declarations
spamCount = 0
nonSpamCount = 0


def printSummary():
	"Function prints the summary of the results obtained"

	print '\nSummary'
	print '--------'
	print 'Number of emails classified as spam     : ', spamCount 
	print 'Number of emails classified as non-spam : ', nonSpamCount, '\n'


def increment_Spam_Count():
	"Function increments the counter spam_As_Spam by one"
	global spamCount
	spamCount += 1


def increment_NonSpam_Count():
	"Function increments the counter spam_As_NonSpam by one"
	global nonSpamCount
	nonSpamCount += 1


def incrementCounters(spamFlag):
	"Function increments the counters based on the classification"
	if (spamFlag > 0):
		increment_Spam_Count()
        else:
		increment_NonSpam_Count()


def isSpamOrNot(str):
	"""Function takes the entire email as string (str) 
	 and returns values spam or not 
	 by comparing against the blackisted words and phrases
	 Return values 0 --> Non-Spam
                       1 --> Spam"""
	if any(word in str.lower() for word in blackPhrases):
		return True

	elif any(regex.search(str.lower()) for regex in blackRegExps):
		return True

	else:
		return False

	
def readAllFiles(rootPath):
	"Function reads all the file from the specified directory recursively"
	count = 0
	spamFlag = 0
	for root, subFolders, files in os.walk(rootPath):
		for file in files:
			filePath = os.path.join(root,file)
			fo = open(filePath, 'r')
			str = fo.read()
			spamFlag = isSpamOrNot(str)
			incrementCounters(spamFlag)
			fo.close()


if __name__ == '__main__':
	"Program Execution start from here"

	if len(sys.argv) > 1: #Check whether the directory path is passes as an input
		if os.path.isdir(str(sys.argv[1])): #Check the directory specified is valid
                	readAllFiles(str(sys.argv[1]))
			printSummary()
		else:
			print '\n[Error]: The specified directory is not valid'
	else:
		print '\nUsage: python spam-filter.py <path-to-folder-containing-emails>'

