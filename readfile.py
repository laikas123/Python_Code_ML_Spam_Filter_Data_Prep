#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from os import listdir
from os.path import isfile, join
import re
import sys


#SPAM PATH HAM PATH 
SPAM_PATH = os.path.join("HamandSpam", "Spam", "spam") 

HAM_PATH = os.path.join("HamandSpam", "Ham", "easy_ham") 



#HYPERPARAMETERS 
REMOVE_PUNCTUATION = True
REMOVE_SYMBOLS = True
# if False count how many times a word shows up per word
# if True count words only once, whether they appear or don't
COUNT_SINGLE_INSTANCE = False
SET_ALL_WORDS_UPPER_CASE = True
COUNT_INVALID_LONE_LETTERS = True
CHECK_IF_EMAIL_CONTAINS_MARKUP = True
COUNT_UPPER_CASE_WORDS_BEFORE_PROCESSING = True
COUNT_ALL_SYMBOL_WORDS_LENGTH_THRESHOLD = [True, 2]
#some emails have rather long words, especially spam
#this leads to a large dataset when looking at unique words
#setting shortest and longest word limits help reduce dataset size
REMOVE_WORDS_LENGTH_THRESHOLD = [True, 4, 8]
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
#keys used in the containers for data that shouldn't be overwritten if an email contains them
def isSpecialWord(word):
    if(word == "upperCnt" or word == "symbolCnt" or word == "loneCnt" or word == "markupPrsnt" or word == "IsSpam"):
        print("Special Word was present")
        sys.Exit()
        return True
    else:
        return False


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

                        if(isSpecialWord(word)):
                            continue
                        
                        if(word == " " or word == ""):
                            continue

                        #markup check should be done before all processing
                        if(check_markup_text_presence):
                            if(isMarkupWord(word)):
                                sawMarkupWord = True
                                continue
                                
                            
                        # counts that need to be done pre proccessing
                        if(count_upper_case_words_before_processing):
                            if(isUpperCaseWord(word)):
                                preProccessUpperCaseCount = preProccessUpperCaseCount + 1
                        if(count_all_symbol_words_length_threshold[0]):
                            if(len(word) >= count_all_symbol_words_length_threshold[1]):
                                if(isAllSymbolWord(word)):
                                    allSymbolWordsCount = allSymbolWordsCount + 1
                                    continue
                                    

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
                        elif (len(wordAfterHyperParameters) > remove_words_length_threshold[1] and 
                             len(wordAfterHyperParameters) < remove_words_length_threshold[2]):
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
                        
                        if(isSpecialWord(word)):
                            continue

                        if(word == " " or word == ""):
                            continue
                            
                        #markup check should be done before all processing
                        if(check_markup_text_presence):
                            if(isMarkupWord(word)):
                                sawMarkupWord = True
                                continue
                                    
                        # counts that need to be done pre proccessing
                        if(count_upper_case_words_before_processing):
                            if(isUpperCaseWord(word)):
                                preProccessUpperCaseCount = preProccessUpperCaseCount + 1
                        if(count_all_symbol_words_length_threshold[0]):
                            if(len(word) > count_all_symbol_words_length_threshold[1]):
                                if(isAllSymbolWord(word)):
                                    allSymbolWordsCount = allSymbolWordsCount + 1
                                    continue
                                    

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
                        elif (len(wordAfterHyperParameters) > remove_words_length_threshold[1] and 
                             len(wordAfterHyperParameters) < remove_words_length_threshold[2]):
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

    return spam_word_count_per_email_data, ham_word_count_per_email_data


spam_word_count_container, ham_word_count_container = GetDataApplyHyperparameters()



# In[83]:




# allpossiblewords = []

totalWordCount = 0

for email in spam_word_count_container:
    for word in spam_word_count_container[email]:
        if(isMarkupWord(word) or isAllSymbolWord(word) or isPunctuation(word)):
            print(word)
        totalWordCount = totalWordCount + 1

for email in ham_word_count_container:
    for word in ham_word_count_container[email]:
        if(isMarkupWord(word) or isAllSymbolWord(word) or isPunctuation(word)):
            print(word)
        totalWordCount = totalWordCount + 1




# In[84]:


print(totalWordCount)


# In[85]:


import random
import pandas as pd
import numpy as np
#to generate random indices when picking words from an email
def randomListOfXValuesInRange(high_lim, number_items_to_return):
    return_vals = []

    if(number_items_to_return <= 0):
        return return_vals
    
    while len(return_vals) < number_items_to_return:
        random_num = random.randrange(high_lim)
        if(return_vals.count(random_num) == 0):
            return_vals.append(random_num)
    return return_vals




