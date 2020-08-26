import os
from os import listdir
from os.path import isfile, join
import re
import sys


#SPAM PATH HAM PATH NORM DICT PATH SPAM DICT PATH GLOBAL VARIABLES 
SPAM_PATH = os.path.join("HamandSpam", "Spam", "spam") 

HAM_PATH = os.path.join("HamandSpam", "Ham", "easy_ham") 

NORMAL_DICTIONARY_PATH = os.path.join("Dictionaries", "dictionary.txt") 

SPAM_DICTIONARY_PATH = os.path.join("Dictionaries", "spamdictionary.txt") 

#HYPERPARAMETERS 
REMOVE_PUNCTUATION = False
REMOVE_SYMBOLS = False
# if False count how many times a word shows up per word
# if True count words only once, whether they appear or don't
COUNT_SINGLE_INSTANCE = False
SET_ALL_WORDS_UPPER_CASE = True
COUNT_INVALID_LONE_LETTERS = True
CHECK_IF_EMAIL_CONTAINS_MARKUP = True
COUNT_UPPER_CASE_WORDS_BEFORE_PROCESSING = True
COUNT_ALL_SYMBOL_WORDS_LENGTH_THRESHOLD = [True, 2]
REMOVE_WORDS_LENGTH_THRESHOLD = [True, 4]
CHECK_MARKUP_TEXT_PRESENCE = True

#HELPER FUNCTIONS 
def removeAllSymbolsFromAString(word):
    for letter in word:
        if(isSymbol(letter)):
            word = word.replace(letter, "")

    return word


def removeAllPunctFromAString(word):
    for letter in word:
        if(isPunctuation(letter)):
            word = word.replace(letter, "")

    return word
    

def isPunctuation(letter):
    punctuation_text = re.search(r"([/./?\,\'\-\—\!\:\;\[\]\(\)\/\\\"])", letter)
    if(punctuation_text is None):
        return False
    else:
        return True
    

# checker function for making sure invalid lone letter count only
# increments for actual letters
def isLetter(letter):
    letter_text = re.search(r"([A-Za-z])", letter)
    if(letter_text is None):
        return False
    else:
        return True

# capital letter checker, same as above function but don't capitalize
# input prior to checking
def isCapitalLetter(letter):
    letter_text = re.search(r"([A-Z])", letter)
    if(letter_text is None):
        return False
    else:
        return True


def isUpperCaseWord(word):
    # remove symbols and punctuation since only letters can be capital
    word = removeAllPunctFromAString(word)
    word = removeAllSymbolsFromAString(word)
    # if the word was just symbols and punctuation
    # return False if the word was all symbols and punctuation
    if(len(word) == 0):
        return False
    sawACapitalLetter = False
    for letter in word:
        if(isCapitalLetter(letter) == False):
            return False

    return True


def isSymbol(letter):
    symbol_text = re.search(r"([\?\/\\\|\~\`\<\>\,\.\:\;\\\'\{\}\-\—\=\+\!\@\#\\\$\%\^\&\*])", letter)
    if(symbol_text is None):
        return False
    else:
        return True
def isAllSymbolWord(word):
    for letter in word:
        if(letter == " " or letter == ""):
            return False
        if(isSymbol(letter) != True):
            return False
    return True
def isMarkupWord(word):
    markup_text = re.search(r"\<([A-Za-z0-9_]+)\>", word)
    if(markup_text is None):
        return False
    else:
        return True



