import re
import string


def removeAllSymbolsFromAString(word):
	for letter in word:
		if(isSymbol(letter)):
			word = word.replace(letter, "")

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
    word = word.replace("(", "")
    word = word.replace(")", "")
    word = word.replace("/", "")
    word = word.replace("\\", "")
    word = word.replace('"', "")

    return word

def isPunctuation(letter):
    punctuation_text = re.search(r"([/./?\,\'\-\—\!\:\;\[\]\(\)\/\\\"])", letter)
    if(punctuation_text is None):
        return False
    else:
        return True
    

# def isCapitalLetter(letter):
#     print(letter)
#     if(letter == "A" or letter == "B" or letter == "C" or letter == "D" or letter == "E" or letter == "F" or letter == "G" or letter == "H" or letter == "I" or letter == "J" or letter == "K" or letter == "L" or letter == "M" or letter == "N" or letter == "O" or letter == "P" or letter == "Q" or letter == "R" or letter == "S" or letter == "T" or letter == "U" or letter == "V" or letter == "W" or letter == "X" or letter == "Y" or letter == "Z"):
#         return True
#     else:
#         return False


# def isUpperCaseWord(word):
#     # remove symbols and punctuation since only letters can be capital
#     word = removeAllPunctFromAString(word)
#     word = removeAllSymbolsFromAString(word)
#     # if the word was just symbols and punctuation
#     # return False if the word was all symbols and punctuation
#     print(word)
#     if(len(word) == 0):
#         return False
#     sawACapitalLetter = False
#     for letter in word:
#         print(letter)
#         if(isCapitalLetter(letter) == False):
#             return False

#     return True


# def isAllSymbolWord(word):
#     for letter in word:
#         if(letter != "?" and letter != "/" and letter != "\\" and letter != "|" and letter != "~" and letter != "`" and letter != "<" and letter != ">" and letter != "," and letter != "." and letter != ":" and letter != ";" and letter != "\"" and letter != "'" and letter != "[" and letter != "]" and letter != "{" and letter != "}" and letter != "(" and letter != ")" and letter != "-" and letter != "—" and letter != "=" and letter != "+" and letter != "!" and letter != "@" and letter != "#" and letter != "$" and letter != "%" and letter != "^" and letter != "&" and letter != "*"):
#             return False
#     return True


def isMarkupWord(word):
    if "<" in word and ">" in word:
        return True
    else:
        return False


def isMarkupWordRegex(word):
    markup_text = re.search(r"\<([A-Za-z0-9_]+)\>", word)
    if(markup_text is None):
        print("no match")
    else:
        print(markup_text.group(1))

def isLetter(letter):
	letter_text = re.search(r"([A-Za-z])", letter)
	if(letter_text is None):
		print("no match")
	else:
		print(letter_text.group(1))


def isCapitalLetter(letter):
    letter_text = re.search(r"([A-Z])", letter)
    if(letter_text is None):
        print("no match")
    else:
        print(letter_text.group(1))



#\\"   "|"   "~"   "`"   "<"   ">"   ","   "."   ":"   ";"   "\""   "'"   "["   "]"   "{"   "}"   "("   ")"   "-"   "—"   "="   "+"   "!"   "@"   "#"   "$"   "%"   "^"   "&"   "*"
def regexIsSymbol(word):
	symbol_text = re.search(r"([\?\/\\\|\~\`\<\>\,\.\:\;\\\'\[\]\{\}\(\)\-\—\=\+\!\@\#\\\$\%\^\&\*])", word)
	if(symbol_text is None):
		print("no match")
	else:
		print(symbol_text.group(1))

def isSymbol(letter):
	symbol_text = re.search(r"([\?\/\\\|\~\`\<\>\,\.\:\;\\\'\[\]\{\}\(\)\-\—\=\+\!\@\#\\\$\%\^\&\*])", letter)
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



def removeAllPunctFromAString(word):
    for letter in word:
        if(isPunctuation(letter)):
            word = word.replace(letter, "")

    return word
    

# print("is regex symbol")
# print(regexIsSymbol("hfjskhfkjdshf"))


# print(isAllSymbolWord(".$$$$$$%##@#@#@"), "is symbol word")

myword1 = ".....,,,,,(((((((hi"

print(removeAllPunctFromAString(myword1))

isMarkupWordRegex("<hello>")

# isLetter("L")
# print(isPunctuation("$"))
# # # print(isUpperCaseWord("HELLOTHERE$$$$$$$"), "is uppercase")

# myword = "@#$%^&*()Hi"

# print(removeAllSymbolsFromAString(myword))

# # myword = "()\'\"\"\"\"\"\"\"\"(((((())))))))))!!!!!:::::\"\"\"\"\'\'\'\'\'\'\'\'\'\'\'[[[[[[[Hi"

# # print(removeAllPunctFromAString(myword))


# # mywords = ["hello"]

# # print(mywords.count("hi"))
