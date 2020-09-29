import cryptomath,sys,secrets

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def vignere(message):
    myKey = 'DUMPLINGS'
    translated = encryptVignere(myKey,message)
    print('Vignere Key: ',myKey)
    print('Vignere Ciphertext:')
    print(translated)
    print()
    print('Vignere Plaintext:')
    print(message)


def affine(message):
    myKey=267
    print("Affine Key:",myKey)
    translated=encryptAffine(myKey,message)
    print('Affine Key-A: ',translated[0])
    print('Affine Key-B: ',translated[1])
    print('Affine ModInverse Key-A: ',translated[2])
    print('Affine Ciphertext:')
    print(translated[3])
    print()
    print('Affine Plaintext')
    print(message)


def onetimepad(message):
    myKey=generateOtp(message)
    print('One Time Pad Key: ',myKey)
    translated=encryptVignere(myKey,message)
    print('One Time Pad Ciphertext:')
    print(translated)
    print('One Time Pad Plaintext')
    print(message)
    
def main():
    myMessage = """"Encryption works. Properly implemented strong crypto systems are one of the few things
that you can rely on. Unfortunately, endpoint security is so terrifically weak that NSA can
frequently find ways around it." ― Edward Snowden"""
    
    method=input('Method of Encrypt Message (Affine / Vigenere / One Time Pad): ')
    if(method.lower()=='affine'):
        affine(myMessage)
    elif(method.lower()=='vigenere'):
        vignere(myMessage)
    elif(method.lower()=="one time pad"):
        onetimepad(myMessage)

def encryptVignere(key, message):
    translated = []
    keyIndex = 0
    key = key
    
    for symbol in message: # Loop through each symbol in message.
        num = LETTERS.find(symbol.upper())
        if num != -1:
            num += LETTERS.find(key[keyIndex])
            num %= len(LETTERS)
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())
            
            keyIndex += 1 # Move to the next letter in the key.
            
            if keyIndex == len(key):
                keyIndex = 0
        else:
            # Append the symbol without encrypting/decrypting.
            translated.append(symbol)
    return ''.join(translated)

def encryptAffine(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB)
    modInverseOfKeyA = cryptomath.findModInverse(keyA, len(LETTERS))
    ciphertext = ''
    for symbol in message:
        if symbol in LETTERS:
            # Encrypt the symbol:
            symbolIndex = LETTERS.find(symbol)
            ciphertext += LETTERS[(symbolIndex * keyA + keyB) % len(LETTERS)]
        else:
            ciphertext += symbol # Append the symbol without encrypting.
    return keyA,keyB,modInverseOfKeyA,ciphertext

def getKeyParts(key):
    keyA = key // len(LETTERS)
    keyB = key % len(LETTERS)
    return (keyA, keyB)


def checkKeys(keyA, keyB):
    if cryptomath.gcd(keyA, len(LETTERS)) != 1:
        sys.exit('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (keyA, len(LETTERS)))
        

def generateOtp(message):
    otp = ''
    for i in range(len(message)):
        otp += secrets.choice(LETTERS)
    return otp

if __name__ == '__main__':
    main()