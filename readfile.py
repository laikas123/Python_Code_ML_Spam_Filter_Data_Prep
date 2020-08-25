from os import listdir
from os.path import isfile, join
import sys

#these are hyper parameters
removePunctuation = False
removeSymbols = False
#if False count how many times a word shows up per word
#if True count words only once, whether they appear or don't
countSignalInstance = False
setAllWordsUpperCase = True
countInvalidLoneLetters = True
countUpperCaseWordsBeforeProcessing = True
countAllSymbolWordsLengthThreshold = [True, 2]
removeWordsLengthThreshold = [True, 10]



def removeAllSymbolsFromAString(word):
	word = word.replace("@", "")
	word = word.replace("#", "")
	word = word.replace("$", "")
	word = word.replace("%", "")
	word = word.replace("^", "")
	word = word.replace("&", "")
	word = word.replace("*", "")
	word = word.replace("~", "")
	word = word.replace("`", "")
	word = word.replace("<", "")
	word = word.replace(">", "")
	word = word.replace("=", "")
	word = word.replace("+", "")
	word = word.replace("|", "")
		

	return word

def removeAllPunctFromAString(word):
	word = word.replace(".", "")
	word = word.replace("?", "")
	word = word.replace(",", "")
	word = word.replace("'", "")
	word = word.replace("-", "")
	word = word.replace("—", "")
	word = word.replace("!", "")
	word = word.replace(":", "")
	word = word.replace(";", "")
	word = word.replace("[", "")
	word = word.replace("]", "")
	word = word.replace("{", "")
	word = word.replace("}", "")
	word = word.replace("(", "")
	word = word.replace(")", "")
	word = word.replace("/", "")
	word = word.replace("\\", "")
	word = word.replace('"', "")

	return word




#checker function for making sure invalid lone letter count only increments for actual letters
def isLetter(letter):
	letter = letter.upper()
	if(letter == "A" or letter == "B" or letter == "C" or letter == "D" or letter == "E" or letter == "F" or letter == "G" or letter == "H" or letter == "I" or letter == "J" or letter == "K" or letter == "L" or letter == "M" or letter == "N" or letter == "P" or letter == "Q" or letter == "R" or letter == "S" or letter == "T" or letter == "U"  or letter == "V"  or letter == "W"  or letter == "X"  or letter == "Y"  or letter == "Z" ):
		return True
	else:
		return False
#capital letter checker, same as above function but don't capitalize input prior to checking
def isCapitalLetter(letter):
	if(letter == "A" or letter == "B" or letter == "C" or letter == "D" or letter == "E" or letter == "F" or letter == "G" or letter == "H" or letter == "I" or letter == "J" or letter == "K" or letter == "L" or letter == "M" or letter == "N"  or letter == "O"  or letter == "P" or letter == "Q" or letter == "R" or letter == "S" or letter == "T" or letter == "U"  or letter == "V"  or letter == "W"  or letter == "X"  or letter == "Y"  or letter == "Z" ):
		return True
	else:
		return False

def isUpperCaseWord(word):
	#remove symbols and punctuation since only letters can be capital
	word = removeAllPunctFromAString(word)
	word = removeAllSymbolsFromAString(word)
	#if the word was just symbols and punctuation 
	#return False if the word was all symbols and punctuation
	if(len(word) == 0):
		return False
	sawACapitalLetter = False
	for letter in word:
		if(isCapitalLetter(letter) == False):
			return False

	return True

def isAllSymbolWord(word):
	for letter in word:
		if(letter == " " or letter == ""):
			return False
		if(letter != "?" and letter != "/" and letter != "\\" and letter != "|" and letter != "~" and letter != "`" and letter != "<" and letter != ">" and letter != "," and letter != "." and letter != ":" and letter != ";" and letter != "\"" and letter != "'" and letter != "[" and letter != "]" and letter != "{" and letter != "}" and letter != "(" and letter != ")" and letter != "-" and letter != "—" and letter != "=" and letter != "+" and letter != "!" and letter != "@" and letter != "#" and letter != "$" and letter != "%" and letter != "^" and letter != "&" and letter != "*" ):
			return False
	return True

