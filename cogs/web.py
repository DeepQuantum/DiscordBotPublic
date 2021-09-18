import discord, os, random, urllib.request
from discord.errors import HTTPException
from discord.ext import commands
from constants import COGSPATH, logcommand
from discord_components import DiscordComponents, Button
from libretranslatepy import LibreTranslateAPI
from bs4 import BeautifulSoup as BS


class Web(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Web loaded.')

    # Commands
    @commands.command()
    async def google(self, ctx, *, message):
        await ctx.send(f'https://www.google.com/search?client=firefox-b-d&q={message.replace(" ", "+")}')

    @commands.command()
    async def randomwiki(self, ctx):
        await ctx.send("1", components= [
                Button(label="Here's your random article", style=5, url="https://en.wikipedia.org/wiki/Special:Random")])
    
    @commands.command()
    async def randomfact(self, ctx):
        with open(COGSPATH + r'\data\facts.data', 'r') as facts:
            await ctx.send(random.choice(facts.readlines()))

    @commands.command(aliases=["Translate", "translation", "Translation"])
    async def translate(self, ctx, inlang, outlang, *, message):
        lt = LibreTranslateAPI("https://translate.astian.org/")
        await ctx.send(lt.translate(message, inlang, outlang))

    @commands.command(aliases=["w", "W"])
    async def wfwiki(self, ctx, *, input):
        url = f"https://warframe.fandom.com/wiki/Special:Search?query={'+'.join(input.split())}&scope=internal&contentType=&ns%5B0%5D=0&ns%5B1%5D=112&ns%5B2%5D=500&ns%5B3%5D=502"
        fp = urllib.request.urlopen(url)
        contentbytes = fp.read()
        content = contentbytes.decode("utf8")
        fp.close()
        usr = "unified-search__result"
        bs = BS(content, features="html.parser")
        result_count = bs.find(class_=f"{usr}s__count").get_text().split()[1]
        results = bs.find_all(class_="unified-search__results")
        main_result = results[0].find(class_="unified-search__result__content").string
        main_result += " " + results[0].find(class_="unified-search__result__title").get("href")
        await ctx.send(main_result)


        

    @google.error
    async def missingarg(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please enter a valid message to Google.')

    @translate.error
    async def httperror(self, ctx, error):
        if (isinstance(error, urllib.request.HTTPErrorProcessor)):
            ctx.send("There was an error with the command.")

    DESCRIPTION = f'Functionality for web browsing.'

def setup(client):
    client.add_cog(Web(client))
