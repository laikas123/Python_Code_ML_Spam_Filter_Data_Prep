



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
	word = word.replace("(", "")
	word = word.replace(")", "")
	word = word.replace("/", "")
	word = word.replace("\\", "")
	word = word.replace('"', "")

	return word

def isCapitalLetter(letter):
	print(letter)
	if(letter == "A" or letter == "B" or letter == "C" or letter == "D" or letter == "E" or letter == "F" or letter == "G" or letter == "H" or letter == "I" or letter == "J" or letter == "K" or letter == "L" or letter == "M" or letter == "N" or letter == "O" or letter == "P" or letter == "Q" or letter == "R" or letter == "S" or letter == "T" or letter == "U"  or letter == "V"  or letter == "W"  or letter == "X"  or letter == "Y"  or letter == "Z" ):
		return True
	else:
		return False


def isUpperCaseWord(word):
	#remove symbols and punctuation since only letters can be capital
	word = removeAllPunctFromAString(word)
	word = removeAllSymbolsFromAString(word)
	#if the word was just symbols and punctuation 
	#return False if the word was all symbols and punctuation
	print(word)
	if(len(word) == 0):
		return False
	sawACapitalLetter = False
	for letter in word:
		print(letter)
		if(isCapitalLetter(letter) == False):
			return False

	return True

def isAllSymbolWord(word):
	for letter in word:
		if(letter != "?" and letter != "/" and letter != "\\" and letter != "|" and letter != "~" and letter != "`" and letter != "<" and letter != ">" and letter != "," and letter != "." and letter != ":" and letter != ";" and letter != "\"" and letter != "'" and letter != "[" and letter != "]" and letter != "{" and letter != "}" and letter != "(" and letter != ")" and letter != "-" and letter != "—" and letter != "=" and letter != "+" and letter != "!" and letter != "@" and letter != "#" and letter != "$" and letter != "%" and letter != "^" and letter != "&" and letter != "*" ):
			return False
	return True

print(isAllSymbolWord(".$$$$$$%##@#@#@"), "is symbol word")


print(isUpperCaseWord("HELLOTHERE$$$$$$$"), "is uppercase")

myword = "@#$%^&*()Hi"

print(removeAllSymbolsFromAString(myword))

myword = "()\'\"\"\"\"\"\"\"\"(((((())))))))))!!!!!:::::\"\"\"\"\'\'\'\'\'\'\'\'\'\'\'[[[[[[[Hi"

print(removeAllPunctFromAString(myword))


mywords = ["hello"]

print(mywords.count("hi"))