def SamplePortionFromEveryEmail(container_spam, container_ham, portion_size):
    
    possible_words_for_sample = []
    
    for email in container_spam:
        total_words_in_email = len(container_spam[email])
        
        random_indices = randomListOfXValuesInRange(total_words_in_email, int(round(portion_size*total_words_in_email)))
        current_index = 0
        for word in container_spam[email]:
            if(random_indices.count(current_index) > 0 ):
                possible_words_for_sample.append(word)
            current_index = current_index + 1
            
    for email in container_ham:
        total_words_in_email = len(container_ham[email])
        
        random_indices = randomListOfXValuesInRange(total_words_in_email, int(round(portion_size*total_words_in_email)))
        current_index = 0
        for word in container_ham[email]:
            if(random_indices.count(current_index) > 0 ):
                possible_words_for_sample.append(word)
            current_index = current_index + 1
    
    return possible_words_for_sample







# In[ ]:





# In[86]:


def createDataFrameFromSampleWords(sample_words):

    #Let 1 = spam and 0 = ham
    all_train_rows = []

    for email in spam_word_count_container:
        single_train_row = []

        #check if that email has the word, 
        #1 if it does, 0 if not
        for word in sample_words:
            if(word in spam_word_count_container[email]):
                single_train_row.append(1)
            else:
                single_train_row.append(0)
        #append 1 for spam for last column which is "IsSpam"
        single_train_row.append(1)
        all_train_rows.append(single_train_row)

    for email in ham_word_count_container:
        single_train_row = []

        #check if that email has the word, 
        #1 if it does, 0 if not
        for word in sample_words:
            if(word in ham_word_count_container[email]):
                single_train_row.append(1)
            else:
                single_train_row.append(0)
        #append 0 for ham for last column which is "IsSpam"
        single_train_row.append(0)
        all_train_rows.append(single_train_row)




    is_spam_col = "IsSpam"
    sample_words.append(is_spam_col)


    Train_df = pd.DataFrame(all_train_rows, columns = sample_words)

    return Train_df


# In[87]:


from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestClassifier

def calculateProbasForTrainDataFrame(train_df):
    X_train = Train_df.drop("IsSpam", axis = 1)
    y_train = Train_df["IsSpam"]
    forest_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    y_probas_forest = cross_val_predict(forest_clf, X_train, y_train, cv=3,
                                    method="predict_proba")
    return y_probas_forest
    


# In[88]:


def sampleXTimesAndAverageProbas(times_to_sample):
    probas_per_sample = []
    times_sampled = 0
    while times_sampled < times_to_sample:
        words_from_sample = SamplePortionFromEveryEmail(spam_word_count_container, ham_word_count_container, 0.1)
        df_for_sample = createDataFrameFromSampleWords(words_from_sample)
        probas_to_append = calculateProbasForTrainDataFrame(df_for_sample)
        probas_per_sample.append(probas_to_append[:,0])
        times_sampled = times_sampled + 1
    
    return probas_per_sample
    
probas_for_ten_samples = sampleXTimesAndAverageProbas(10)


# In[97]:


print(np.shape(probas_for_ten_samples))


# In[98]:


def calcAverageForColumn2DProbaArray(proba_array):
    
    average_probas_to_return = []
    
    number_cols = len(proba_array[0])
    
    col_index = 0
    
    proba_as_np = np.asarray(proba_array)
    
    while col_index < number_cols:
        current_cols = proba_as_np[:,col_index]
        total_cols = len(current_cols)
        mean_score = (sum(current_cols)/total_cols)
        average_probas_to_return.append(mean_score)
        col_index = col_index + 1
    

    return average_probas_to_return
average_of_probas = calcAverageForColumn2DProbaArray(probas_for_ten_samples)


# In[99]:


print(np.shape(np.asarray(average_of_probas)))


# In[100]:


def getYValsFromDataset():
    y_train_return = []
    for email in spam_word_count_container:
          
        #append 1 for spam
        y_train_return.append(1)
        

    for email in ham_word_count_container:
          
        #append 0 for ham
        y_train_return.append(0)
    
    return y_train_return
y_train_for_accuracy = getYValsFromDataset()


# In[101]:


print(average_of_probas[0:10])

#need to round to 0 or 1
rounded_averages = [int(round(val)) for val in average_of_probas]

print(rounded_averages[0:10])

inverted_rounded_averages = []
for value in rounded_averages:
    if(value == 1):
        inverted_rounded_averages.append(0)
    else:
        inverted_rounded_averages.append(1)
print(inverted_rounded_averages[0:10])


# In[102]:


from sklearn.metrics import accuracy_score
accuracy_score(y_train_for_accuracy, inverted_rounded_averages)

