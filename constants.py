import datetime, functools, os
import discord
from discord.ext import commands

BASEPATH = os.path.dirname(__file__)
COGSPATH = BASEPATH + "\\cogs"

emptyfield = ":black_large_square: :black_large_square: :black_large_square:\n:black_large_square: :black_large_square: :black_large_square:\n:black_large_square: :black_large_square: :black_large_square:"

def checkcomma(number):
        if ',' in number:
            return number.replace(',', '.')
        else:
            return number

def logmsg(msg: discord.Message) -> str:
    result = f'[{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ["{msg.guild}"->"{msg.channel}"]' 
    result += f' QuantumBot: {msg.content} \n'
    return result


def logcommand(ctx: discord.ext.commands.Context) -> str:
    trace = f'[{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] ["{str(ctx.guild)}"->"{ctx.channel}"] '
    trace +=  f'{str(ctx.author)}: {str(ctx.message.content)} \n'
    return trace

def getbotkey():
    with open(BASEPATH[:-17] + "discordkey.txt", "r") as file:
        return file.read()

PI = 3.141592653589793238462643383279


LETTERMAPPING = {
    ' ': '10', 'a': '11', 'b': '12', 'c': '13', 'd': '14', 'e': '15', 'f': '16','g': '17','h': '18','i': '19','j': '20','k': '21','l': '22','m': '23',
    'n': '24', 'o': '25', 'p': '26', 'q': '27','r': '28','s': '29','t': '30','u': '31','v': '32','w': '33','x': '34','y': '35','z': '36','!': '37','A': '38',
    'B': '39','C': '40','D': '41','E': '42','F': '43','G': '44','H': '45','I': '46','J': '47','K': '48','L': '49','M': '50','N': '51','O': '52','P': '53',
    'Q': '54','R': '55','S': '56','T': '57','U': '58','V': '59','W': '60','X': '61','Y': '62','Z': '63','ü': '64','Ü': '65','ö': '66','Ö': '67','ä': '68',
    'Ä': '69',  '-': '70',  '+': '71',  '"': '72',  "'": '73',  '/': '74',  '.': '75',  '*': '76',  ',': '77',  ':': '78',  '#': '79',  '=': '80',  '1': '81',
    '2': '82',  '3': '83',  '4': '84',  '5': '85',  '6': '86',  '7': '87',  '8': '88',  '9': '89',  '?': '90',  '0': '91'
}

NUMBERMAPPING = {
    '10': ' ',  '11': 'a',  '12': 'b',  '13': 'c',  '14': 'd',  '15': 'e',  '16': 'f',  '17': 'g',  '18': 'h',  '19': 'i',  '20': 'j',  '21': 'k',  '22': 'l',
    '23': 'm',  '24': 'n',  '25': 'o',  '26': 'p',  '27': 'q',  '28': 'r',  '29': 's',  '30': 't',  '31': 'u',  '32': 'v',  '33': 'w',  '34': 'x',  '35': 'y',
    '36': 'z',  '37': '!',  '38': 'A',  '39': 'B',  '40': 'C',  '41': 'D',  '42': 'E',  '43': 'F',  '44': 'G',  '45': 'H',  '46': 'I',  '47': 'J',  '48': 'K',
    '49': 'L',  '50': 'M',  '51': 'N',  '52': 'O',  '53': 'P',  '54': 'Q',  '55': 'R',  '56': 'S',  '57': 'T',  '58': 'U',  '59': 'V',  '60': 'W',  '61': 'X',
    '62': 'Y',  '63': 'Z',  '64': 'ü',  '65': 'Ü',  '66': 'ö',  '67': 'Ö',  '68': 'ä',  '69': 'Ä',  '70': '-',  '71': '+',  '72': '"',  '73': "'",  '74': '/',
    '75': '.',  '76': '*',  '77': ',',  '78': ':',  '79': '#',  '80': '=',  '81': '1',  '82': '2',  '83': '3',  '84': '4',  '85': '5',  '86': '6',  '87': '7',
    '88': '8',  '89': '9',  '90': '?',  '91': '0'
}
