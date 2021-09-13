import discord
from discord.ext import commands
from constants import PI, checkcomma, logcommand


class Math(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Math loaded.')

    # Commands
    @commands.command(aliases=['Add', 'ADD', 'Addition', 'add'])
    async def addition(self, ctx, number1, number2):
        result = float(checkcomma(number1)) + float(checkcomma(number2))
        await ctx.send(result)

    @commands.command(aliases=['sub','minus','Subtract', 'subtract'])
    async def subtraction(self, ctx, number1, number2):
        result = float(checkcomma(number1)) - float(checkcomma(number2))
        await ctx.send(result)

    @commands.command(aliases=['multi', 'Multiplication', 'multiply'])
    async def multiplication(self, ctx, number1, number2):
        result = float(checkcomma(number1)) * float(checkcomma(number2))
        await ctx.send(result)

    @commands.command(aliases=['divide', 'Divide', 'Division'])
    async def division(self, ctx, number1, number2):
        result = float(checkcomma(number1)) / float(checkcomma(number2))
        await ctx.send(result)

    @commands.command(aliases=['exp', 'hoch', 'Exponent', 'exponent'])
    async def exponentation(self, ctx, number1, number2):
        result = float(checkcomma(number1)) ** float(checkcomma(number2))
        await ctx.send(result)

    @commands.command(aliases=['Pi', 'PI'])
    async def pi(self,ctx):
        await ctx.send(PI)

    @commands.command(aliases=['fact'])
    async def factorial(self, ctx, number0):
        number0 = int(number0)
        numberList = list(range(1, number0))
        for number in numberList:
            number0 *= number
        await ctx.send(number0)

    @commands.command(aliases=['wurzel', 'Root'])
    async def root(self, ctx, number1, number2):
        result = float(checkcomma(number2)) ** (1 / float(checkcomma(number1))) 
        await ctx.send(f'{number1} √ {number2} = {result}')
        
    # Error Handling
    @addition.error
    @subtraction.error
    @multiplication.error
    @division.error
    @factorial.error
    @root.error
    async def missingarg(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please enter all needed numbers.')

    @addition.error
    @subtraction.error
    @multiplication.error
    @division.error
    @factorial.error
    @root.error
    async def valueerror(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Invalid value: Please enter a number.')

    DESCRIPTION = '''```MATH:

!add *number1* *number2* 
!subtract *number1* *number2* 
!multiply *number1* *number2*
!divide *number1* *number2*
!exponent *number1* *number2*
!factorial *number1*
!root *number1* *number2*
!pi

-----------------------------
    *: required | **: optional```'''

def setup(client):
    client.add_cog(Math(client))