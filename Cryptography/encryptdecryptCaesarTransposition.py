import time
import math
key = 8
translated=''
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def encryptCaesar(message,key):
	translated = ''
	for symbol in message:
		if symbol in SYMBOLS:
			symbolIndex = SYMBOLS.find(symbol)
			translatedIndex = (symbolIndex+key) % 52
			translated = translated + SYMBOLS[translatedIndex]
		else:
			translated = translated + symbol
	return translated

def decryptCaesar(cipher,key):
	translated = ''
	for symbol in cipher:
		if symbol in SYMBOLS:
			symbolIndex = SYMBOLS.find(symbol)
			translatedIndex = (symbolIndex-key) % 52
			translated = translated + SYMBOLS[translatedIndex]
		else:
			translated = translated + symbol
	return translated

def encryptTranspositionMessage(message,key):
    ciphertext=['']*key

    for column in range(key):
        currentIndex = column

        while currentIndex < len(message):
            ciphertext[column]+=message[currentIndex]
            currentIndex+=key

    return ''.join(ciphertext)

def decryptTranspositionMessage(message,key):
    numOfColumns = int(math.ceil(len(message)/float(key)))
    numOfRows = key
    numOfShadeBoxes = (numOfColumns*numOfRows) - len(message)

    plaintext= ['']*numOfColumns
    column = 0
    row = 0

    for symbol in message:
        plaintext[column] += symbol
        column+=1

        if(column==numOfColumns) or (column==numOfColumns-1 and row >= numOfRows-numOfShadeBoxes):
            column = 0
            row +=1
    return ''.join(plaintext)

def main():
    fileinput = ""
    myMode = ""
    fileoutput = ""
    metode = ""
    fileinput = input("File name: ")
    fileObj = open(fileinput)
    content = fileObj.read()
    fileObj.close()

    metode = input("Metode caesar / transposition :")
    myMode = input("Mode encrypt/decrypt: ")
    print('%sing...' %(myMode.title()))

    startTime = time.time()
    if myMode == 'encrypt' and metode == 'caesar':
	    translated = encryptCaesar(content,key)
    elif myMode == 'decrypt' and metode == 'caesar':
	    translated = decryptCaesar(content,key)
    elif myMode == 'encrypt' and metode == 'transposition':
	    translated = encryptTranspositionMessage(content,key)
    elif myMode == 'decrypt' and metode == 'transposition':
	    translated = decryptTranspositionMessage(content,key)

    totalTime = round(time.time() - startTime,2)
    print('%sion time: %s seconds' %(myMode.title(),totalTime))

    fileoutput = input('File output: ')
    outputFileObj = open(fileoutput,'w')
    outputFileObj.write(translated)
    outputFileObj.close()

if __name__ == "__main__":
    main()