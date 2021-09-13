from constants import LETTERMAPPING
import subprocess
import random
import os

def generateKey():
    int0 = random.randint(15000, 35000)
    int1 = random.randint(5000000, 10000000)
    key = f'{hex(int0)}{hex(int1)}'.replace('0x', '')
    keyfile = open('.\key.txt', 'w+')
    keyfile.write(f'{key}\n')
    keyfile.close()
    print(f'Key generated: {key}')

def getKey():
    keyfile = open('.\key.txt', 'r')
    key = keyfile.read()
    return f'{key[0:4]} {key[4:10]}'


def encode0_hex(code=None, nmbr_list=None, modified_list=None, encoded_list=None):
    ch_list = list(code)
    for ch in ch_list:
        nmbr_list.append(int(LETTERMAPPING.get(ch)))

    for n in nmbr_list:
        modified_list.append(n * 31415 + 4534534)

    for i in modified_list:
        encoded_list.append(hex(i))

    return ''.join(encoded_list).replace('0x', '')
        
def encode1_bin(code=None, nmbr_list=None, modified_list=None, encoded_list=None):
    ch_list = list(code)
    for ch in ch_list:
        nmbr_list.append(int(LETTERMAPPING.get(ch)))

    for n in nmbr_list:
        modified_list.append(n * 243 + 534)

    for i in modified_list:
        encoded_list.append(bin(i))
    return ' '.join(encoded_list).replace('0b', '')

def encode1_hex(code=None, nmbr_list=None, modified_list=None, encoded_list=None):
    ch_list = list(code)
    for ch in ch_list:
        nmbr_list.append(int(LETTERMAPPING.get(ch)))

    int0 = getKey().split()[0]
    int1 = getKey().split()[1]
    for n in nmbr_list:
        modified_list.append(n * int(int0, 16) + int(int1, 16))

    for i in modified_list:
        encoded_list.append(hex(i))

    return ''.join(encoded_list).replace('0x', '')


def main():
    while True:
        NBMBR_LST = []
        MODIFIED_LST = []
        ENCODED_LST = []
        usrinput = input('\'bin\' for binary, \'hex\' for hexadecimal encoding. Use \'hexkey\' to generate a special one-time use key.\n> ')
        if usrinput == 'bin':
            CODE = input("> ")
            print(encode1_bin(CODE, NBMBR_LST, MODIFIED_LST, ENCODED_LST))
        elif usrinput == 'hex':
            CODE = input("> ")
            print(encode0_hex(CODE, NBMBR_LST, MODIFIED_LST, ENCODED_LST))
        elif 'hexkey' in usrinput:
            if '-throw' in usrinput:
                generateKey()
                CODE = input('> ')
                print(encode1_hex(CODE, NBMBR_LST, MODIFIED_LST, ENCODED_LST))
                os.remove('key.txt')
                print('Key generated and thrown.')
            else:
                generateKey()
                CODE = input('> ')
                print(encode1_hex(CODE, NBMBR_LST, MODIFIED_LST, ENCODED_LST))
        elif usrinput == 'quit' or usrinput == 'exit':
            break
        elif usrinput == 'decode':
            subprocess.run('python .\decoder.py', shell=True)
        else:
            print('Invalid input')


main()
