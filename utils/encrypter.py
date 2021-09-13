import random
from constants import LETTERMAPPING, NUMBERMAPPING, BASEPATH, COGSPATH
from textwrap import wrap


"""This contains the encrypting functionality, while the 'encrypting' class interfaces with discord"""
class Encrypter:

    @staticmethod
    def generatekey():
        int0 = random.randint(15000, 35000)
        int1 = random.randint(5000000, 10000000)
        key = f'{hex(int0)}{hex(int1)}'.replace('0x', '')
        with open('./key.txt', 'w+') as keyfile: 
            keyfile.write(f'{key}\n')

    @staticmethod
    def getkey():
        with open('./key.txt', 'r') as keyfile:
            key = keyfile.read()
        return f'{key[0:4]} {key[4:10]}'

    @staticmethod
    def mainencode(base, message, encrypt = False) -> str:
        ch_list = []
        numberlist = []
        modifiedlist = []
        finalencode = ''

        if base == 'hexkey':
            generatekey()
            int0 = getkey().split()[0]
            int1 = getkey().split()[1]

        ch_list = list(message)
        for char in ch_list:
            numberlist.append(int(LETTERMAPPING.get(char)))
        
        for number in numberlist:
            if base == 2 and encrypt == False:
                modifiedlist.append(bin(number))
            elif base == 16 and encrypt == False:
                modifiedlist.append(hex(number))
            elif base == 2 and encrypt:
                modifiedlist.append(bin(number * 241 + 547))
            elif base == 16 and encrypt:
                modifiedlist.append(hex(number * 31513 + 4514113))
            elif base == 'hexkey':
                modifiedlist.append(hex(number * int(int0, 16) + int(int1, 16)))
                
        if encrypt == False:
            finalencode = ' '.join(modifiedlist)
        elif base == 'hexkey' or base == 16 and encrypt:
            finalencode = ''.join(modifiedlist).replace('0x', '')
        elif base == 2 and encrypt:
            finalencode = ''.join(modifiedlist).replace('0b', ' ')

        return finalencode

    @staticmethod
    def maindecode(base, message, decrypt = False) -> str:
        msglist = []
        ints = []
        finaldecode = ''
        if decrypt == False:
            msglist = message.split()
        elif base == 'hexkey' or decrypt and base == 16:
            msglist = wrap(message, 6)
        elif decrypt and base == 2:
            msglist = message.split()

        if base == 'hexkey':
            int0 = getkey().split()[0]
            int1 = getkey().split()[1]

        for msg in msglist:
            if decrypt == False:
                ints.append(int(msg, base))
            elif base == 16 and decrypt:
                ints.append(int((int(msg, base) - 4514113) / 31513))
            elif base == 2 and decrypt:
                ints.append(int((int(msg, base) - 547) / 241))
            elif base == 'hexkey':
                ints.append(int((int(msg, 16) - int(int1, 16)) / int(int0, 16)))

        for n in ints:
            finaldecode += NUMBERMAPPING.get(str(n))

        return finaldecode

    @staticmethod
    def findbestmatch(attempts: list, lang):
        class Match:
            def __init__(self, sentence):
                self.sentence = sentence
                self.accuracy = 0

        matches = list()
        for att in attempts:
            matches.append(Match(att.lower()))
        
        bestMatch = matches[0]

        if (lang == "eng" or lang == "both"):
            bestMatch = Encrypter.combfile(COGSPATH + '\data\dictionary.txt', matches)
        
        elif (lang == "ger" or lang == "both"):
            bestMatch = Encrypter.combfile(COGSPATH + '\data\german.txt', matches)
        
        return f"[Accuracy: {bestMatch.accuracy}]{bestMatch.sentence}"


    @staticmethod
    def transpose(key: int, content: str) -> str:
        result = ""
        remainder = key - len(content) % key
        if (remainder != 0):
            while remainder > 0:
                content += chr(random.randint(97, 122))
                remainder -= 1
        for i in range(1, key + 1):
            result += content[::key]
            content = content[1:]

        return result

    @staticmethod
    def substitution(key:int, content: str) -> str:
        result = ""
        lwrtxt = content.lower()
        for i in range(len(content)):
            if (ord(lwrtxt[i]) in range(96, 123)):
                if (content[i] != lwrtxt[i]):
                    result += chr(((ord(lwrtxt[i]) - 97 + key) % 26) + 97).upper()
                else:
                    result += chr(((ord(lwrtxt[i]) - 97 + key) % 26) + 97)
            else:
                result += content[i]

        return result

    @staticmethod
    def solvetranspose(content) -> list:
        attempts = 100
        bfkey = 1
        results = list()
        while attempts > 0 and bfkey < len(content):
            result = ""
            if (len(content) % bfkey != 0):
                bfkey += 1
                continue
            attempts -= 1
            bars = len(content) / bfkey
            contentcpy = content
            for j in range(1, int(bars) + 1):
                result += contentcpy[::int(bars)]
                contentcpy = contentcpy[1:]
            results.append(f"[KEY: {bfkey}]\n{result}")
            bfkey += 1
        
        return results 

    @staticmethod
    def combfile(filepath, matches):
        bestMatch = matches[0]
        with open(filepath, 'r') as file:
            words = file.read().split('\n')
            for match in matches:
                for w in match.sentence.split():
                    if (len(w) >= 4):
                        if (w in words):
                            match.accuracy += 1
                if (match.accuracy > bestMatch.accuracy):
                    bestMatch = match
                    
        return bestMatch

    @staticmethod
    def monoalpha(content):
        content = content.lower()
        newalpha = ""
        result = ""
        base = list("abcdefghijklmnopqrstuvwxyz")
        for i in range(0, len(base)):
            choice = random.choice(base)
            newalpha += choice
            base.remove(choice)

        for i in range(0, len(content)):
            if (content[i] not in newalpha):
                result += content[i]
            else:
                charindex = ord(content[i]) - 97
                result += newalpha[charindex]

        return result

    @staticmethod
    def solvemonoalpha(content):
        base = list("abcdefghijklmnopqrstuvwxyz")
        relativeprobability = list("enisratdhulcgmobwfkzpvjyxq")
        occurencemap = dict()
        content = list(content)
        relativemap = dict()
        result = ""

        for i in range(0, len(base)):
            if base[i] in content:
                occurencemap[base[i]] = content.count(base[i]) 
        
        #Sorting occurencemap by descending occurence of char
        occurencemap = {k: v for k, v in sorted(occurencemap.items(), key = lambda item: item[1])}

        newalpha = list(occurencemap.values())
        for i in range(0, len(content)):
            result += newalpha[ord(content[i]) - 97]

        return result
        