mypath = "C:\\Users\\logan\\Downloads\\20021010_spam.tar\\spam\\"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


SpamWordCountPerEmailDict = {}

email_counter = 1


for filename in onlyfiles:
	

	dictionaryName = "Email" + str(email_counter)
	
	SpamWordCountPerEmailDict[dictionaryName] = {}

	# file1 = open(mypath+filename,"r", encoding='utf-8') 
	
	encodings = ['utf-8', 'windows-1250', 'windows-1252', 'ascii']
	for en in encodings:
		try:


			#TODO check that files never open twice
			file1 = open(mypath+filename, 'r', encoding=en)


			alllines = file1.read()
			alllinessplit = alllines.split()
			print("file opened succesfully ", filename)

			invalidLoneLetterCount = 0
			preProccessUpperCaseCount = 0
			allSymbolWordsCount = 0



			# print(len(alllinessplit))
			for word in alllinessplit:
				if(type(word) == str):

					if(word == " " or word == ""):
						continue

					

					#counts that need to be done pre proccessing
					if(countUpperCaseWordsBeforeProcessing == True):
						if(isUpperCaseWord(word)):
							countUpperCaseWordsBeforeProcessing = countUpperCaseWordsBeforeProcessing + 1
					if(countAllSymbolWordsLengthThreshold[0] == True):
						if(len(word) > countAllSymbolWordsLengthThreshold[1]):
							if(isAllSymbolWord(word)):
								allSymbolWordsCount = allSymbolWordsCount + 1
								print(word)


					#hyper parameter filters
					wordAfterHyperParameters = word
					if removePunctuation:
						wordAfterHyperParameters = removeAllPunctFromAString(wordAfterHyperParameters)
					if removeSymbols:
						wordAfterHyperParameters = removeAllSymbolsFromAString(wordAfterHyperParameters)	
					if setAllWordsUpperCase:
						wordAfterHyperParameters = wordAfterHyperParameters.upper()


					#count to do after processing
					if len(wordAfterHyperParameters) == 1 and isLetter(wordAfterHyperParameters):
			
						if(countInvalidLoneLetters):
							if(wordAfterHyperParameters != "i" and wordAfterHyperParameters != "I" and wordAfterHyperParameters != "a" and wordAfterHyperParameters != "A"):
								invalidLoneLetterCount = invalidLoneLetterCount + 1
			

					
					#count occurrences only for the hyperparameter being set
					if wordAfterHyperParameters in SpamWordCountPerEmailDict[dictionaryName] and countSignalInstance == False:
						SpamWordCountPerEmailDict[dictionaryName][wordAfterHyperParameters] = SpamWordCountPerEmailDict[dictionaryName][wordAfterHyperParameters] + 1
					else:
						SpamWordCountPerEmailDict[dictionaryName][wordAfterHyperParameters] = 1	
			email_counter = email_counter + 1
			if(countInvalidLoneLetters):
				SpamWordCountPerEmailDict[dictionaryName]["loneCnt"] = invalidLoneLetterCount
			if(countUpperCaseWordsBeforeProcessing):
				SpamWordCountPerEmailDict[dictionaryName]["upperCnt"] = preProccessUpperCaseCount
			if(countUpperCaseWordsBeforeProcessing):
				SpamWordCountPerEmailDict[dictionaryName]["symbolCnt"] = allSymbolWordsCount
			# if(email_counter == 247):
			# 	for key in SpamWordCountPerEmailDict[dictionaryName]:
			# 		print(SpamWordCountPerEmailDict[dictionaryName][key])
			# 	sys.exit()
			
			file1.close()		
		except UnicodeDecodeError:
			print('got unicode error with %s , trying different encoding' % en)
		else:
			print('opening the file with encoding:  %s ' % en)
			break 

mypath = "C:\\Users\\logan\\Downloads\\20021010_easy_ham\\easy_ham\\"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


