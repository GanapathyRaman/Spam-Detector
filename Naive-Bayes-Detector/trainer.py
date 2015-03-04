"""@Author: Ganapathy Raman Madanagopal
   File description: This python program used act as a trainer in learning 
		     the new spam words and ham words.
		     When the new files are given for the training, 
		     the program loads the already existing spam 
	             and Ham words, and adds the new words to the
		     corresponding spam and ham list repsectively
		     along with the number of occurences"""


from pprint import pprint
import os
import sys
import re
import pickle
import fnmatch

#Global Declarations
spamList       = {}
hamList        = {}
spamFilesCount = 0
hamFilesCount  = 0
spamWordsCount = 0
hamWordsCount  = 0
spamSum        = 0
hamSum         = 0


def readFromBagOfWords():
	"""Function reads the existing variables from the bag of words
	 if they exist"""
        global spamList, hamList
        global spamFilesCount, hamFilesCount
        global spamWordsCount, hamWordsCount
        global spamSum, hamSum
        try:
                fileName = 'bagOfWords.txt' #File containing spam/ham list
                pwd = os.path.dirname(sys.argv[0])
                fullPath = os.path.join(pwd,fileName)
                if os.stat(fullPath).st_size > 0:
                	fo = open(fullPath, 'r')
                        spamList 	= pickle.load(fo) #Load the spam list
                        hamList 	= pickle.load(fo) #Load the ham list
                        spamFilesCount 	= pickle.load(fo) #Load the spam files count
                        hamFilesCount 	= pickle.load(fo) #Load the ham files count
                        spamWordsCount 	= pickle.load(fo) #Load the spam words count
                        hamWordsCount 	= pickle.load(fo) #Load the ham words count
                        spamSum 	= pickle.load(fo) #Load the spam sum 
                        hamSum 		= pickle.load(fo) #Load the ham sum
                	fo.close()
                return True
        except IOError:
                return False	
		

def updateBagOfWords(wordsArray, file):
	"""Function to store the new words and its
	occurence count in the file bagOfWords.txt"""
	global spamList, hamList
	global spamWordsCount, hamWordsCount
	global spamSum, hamSum

	for word in wordsArray:
		if 'spam' in file:
			spamSum += 1
			if word in spamList:
				spamList[word] += 1
			else:
				spamList.update({word:1})
				spamWordsCount += 1
		elif 'ham' in file:
			hamSum += 1
                        if word in hamList:
                                hamList[word] += 1
                        else:
                                hamList.update({word:1})
				hamWordsCount += 1

def writeToBagOfWords():
	"Function will store the bagOfWords in to a file"
	os.system('touch bagOfWords.txt')
	try:
		output = open('bagOfWords.txt', 'w')
		pickle.dump(spamList, output)
		pickle.dump(hamList, output)
		pickle.dump(spamFilesCount, output)
		pickle.dump(hamFilesCount, output)
		pickle.dump(spamWordsCount, output)
		pickle.dump(hamWordsCount, output)
		pickle.dump(spamSum, output)
		pickle.dump(hamSum, output)
		output.close()	
		print 'Spam Files Count : ', spamFilesCount
		print 'Ham Files Count  : ', hamFilesCount
		print 'Spam Words Count : ', spamWordsCount
		print 'Ham Words Count  : ', hamWordsCount
		print 'Spam Sum         : ', spamSum
		print 'Ham Sum          : ', hamSum
	except IOError:
		print '\n[Error]: Unable to open the \'bagOfWords.txt\' \
                       for writing'
		
def readAllFiles(rootPath):
        "Function reads all the file from the specified directory recursively"
	global spamFilesCount, hamFilesCount
	for file in os.listdir(rootPath):
		filePath = os.path.join(rootPath,file)
    		if fnmatch.fnmatch(filePath, '*.txt'):
			if 'spam' in file:
				spamFilesCount += 1
			elif 'ham' in file:
				hamFilesCount += 1
			try:
                		fo = open(filePath, 'r')
                		line = fo.read()
				wordsArray = line.split()
				#Add the words to the bag of words
				updateBagOfWords(wordsArray, file)
				fo.close()
			except IOError:
				print '\n[Error]: File not found'

if __name__ == '__main__':
        "Program Execution start from here"

        if len(sys.argv) > 1: 
	#Check whether the directory path is passed as an argument or not
                if os.path.isdir(str(sys.argv[1])): 
		#Check the directory specifie is valid
			checkFlag = readFromBagOfWords()
			if checkFlag:
				readAllFiles(str(sys.argv[1]))
				writeToBagOfWords()
			else:
				 print '\n[Error]: File \'bagOfWords.txt\' not found'
                else:
                        print '\n[Error]: The specified directory is not valid'
        else:
                print '\nUsage: python spam-filter.py <path-to-folder-containing-emails>'