def GetDataApplyHyperparameters(spam_path = SPAM_PATH, ham_path = HAM_PATH, norm_dict_path = NORMAL_DICTIONARY_PATH,
                               spam_dict_path = SPAM_DICTIONARY_PATH, remove_punctuation = REMOVE_PUNCTUATION,
                        remove_symbols = REMOVE_SYMBOLS, count_single_instance = COUNT_SINGLE_INSTANCE,
                        set_all_words_upper_case = SET_ALL_WORDS_UPPER_CASE, 
                         count_invalid_lone_letters = COUNT_INVALID_LONE_LETTERS, 
                        count_upper_case_words_before_processing = COUNT_UPPER_CASE_WORDS_BEFORE_PROCESSING,
                        count_all_symbol_words_length_threshold = COUNT_ALL_SYMBOL_WORDS_LENGTH_THRESHOLD,
                        remove_words_length_threshold = REMOVE_WORDS_LENGTH_THRESHOLD, 
                                check_markup_text_presence = CHECK_MARKUP_TEXT_PRESENCE):
    
    
    onlyfiles = [f for f in listdir(spam_path) if isfile(os.path.join(spam_path, f))]

    spam_word_count_per_email_data = {}

    email_counter = 1


    for filename in onlyfiles:

        dictionaryName = "Email" + str(email_counter)

        spam_word_count_per_email_data[dictionaryName] = {}

        encodings = ['utf-8', 'windows-1250', 'windows-1252', 'ascii']
        for en in encodings:
            try:

                file1 = open(os.path.join(spam_path, filename), 'r', encoding=en)

                alllines = file1.read()
                alllinessplit = alllines.split()

                invalidLoneLetterCount = 0
                preProccessUpperCaseCount = 0
                allSymbolWordsCount = 0

                sawMarkupWord = False

                for word in alllinessplit:
                    if(isinstance(word, str)):

                        if(word == " " or word == ""):
                            continue

                        #markup check should be done before all processing
                        if(check_markup_text_presence):
                            if(isMarkupWord(word)):
                                sawMarkupWord = True
                                
                            
                        # counts that need to be done pre proccessing
                        if(count_upper_case_words_before_processing):
                            if(isUpperCaseWord(word)):
                                preProccessUpperCaseCount = preProccessUpperCaseCount + 1
                        if(count_all_symbol_words_length_threshold[0]):
                            if(len(word) > count_all_symbol_words_length_threshold[1]):
                                if(isAllSymbolWord(word)):
                                    allSymbolWordsCount = allSymbolWordsCount + 1
                                    

                        # hyper parameter filters
                        wordAfterHyperParameters = word
                        if remove_punctuation:
                            wordAfterHyperParameters = removeAllPunctFromAString(
                                wordAfterHyperParameters)
                        if remove_symbols:
                            wordAfterHyperParameters = removeAllSymbolsFromAString(
                                wordAfterHyperParameters)
                        if set_all_words_upper_case:
                            wordAfterHyperParameters = wordAfterHyperParameters.upper()

                        # count to do after processing
                        if len(wordAfterHyperParameters) == 1 and isLetter(
                                wordAfterHyperParameters):

                            if(count_invalid_lone_letters):
                                if(wordAfterHyperParameters != "i" and wordAfterHyperParameters != "I" and wordAfterHyperParameters != "a" and wordAfterHyperParameters != "A"):
                                    invalidLoneLetterCount = invalidLoneLetterCount + 1

                        # count occurrences only for the hyperparameter being set
                        if wordAfterHyperParameters in spam_word_count_per_email_data[
                                dictionaryName] and count_single_instance == False:
                            spam_word_count_per_email_data[dictionaryName][wordAfterHyperParameters] = spam_word_count_per_email_data[
                                dictionaryName][wordAfterHyperParameters] + 1
                        else:
                            spam_word_count_per_email_data[dictionaryName][wordAfterHyperParameters] = 1
                email_counter = email_counter + 1
                #if hyperparameters were enabled add their respective values to the container
                if(count_invalid_lone_letters):
                    spam_word_count_per_email_data[dictionaryName]["loneCnt"] = invalidLoneLetterCount
                if(count_upper_case_words_before_processing):
                    spam_word_count_per_email_data[dictionaryName]["upperCnt"] = preProccessUpperCaseCount
                if(count_all_symbol_words_length_threshold):
                    spam_word_count_per_email_data[dictionaryName]["symbolCnt"] = allSymbolWordsCount
                if(check_markup_text_presence):
                    if(sawMarkupWord):
                        spam_word_count_per_email_data[dictionaryName]["markupPrsnt"] = 1
                    else:
                        spam_word_count_per_email_data[dictionaryName]["markupPrsnt"] = 0
                file1.close()
            except UnicodeDecodeError:
                print('got unicode error with %s , trying different encoding' % en)
            else:
                break

    onlyfiles = [f for f in listdir(ham_path) if isfile(os.path.join(ham_path, f))]


    ham_word_count_per_email_data = {}

    email_counter = 1

    for filename in onlyfiles:

        dictionaryName = "Email" + str(email_counter)

        ham_word_count_per_email_data[dictionaryName] = {}

        encodings = ['utf-8', 'windows-1250', 'windows-1252', 'ascii']
        for en in encodings:
            try:

                file1 = open(os.path.join(ham_path, filename), 'r', encoding=en)

                alllines = file1.read()
                alllinessplit = alllines.split()

                invalidLoneLetterCount = 0
                preProccessUpperCaseCount = 0
                allSymbolWordsCount = 0
                
                sawMarkupWord = False
                
                for word in alllinessplit:
                    if(isinstance(word, str)):

                        if(word == " " or word == ""):
                            continue
                            
                        #markup check should be done before all processing
                        if(check_markup_text_presence):
                            if(isMarkupWord(word)):
                                sawMarkupWord = True
                                    
                        # counts that need to be done pre proccessing
                        if(count_upper_case_words_before_processing):
                            if(isUpperCaseWord(word)):
                                preProccessUpperCaseCount = preProccessUpperCaseCount + 1
                        if(count_all_symbol_words_length_threshold[0]):
                            if(len(word) > count_all_symbol_words_length_threshold[1]):
                                if(isAllSymbolWord(word)):
                                    allSymbolWordsCount = allSymbolWordsCount + 1
                                    

                        # hyper parameter filters
                        wordAfterHyperParameters = word
                        if remove_punctuation:
                            wordAfterHyperParameters = removeAllPunctFromAString(
                                wordAfterHyperParameters)
                        if remove_symbols:
                            wordAfterHyperParameters = removeAllSymbolsFromAString(
                                wordAfterHyperParameters)
                        if set_all_words_upper_case:
                            wordAfterHyperParameters = wordAfterHyperParameters.upper()

                        # count to do after processing
                        if len(wordAfterHyperParameters) == 1 and isLetter(
                                wordAfterHyperParameters):

                            if(count_invalid_lone_letters):
                                if(wordAfterHyperParameters != "i" and wordAfterHyperParameters != "I" and wordAfterHyperParameters != "a" and wordAfterHyperParameters != "A"):
                                    invalidLoneLetterCount = invalidLoneLetterCount + 1

                        # count occurrences only for the hyperparameter being set
                        if wordAfterHyperParameters in ham_word_count_per_email_data[
                                dictionaryName] and count_single_instance == False:

                            ham_word_count_per_email_data[dictionaryName][wordAfterHyperParameters] = ham_word_count_per_email_data[
                                dictionaryName][wordAfterHyperParameters] + 1
                        else:
                            ham_word_count_per_email_data[dictionaryName][wordAfterHyperParameters] = 1
                email_counter = email_counter + 1
                if(count_invalid_lone_letters):
                    ham_word_count_per_email_data[dictionaryName]["loneCnt"] = invalidLoneLetterCount
                if(count_upper_case_words_before_processing):
                    ham_word_count_per_email_data[dictionaryName]["upperCnt"] = preProccessUpperCaseCount
                if(count_all_symbol_words_length_threshold[0]):
                    ham_word_count_per_email_data[dictionaryName]["symbolCnt"] = allSymbolWordsCount
                if(check_markup_text_presence):
                    if(sawMarkupWord):
                        ham_word_count_per_email_data[dictionaryName]["markupPrsnt"] = 1
                    else:
                        ham_word_count_per_email_data[dictionaryName]["markupPrsnt"] = 0
                file1.close()
            except UnicodeDecodeError:
                print('got unicode error with %s , trying different encoding' % en)
            else:
                break


    
    
    print("DONE READING ALL EMAIL FILES",  "Email counts Spam: ",
        len(spam_word_count_per_email_data), " Ham: ",
        len(ham_word_count_per_email_data))


    dictionary = open(norm_dict_path, "r", encoding='utf-8')

    all_norm_dictionary_words = []

    alllines = dictionary.read()
    alllinessplit = alllines.split()

    for word in alllinessplit:
        # upper case for the purpose of comparison later
        all_norm_dictionary_words.append(word.upper())

    dictionary.close()


    

    spam_dictionary = open(spam_dict_path, "r", encoding='utf-8')

    all_spam_dictionary_words = []

    alllinesspam = spam_dictionary.read()
    alllinessplitspam = alllinesspam.split()

    for word in alllinessplitspam:
        # upper case for the purpose of comparison later
        all_spam_dictionary_words.append(word.upper())

    spam_dictionary.close()

    print("DONE READING ALL DICTIONARY FILES", "Length Normal Dict: ", len(all_norm_dictionary_words),
         " Length Spam Dict: ", len(all_spam_dictionary_words))

    return spam_word_count_per_email_data, ham_word_count_per_email_data, all_norm_dictionary_words, all_spam_dictionary_words