HamWordCountPerEmailDict = {}

email_counter = 1

for filename in onlyfiles:
	

	dictionaryName = "Email" + str(email_counter)
	
	HamWordCountPerEmailDict[dictionaryName] = {}

	# file1 = open(mypath+filename,"r", encoding='utf-8') 
	
	encodings = ['utf-8', 'windows-1250', 'windows-1252', 'ascii']
	for en in encodings:
		try:
		
			file1 = open(mypath+filename, 'r', encoding=en)
			print("file opened succesfully ", filename)
			alllines = file1.read()
			alllinessplit = alllines.split()
		
			invalidLoneLetterCount = 0
			preProccessUpperCaseCount = 0
			allSymbolWordsCount = 0


			# print(len(alllinessplit))
			for word in alllinessplit:
				if(type(word) == str):
					

					if(word == " " or word == ""):
						continue

					#counts that need to be done pre proccessing
					if(countUpperCaseWordsBeforeProcessing == True):
						if(isUpperCaseWord(word)):
							countUpperCaseWordsBeforeProcessing = countUpperCaseWordsBeforeProcessing + 1
					if(countAllSymbolWordsLengthThreshold[0] == True):
						if(len(word) > countAllSymbolWordsLengthThreshold[1]):
							if(isAllSymbolWord(word)):
								allSymbolWordsCount = allSymbolWordsCount + 1


					#hyper parameter filters
					wordAfterHyperParameters = word
					if removePunctuation:
						wordAfterHyperParameters = removeAllPunctFromAString(wordAfterHyperParameters)
					if removeSymbols:
						wordAfterHyperParameters = removeAllSymbolsFromAString(wordAfterHyperParameters)	
					if setAllWordsUpperCase:
						wordAfterHyperParameters = wordAfterHyperParameters.upper()


					#count to do after processing
					if len(wordAfterHyperParameters) == 1 and isLetter(wordAfterHyperParameters):
						if(countInvalidLoneLetters):
							if(wordAfterHyperParameters != "i" and wordAfterHyperParameters != "I" and wordAfterHyperParameters != "a" and wordAfterHyperParameters != "A"):
								invalidLoneLetterCount = invalidLoneLetterCount + 1


					#count occurrences only for the hyperparameter being set
					if wordAfterHyperParameters in HamWordCountPerEmailDict[dictionaryName] and countSignalInstance == False:
						
						HamWordCountPerEmailDict[dictionaryName][wordAfterHyperParameters] = HamWordCountPerEmailDict[dictionaryName][wordAfterHyperParameters] + 1
					else:
						HamWordCountPerEmailDict[dictionaryName][wordAfterHyperParameters] = 1	
			email_counter = email_counter + 1
			if(countInvalidLoneLetters):
				HamWordCountPerEmailDict[dictionaryName]["loneCnt"] = invalidLoneLetterCount
			if(countUpperCaseWordsBeforeProcessing):
				HamWordCountPerEmailDict[dictionaryName]["upperCnt"] = preProccessUpperCaseCount
			if(countUpperCaseWordsBeforeProcessing):
				HamWordCountPerEmailDict[dictionaryName]["symbolCnt"] = allSymbolWordsCount
			
			file1.close()		
		except UnicodeDecodeError:
			print('got unicode error with %s , trying different encoding' % en)
		else:
			print('opening the file with encoding:  %s ' % en)
			break 



print("DICTLENGTHS", len(SpamWordCountPerEmailDict), len(HamWordCountPerEmailDict))

dictionary_path = "C:\\Users\\logan\\Documents\\TensorFlow\\dictionary.txt"

dictionary = open(dictionary_path,"r", encoding='utf-8') 

all_dictionary_words = []

alllines = dictionary.read()
alllinessplit = alllines.split()

for word in alllinessplit:
	#upper case for the purpose of comparison later
	all_dictionary_words.append(word.upper())

print(len(all_dictionary_words), "len dict")

dictionary.close()


spam_dictionary_path = "C:\\Users\\logan\\Documents\\TensorFlow\\spamdictionary.txt"

