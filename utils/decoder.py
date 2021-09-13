from textwrap import wrap
from constants import NUMBERMAPPING
import subprocess
import os


def decode0_hex(msglist, ints, newints, words):
    for msg in msglist:
        ints.append(int(msg, 16))

    for i in ints:
        newints.append(int((i - 4534534) / 31415))

    for n in newints:
        words.append(NUMBERMAPPING.get(str(n)))
    try:
        return ''.join(words)
    except:
        print('Invalid input or key.')

def decode1_bin(msglist, ints, newints, words):
    for msg in msglist:
        ints.append(int(msg, 2))
    
    for i in ints:
        newints.append(int((i - 534) / 243))

    for n in newints:
        words.append(NUMBERMAPPING.get(str(n)))
    return ''.join(words)

def decode1_hex(msglist, ints, newints, words):
    for msg in msglist:
        ints.append(int(msg, 16))
 
    int0 = getKey().split()[0]
    int1 = getKey().split()[1]
    for i in ints:
        newints.append(int((i - int(int1, 16)) / int(int0, 16)))
    
    for n in newints:
        words.append(NUMBERMAPPING.get(str(n)))
    
    return ''.join(words)
    
def getKey():
    try:
        keyfile = open('.\key.txt', 'r')
        key = keyfile.read()
        return f'{key[0:4]} {key[4:10]}'
    except:
        print('No key found.')
        main()


def main():
    while True:
        INTS = []
        NEWINTS = []
        WORDS = []
        usrinput = input('\'bin\' for binary, \'hex\' for hexadecimal decoding. Type \'hexkey\' to decode with the special one-time key.\n> ')
        if usrinput == 'hex':
            MESSAGE = input('> ')
            MSGLIST = wrap(MESSAGE, 6)
            print(decode0_hex(MSGLIST, INTS, NEWINTS, WORDS))
        elif usrinput == 'bin':
            MESSAGE = input('> ')
            MSGLIST = MESSAGE.split()
            print(decode1_bin(MSGLIST, INTS, NEWINTS, WORDS))
        elif usrinput == 'hexkey':
            MESSAGE = input('> ')
            MSGLIST = wrap(MESSAGE, 6)
            print(decode1_hex(MSGLIST, INTS, NEWINTS, WORDS))
            os.remove('key.txt')
            print('Key deleted.')
        elif usrinput == 'quit' or usrinput == 'exit':
            break
        elif usrinput == 'encode':
            subprocess.run('python .\encoder.py', shell=True)
            break
        else:
            print('Invalid input')

main()