spam_word_count_container, ham_word_count_container, norm_dict, spam_dict = GetDataApplyHyperparameters()







#Cell 2





allpossiblewords = []


for email in spam_word_count_container:
    if(spam_word_count_container[email]["markupPrsnt"] == 1):
        print(spam_word_count_container[email])
#         sys.exit()
    for word in spam_word_count_container[email]:
        if(allpossiblewords.count(word) == 0):
            # if a threshold for how long a word is to be counted is specified
            # check the word is valid length
            if(REMOVE_WORDS_LENGTH_THRESHOLD[0]):
                if(len(word) > REMOVE_WORDS_LENGTH_THRESHOLD[1]):
                    allpossiblewords.append(word)
                   # print(len(allpossiblewords), "spam addition")
                
sys.exit()
for email in ham_word_count_container:

    for word in ham_word_count_container[email]:
        if(allpossiblewords.count(word) == 0):
            # if a threshold for how long a word is to be counted is specified
            # check the word is valid length
            if(REMOVE_WORDS_LENGTH_THRESHOLD[0]):
                if(len(word) > REMOVE_WORDS_LENGTH_THRESHOLD[1]):
                    allpossiblewords.append(word)
                    print(len(allpossiblewords), "ham addition")
              


print(len(allpossiblewords), "total words")


