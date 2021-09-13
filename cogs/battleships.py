import discord
from itertools import cycle
from numpy import concatenate
from utils.battleshipplayer import BattleshipPlayer
from discord.ext import commands
from discord_components import Button, ButtonStyle
from utils.botexceptions import InvalidParameterRangeError, InvalidStateError

class Battleships(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.players = []
        self.cycleplayers = []
        self.currentplayer = None
        self.currentplayers = 0
        self.started = False
        self.placed = False

    def getenemy(self) -> BattleshipPlayer:
        copy = list(self.players)
        copy.remove(self.currentplayer)
        return copy[0]
    
    @commands.command(aliases=["Battleships"])
    async def battleships(self, ctx):
        button1 = Button(style=ButtonStyle.blue, label="Register player")
        button2 = Button(style=ButtonStyle.blue, label="Register player")
        openmsg = await ctx.send("Opened game. Waiting for 2 players to register.", components=[button1, button2])

        res = await self.client.wait_for("button_click")
        if res.channel == ctx.message.channel:
            self.register(res.user)
            await res.respond(content="You're now registered. Check your DM's!")
            await res.user.send("You're now registered!")
            await openmsg.edit("Opened game. Waiting for 1 player to register.", components=[button1])

        res2 = await self.client.wait_for("button_click")
        if res2.channel == ctx.message.channel:
            self.register(res2.user)
            await res2.respond(content="You're now registered. Check your DM's!")
            await res2.user.send("You're now registered!")
            await openmsg.delete()
            await ctx.send(self.start())

            for i in self.players:
                await i.user.send("```You can now place your ships by using the !place command. " + 
                 "Specify your ship type, x and y coordinates and the orientation (v|h). For example, '!place Carrier 2 1 h'.```")
                i.discmessages["remainingships"] = await i.user.send("```Remaining ships: Carrier, Frigate, Destroyer.```")
                i.discmessages["placing"] = await i.user.send(i.ownfieldstr)

    def register(self, user):
        self.players.append(BattleshipPlayer(user))
        self.currentplayers += 1
        return f"{user.name} registered as Player {self.currentplayers}"

    def start(self):
        self.started = True
        self.cycleplayers = cycle(self.players)
        self.currentplayer = next(self.cycleplayers)

        return f"{self.players[0].name} is playing against {self.players[1].name}. Good luck and have fun!"

    def checkargs(self, x = "", y = "", r = "h", stype = "Destroyer"):
        self.checkstate()
        try:
            x = int(x) - 1
            y = int(y) - 1
        except:
            raise InvalidParameterRangeError(x, y)
        if x not in range(10) or y not in range(10) or r not in ["h", "v"] or stype not in BattleshipPlayer.getships()[1:]:
            raise InvalidParameterRangeError(x, y)
        return x, y

    def checkstate(self):
        if not self.started:
            raise InvalidStateError

    @commands.command(aliases=["Place"])
    async def place(self, ctx, stype, x, y, r):
        stype = stype.title()
        r = r.lower()
        x, y = self.checkargs(x, y, r, stype)
        if (isinstance(ctx.channel, discord.channel.DMChannel)):
            player = [x for x in self.players if x.user.name == ctx.author.name][0]
            if (player != None):
                response = player.place(stype, x, y, r)
                if response == 1:
                    await player.discmessages["placing"].edit(player.constructfield())
                else:
                    await player.user.send(response)
                    return
                await player.discmessages["remainingships"].edit("```Remaining ships: " + ', '.join(player.remainingships) + ".```")
                if not player.remainingships:
                    await player.discmessages["remainingships"].delete()
                    await self.awaitreadybutton(player)

    async def awaitreadybutton(self, player):
        readymsg = await player.user.send("All ships placed. Press the button to confirm that you're ready.", 
            components=[Button(style=ButtonStyle.red, label="Ready")])
        response = await self.client.wait_for("button_click")
        if response.user in [x.user for x in self.players] and readymsg == response.message:
            await readymsg.delete()
            player.ready = True
        _ready = True
        for i in self.players:
            if not i.ready: _ready = False
        if _ready:
            await self.startbattle()

    async def startbattle(self):
        self.placed = True
        for i in self.players:
            await self.sendgamemessages(i, True)
        self.currentplayer.discmessages["turn"] = await self.currentplayer.user.send("```\U0001F7E9 It's your turn \U0001F7E9 ```")
        self.getenemy().discmessages["turn"] = await self.getenemy().user.send("```\U0001F7E5 It's currently the enemy's turn \U0001F7E5```")

    async def sendgamemessages(self, player, start):
        await player.user.send("```Your field:```")
        player.discmessages["ownfield"] = await player.user.send(player.constructfield())
        await player.user.send("```Enemy's field:```")
        player.discmessages["enemyfield"] = await player.user.send(self.getenemy().constructfield().replace("\U0001F6A2", "\u2b1b"))
        if not start:
            player.discmessages["turn"] = await player.user.send(player.discmessages["turn"].content)

    @commands.command()
    async def fire(self, ctx, x, y):
        x, y = self.checkargs(x, y)
        self.currentplayer.firemessagecount += 1
        if not self.placed:
            await ctx.send("Some players aren't ready yet.")
            return
        if ctx.message.author.name == self.currentplayer.name:
            enemy = self.getenemy()
            returncode = enemy.checkhit(x, y)
            if returncode == -1:
                await ctx.message.author.send("You've already shot at this spot. Try again!")
                return
            elif returncode == 3:
                self.currentplayer.enemyfield[x][y] = "\U0001F4A5"
                await self.checkwin()
            elif returncode == 2:
                self.currentplayer.enemyfield[x][y] = "\u274c"
            await self.updatemessages(self.currentplayer.firemessagecount)
            self.currentplayer = next(self.cycleplayers)
        else:
            await ctx.message.author.send("It's currently the enemy's turn.")
            return

    async def checkwin(self):
        if 1 not in concatenate(self.getenemy().ownfield):
            await self.currentplayer.user.send("You won! Congratulations!")
            await self.getenemy().user.send("You lost!")


    async def updatemessages(self, messagecount):
        enemyfield = self.getenemy().constructfield().replace("\U0001F6A2", "\u2b1b")
        if messagecount > 10:
            await self.sendgamemessages(self.currentplayer, False)
            messagecount = 0
        else:
            await self.currentplayer.discmessages["enemyfield"].edit(enemyfield)
            await self.currentplayer.discmessages["turn"].edit("```\U0001F7E5 It's currently the enemy's turn \U0001F7E5```")
            await self.getenemy().discmessages["ownfield"].edit(self.getenemy().constructfield())
        await self.getenemy().discmessages["turn"].edit("```\U0001F7E9 It's your turn \U0001F7E9 ```")  
    
    @place.error
    @fire.error
    async def commanderror(self, ctx, error):
        if (isinstance(error, commands.MissingRequiredArgument)):
            await ctx.send(f"Please enter the all the arguments for the command. You are missing: {error.param}")
        elif (isinstance(error, InvalidParameterRangeError)):
            await ctx.send("Some of the arguments you provided were out of the specified range.")
        elif (isinstance(error, InvalidStateError)):
            await ctx.send("There are currently no open games or the game hasn't started yet. You can open a game by calling its command and inviting some friends.")

def setup(client):
    client.add_cog(Battleships(client))




        
