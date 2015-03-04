"""@Author: Ganapathy Raman Madanagopal
   File description: This file is used to detect whether the give file is 
		     a spam or not by calculating the probabilty from the
		     existing bag of words. Here we use Navie Bayers method
		     for calculating the probabilty"""

from __future__ import division
from pprint import pprint
from decimal import Decimal
import os
import sys
import re
import pickle
import fnmatch
import math
import time

#Gloabal Declarations

# For testing purpose
spamCount	 = 0
hamCount	 = 0
spamThreshold	 = 0.7 #Setting the threshold to 0.7
hamThreshold	 = (1 - spamThreshold)
threshold	 = math.log(spamThreshold/hamThreshold)

#From trainer program
spamList 	= {}
hamList 	= {}
spamFilesCount 	= 0
hamFilesCount  	= 0
spamWordsCount 	= 0
hamWordsCount 	= 0
spamSum 	= 0
hamSum 		= 0


def printSummary():
	"Function prints the summary of the results obtained"
	global spamCount, hamCount
	print '\nSummary'
	print '-------'
	print 'Number of emails classified as spam    : ', spamCount
	print 'Number of emails classified as non-spam: ', hamCount, '\n'

def countRatios(file, spamGivenFile, hamGivenFile):
	"Function calculates the True postive and False postive ratio"
	global spamCount, hamCount
	global threshold
	if ((spamGivenFile - hamGivenFile) > threshold):
		spamCount += 1
	else:
		hamCount += 1
	
def readFromBagOfWords():
	"Function reads the the bag of words from the file bagOfWords.txt"
	global spamList, hamList
	global spamFilesCount, hamFilesCount
	global spamWordsCount, hamWordsCount
	global spamSum, hamSum
	try:
		fileName = 'bagOfWords.txt'	#File containing spam/ham list
		pwd = os.path.dirname(sys.argv[0])
		fullPath = os.path.join(pwd,fileName) #Join the pwd with the filename
		fo = open(fullPath, 'r')
		if os.stat(fullPath).st_size > 0:
			spamList 	= pickle.load(fo)	#Load the spam list
			hamList 	= pickle.load(fo)	#Load the ham list
			spamFilesCount 	= pickle.load(fo)	#Load the spam file count
			hamFilesCount 	= pickle.load(fo)	#Load the ham file count
			spamWordsCount 	= pickle.load(fo)	#Load the spam words count
			hamWordsCount 	= pickle.load(fo)	#Load the hamWords count
			spamSum 	= pickle.load(fo)	#Load the spam sum
			hamSum 		= pickle.load(fo)	#Load the ham sum
		fo.close()
		return True
	except IOError:
		return False

def  calculateProbability(spamProbs, hamProbs):
	"Function caluclates the probabilty whether the emai is spam or not"
	global spamFilesCount, hamFilesCount
	trainerTotalMails = spamFilesCount + hamFilesCount

	#Probability that a given file being spam
	spamGivenFile = spamProbs + math.log10(spamFilesCount/trainerTotalMails)
	
	#Probability that a given file being ham
	hamGivenFile = hamProbs + math.log10(hamFilesCount/trainerTotalMails)

	return spamGivenFile, hamGivenFile


def checkInBagOfWords(wordsArray, file):
	"Functions checks whether the words in the email are in bag of words"
	global spamList, hamList
	global spamFilesCount, hamFilesCount
	spamProbs = 1
	hamProbs = 1
	logSpamProb = 0
	logHamProb = 0

	for word in wordsArray:		#For every word in the mail

		#Check if the word is in the spamList in the bag of words
		if word in spamList:
			logSpamProb = logSpamProb + math.log(spamList[word] + 1) \
				      - math.log(spamSum + spamWordsCount)
		else:
			logSpamProb = logSpamProb - math.log(spamSum + spamWordsCount)

		#Check if the word is in the spamList (in the bag of words)
		if word in hamList:
			logHamProb = logHamProb + math.log(hamList[word] + 1) \
				     - math.log(hamSum + hamWordsCount)
		else:
			logHamProb = logHamProb - math.log(hamSum + hamWordsCount)

	#Calculate the probabilty  of a file being spam
	spamGivenFile, hamGivenFile = calculateProbability(logSpamProb, logHamProb)

	#Count the ratios fo spamFile and hamFile
	countRatios(file, spamGivenFile, hamGivenFile)


def readAllFiles(rootPath):
        "Function reads all the file from the specified directory recursively"
	global bagOfWords

	#Read all the files in the directory
	for file in os.listdir(rootPath):
		filePath = os.path.join(rootPath,file)
		#Check for the file with the extension '.txt'
    		if fnmatch.fnmatch(filePath, '*.txt'):
                        try:
                                fo = open(filePath, 'r')
                                line = fo.read()
                                wordsArray = line.split()
				#Pass the entire words in the mail
                                checkInBagOfWords(wordsArray, file)
                                fo.close()
                        except IOError:
                                print '\n[Error]: File not found'

if __name__ == '__main__':
        "Program Execution start from here"
	#Check whether the directory path is passed as an argument or not
        if len(sys.argv) > 1: 
		#Check the directory specified is valid
                if os.path.isdir(str(sys.argv[1])): 
		#Check the whether the file 'bagOfWords.txt' exist or not
                        checkFlag = readFromBagOfWords()
			if checkFlag:
				#Read from emails from the specified folder
				readAllFiles(str(sys.argv[1]))
				#Print the final summary
				printSummary()
			else:
				print '\n[Error]: File \'bagOfWords.txt\' not found'
                else:
                        print '\n[Error]: The specified directory is not valid'
        else:
                print '\nUsage: python spam-filter.py <path-to-folder-containing-emails>'
