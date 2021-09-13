import os, time, re, stat, math, quantumbot, discord

from discord.ext.commands.cog import _cog_special_method
from discord.ext import commands
from constants import logcommand, COGSPATH, BASEPATH
from . import banning as bn, encrypting as enc, math as mt, web

asgn0 = lambda n: [0 for _ in range(n)]
addlist = lambda l1, l2: [l1[_] + l2[_] for _ in range(0, len(l1))]



def getSTSIZE(path):
    stats = os.stat(path)
    if len(str(stats[stat.ST_SIZE])) < 4:
        return '0' + str(stats[stat.ST_SIZE])
    return stats[stat.ST_SIZE]

def getModules(dirpath, mod=14, listofcommands = [], listofmodules = [], counter = 0):
    message = ''
    for filename in os.listdir(dirpath):
        if filename.endswith('.py') and filename != '__init__.py' and filename != 'constants.py':
            listofmodules.append(filename[:-3])
            currentFullModule = f'{filename[:-3].upper()}:'
            path = dirpath + '\\' + filename
            with open(path, 'r') as currentFile:
                lines = currentFile.readlines()
                for line in lines:
                    if 'async def' in line and 'on_' not in line and 'error' not in line:
                        x = re.search('\(', line)
                        functionNameSubstring = line[mod:x.start()]
                        listofcommands.append(functionNameSubstring)
                        currentFullModule += f'\n\t{functionNameSubstring}'
                    else:
                        continue
                message += f'''```\n{currentFullModule}```'''
        else:
            continue
    return message

def getInfo(dirpath, increaseModules = 0, currdir = None):
    amountoffiles, amountoflines, amountofmodules, totalsize = asgn0(4)
    metadata = ''
    for filename in os.listdir(currdir):
        if '__init__' not in filename and filename.endswith('.py') or filename.endswith('.md'):
            path = dirpath + filename
            with open(path, 'r') as currFile:
                amountoflines += len(currFile.readlines())
            if filename == 'README.md':
                amountofmodules += 0
            else:
                amountofmodules += increaseModules
            amountoffiles += 1
            stats = os.stat(path)
            metadata += f'\n {filename[:-3].upper()} size: ' + ' ' * (11-len(filename[:-3]))
            metadata += f'{getSTSIZE(path)} Bytes, time last changed: {time.asctime(time.localtime(stats[stat.ST_MTIME]))[:-5]}'
            totalsize += stats[stat.ST_SIZE]
    return (amountofmodules, amountoffiles, amountoflines, metadata, totalsize)
   

class Maintenance(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Maintenance loaded.')

    @commands.command(aliases=['Help', 'HELP'])
    async def help(self, ctx, *, command=None):
        if command == None:
            FULLMESSAGE = getModules(BASEPATH, mod=10)
            FULLMESSAGE += getModules(COGSPATH)
            FULLMESSAGE += f':exclamation: Type !help \*module\* to find out more about a module and the syntax for its commands.'
            await ctx.send(FULLMESSAGE)
        elif command == 'banning':
            await ctx.send(bn.Banning.DESCRIPTION)
        elif command == 'encrypting':
            await ctx.send(enc.Encrypting.DESCRIPTION)
        elif command == 'math':
            await ctx.send(mt.Math.DESCRIPTION)
        elif command == 'bot' or command == 'quantumbot':
            await ctx.send(quantumbot.DESCRIPTION)
        elif command == 'maintenance':
            await ctx.send(Maintenance.DESCRIPTION)
        elif command == 'web':
            await ctx.send(web.Web.DESCRIPTION)
        elif command == 'ascii':
            await ctx.send('No description yet.')
        else:
            await ctx.send('Invalid module name. Type !help for a list of all modules and commands.')

    @commands.command()
    async def purge(self, ctx, number):
        await ctx.channel.purge(limit=int(number))
    
    @commands.command(aliases=['Code'])
    async def info(self, ctx):
        mainInfo = getInfo(
            dirpath = BASEPATH + "\\")
        modulesInfo = getInfo(
            dirpath = COGSPATH + "\\", 
            increaseModules = 1,
            currdir = './cogs')
        metaData = mainInfo[3] + modulesInfo[3]
        totalsize = mainInfo[4] + modulesInfo[4]
        allInfo = addlist(mainInfo, modulesInfo)
        await ctx.send(f"""
    ```python
----- BOT INFO -----

CURRENT AMOUNT OF MODULES: {allInfo[0]}
CURRENT AMOUNT OF FILES: {allInfo[1]}
TOTAL AMOUNT OF LINES: {allInfo[2]}

METADATA: {metaData}

----------------------------------------------
    TOTAL SIZE {totalsize} Bytes
```
        """)

    # @commands.command()
    # async def about(self, ctx):
    #     embed = discord.Embed()
    #     embed.set_image()
        



    DESCRIPTION = '''```MAINTENANCE:

!help **module**-> Shows all commands with their parent modules.
!info  -> Shows several statistics for the bot.

-----------------------------------------
    *: required | **: optional```'''


def setup(client):
    client.add_cog(Maintenance(client))