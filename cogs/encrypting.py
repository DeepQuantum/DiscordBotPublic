import random, os, discord, os, qrcode
from textwrap import wrap
from discord.ext import commands
from constants import LETTERMAPPING, NUMBERMAPPING, logcommand
from PIL import Image
from utils.encrypter import Encrypter

class Encrypting(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Encryping loaded.')

    # Commands

    @commands.command(aliases=['Encode', 'ENCODE'])
    async def encrypt(self, ctx, typeOfEncode, *, message):
        if typeOfEncode == 'hex' or typeOfEncode == 'hexadecimal':
            await ctx.send(Encrypter.mainencode(16, message, encrypt=True))
        elif typeOfEncode == 'bin' or typeOfEncode == 'binary':
            await ctx.send(Encrypter.mainencode(2, message, encrypt=True))
        elif typeOfEncode == 'hexkey':
            await ctx.send(Encrypter.mainencode('hexkey', message, encrypt=True))
        else:
            await ctx.send('Invalid type of encoding.')

    @commands.command(aliases=['Decrypt', 'DECRYPT'])
    async def decrypt(self, ctx, type, *, message):
        if type == 'hex' or type == 'hexadecimal':
            await ctx.send(Encrypter.maindecode(16, message, decrypt=True))
        elif type == 'bin' or type == 'binary':
            await ctx.send(Encrypter.maindecode(2, message, decrypt=True))
        elif type == 'hexkey':
            await ctx.send(Encrypter.maindecode('hexkey', message, decrypt=True))
            os.remove('.\key.txt')
            

    @commands.command()
    async def encode(self, ctx, typeOfEncode, *, message):
        if typeOfEncode == 'bin':
            await ctx.send(Encrypter.mainencode(2, message))
        elif typeOfEncode == 'hex':
            await ctx.send(Encrypter.mainencode(16, message))
        else:
            await ctx.send('Invalid type of encoding.')

    @commands.command()
    async def decode(self, ctx, typeOfDecode, *, message):
        if typeOfDecode == 'bin':
            await ctx.send(Encrypter.maindecode(2, message))
        elif typeOfDecode == 'hex':
            await ctx.send(Encrypter.maindecode(16, message))
        else:
            await ctx.send('Invalid type of decoding.')

    @commands.command()
    async def qrcode(self, ctx, *, content):
        imgpath = os.path.dirname(__file__) + "\data\img.jpg"
        img = qrcode.make(content)
        img.save(imgpath)
        await ctx.send(file=discord.File(imgpath))
        os.remove(imgpath)
        await ctx.message.delete()
    
    @commands.command()
    async def transpose(self, ctx, key: int, *, content):
        await ctx.send(Encrypter.transpose(key, content))

    @commands.command()
    async def detranspose(self, ctx, key, *, content):
        result = ""
        bars = len(content) / key
        for i in range(1, int(bars) + 1):
            result += content[::int(bars)]
            content = content[1:]
        await ctx.send(result)

    @commands.command()
    async def monoalpha(self, ctx, *, content):
        await ctx.send(Encrypter.monoalpha(content))
        

    #TODO bruteforce monoalpha
    @commands.command()
    async def bruteforce(self, ctx, typeofenc, language, *, content):
        results = list()
        if (typeofenc == "transpose"):
            results = Encrypter.solvetranspose(content)

        elif (typeofenc == "sub"):
            for i in range(1, 26):
                results.append(f"Key: {i} -> {substitution(-i, content)}\n-----------------\n")

        elif (typeofenc == "monoalpha"):
            await ctx.send(Encrypter.solvemonoalpha(content))

        if (language == "None"):
            for i in results:
                await ctx.send(i)

        else:
            await ctx.send(Encrypter.findbestmatch(results, language))
            
    @commands.command()
    async def substitution(self, ctx, key: int, *, content):
        await ctx.send(Encrypter.substitution(key, content))


    # Error handling
    @encode.error
    @encrypt.error
    async def encrypt_error_invoke(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Overflow error.')
    
    @transpose.error
    async def badargument(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Wrong parameters used.')

    @bruteforce.error
    @qrcode.error
    @encode.error
    @decode.error
    @decrypt.error
    @encrypt.error
    async def missingarg(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please enter a valid message to encode/decode.')
        

    DESCRIPTION = f'''```ENCRYPTING:

!encode *type* *message* |-> Encode a message in binary or hexadecimal. Message is converted without encryption.
        types: hex | bin
!decode *type* *message* |-> Decode a message from binary or hexadecimal.
        types: hex | bin
!encrypt *type* *message* |-> Encrypt a message to binary or hexadecimal. Hexkey uses a one-time randomly generated key.
        types: hex | bin | hexkey
!decrypt *type* *message* |-> Decrypt a message from binary or hexadecimal. With hexkey, message is decrypted using the one-time key, 
                                after which the key is permanently deleted.
        types: hex | bin | hexkey
!qrcode *message* |-> Generate a QR-Code with a message
!transpose *key* *message* |-> Encrypt a message using a columnar transposition cipher with a key
!detranspose *key* *message* |-> Decrypt a message encrypted with a columnar transposition cipher with a key
!bruteforce *type of encoding* *language* *message* |-> attempt to bruteforce decipher a message and find a best match
            types: sub | transpose    languages: ger, eng, both, None (using None will result in showing all results without finding best match)

-----------------------------------
    *: required | **: optional```'''

def setup(client):
    client.add_cog(Encrypting(client))