spam_dictionary = open(spam_dictionary_path, "r", encoding='utf-8') 

all_spam_dictionary_words = []

alllinesspam = spam_dictionary.read()
alllinessplitspam = alllinesspam.split()

for word in alllinessplitspam:
	#upper case for the purpose of comparison later
	all_spam_dictionary_words.append(word.upper())

print(len(all_spam_dictionary_words), "len spam dict")

spam_dictionary.close

# for word in all_spam_dictionary_words:
	# print(word)



# print(len(SpamWordCountPerEmailDict))
# print(len(HamWordCountPerEmailDict))


allpossiblewords = []


print("spam counts")
for dictn in SpamWordCountPerEmailDict:
	if(SpamWordCountPerEmailDict[dictn]["symbolCnt"] >= 10):
		print(SpamWordCountPerEmailDict[dictn])
		for key in SpamWordCountPerEmailDict[dictn]:
			if(isAllSymbolWord(key)):
				print(key, "ocurrences", SpamWordCountPerEmailDict[dictn][key])
		sys.exit()	
		
		
	print(dictn, "lone ", SpamWordCountPerEmailDict[dictn]["loneCnt"], " uppers ", SpamWordCountPerEmailDict[dictn]["upperCnt"], " symbols ", SpamWordCountPerEmailDict[dictn]["symbolCnt"],)


for email in SpamWordCountPerEmailDict:

	for word in SpamWordCountPerEmailDict[email]:
		if(allpossiblewords.count(word) == 0):
			#if a threshold for how long a word is to be counted is specified check the word is valid length
			if(removeWordsLengthThreshold[0] == True):
				if(len(word) > removeWordsLengthThreshold[1]):
					allpossiblewords.append(word)
			else:
				allpossiblewords.append(word)

for email in HamWordCountPerEmailDict:

	for word in HamWordCountPerEmailDict[email]:
		if(allpossiblewords.count(word) == 0):
			#if a threshold for how long a word is to be counted is specified check the word is valid length
			if(removeWordsLengthThreshold[0] == True):
				if(len(word) > removeWordsLengthThreshold[1]):
					allpossiblewords.append(word)
			else:
				allpossiblewords.append(word)


print(len(allpossiblewords), "total words")

















#THIS CODE BELOW IS GOOD



count = 0
for email in SpamWordCountPerEmailDict:
	dictionaryWords = 0
	spamWords = 0
	totalWords = 0
	for word in SpamWordCountPerEmailDict[email]:
		totalWords = totalWords + 1
		if(all_dictionary_words.count(word.upper()) > 0):
			dictionaryWords = dictionaryWords + 1
		if(all_spam_dictionary_words.count(word.upper()) > 0):
			spamWords = spamWords + 1 	
			# print(word)

	# print("spam email: ", email, "has %", 100*(dictionaryWords/totalWords), "dictionary words and ", "has %", 100*(spamWords/totalWords), "spam words")
	print("spam email: ", email, "has ham% - spam% = ", (100*(dictionaryWords/totalWords)) - (100*(spamWords/totalWords)))
	count = count + 1 
	if count == 30:
		break

count = 0
for email in HamWordCountPerEmailDict:
	dictionaryWords = 0
	spamWords = 0
	totalWords = 0
	for word in HamWordCountPerEmailDict[email]:
		totalWords = totalWords + 1
		if(all_dictionary_words.count(word.upper()) > 0):
			dictionaryWords = dictionaryWords + 1
			# print(word)
		if(all_spam_dictionary_words.count(word.upper()) > 0):
			spamWords = spamWords + 1

	# print("ham email: ", email, "has %", 100*(dictionaryWords/totalWords), "dictionary words and ", "has %", 100*(spamWords/totalWords), "spam words")
	print("ham email: ", email, "has ham% - spam% = ", (100*(dictionaryWords/totalWords)) - (100*(spamWords/totalWords)))
	count = count + 1
	if count == 30:
		break


# print(len(allpossiblewords))












