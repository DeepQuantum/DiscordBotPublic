from itertools import cycle
from utils.botexceptions import InvalidStateError
from utils.player import Player
import discord, emoji as EMJ
from discord.ext import commands
from discord_components import Button, ButtonStyle

class TicTacToe(commands.Cog):


    @staticmethod
    def reactions() -> list:
        return [":up-left_arrow:", ":up_arrow:", ":up-right_arrow:", ":left_arrow:", ":blue_circle:", 
        ":right_arrow:", ":down-left_arrow:", ":down_arrow:", ":down-right_arrow:"]

    @staticmethod
    def getpos(dir) -> int:
        return TicTacToe.reactions().index(dir)

    def __init__(self, client):
        self.client = client
        self.n = 0
        self.hascustomsize = None
        self.players = []
        self.cycleplayers = []
        self.currentplayers = 0
        self.opened = False
        self.started = False
        self.currentplayer = None
        self.field = []
        self.gamestring = ""
        self.currentplayermsg = None

    def constructfield(self):
        return (":black_large_square: " * self.n + "\n") * self.n

    def gamesetup(self, n):
        self.opened = True
        self.n = n
        self.hascustomsize = n > 3 
        self.gamestring = self.constructfield()
        self.field = [0 for i in range(n * n)]

    @commands.command(aliases=["TicTacToe"])
    async def tictactoe(self, ctx, n = 3):
        self.gamesetup(n)
        button1 = Button(style=ButtonStyle.blue, label="Register player")
        button2 = Button(style=ButtonStyle.blue, label="Register player")
        openmsg = await ctx.send("Opened game. Waiting for 2 players to register.", components=[button1, button2])

        res = await self.client.wait_for("button_click")
        if res.channel == ctx.message.channel:
            self.register(res.user)
            await res.respond(content=f"You have registered as player 1!")
            await openmsg.edit("Opened game. Waiting for 1 player to register.", components=[button2])
            
        res2 = await self.client.wait_for("button_click")
        if res2.channel == ctx.message.channel:
            self.register(res.user)
            await res2.respond(content="You have registered as player 2!")
            await openmsg.delete()
            startstr = await self.start(ctx)
            await ctx.send(startstr)

        
    def register(self, user, emoji=None):
        if (not self.opened):
            return "No game open."
        self.players.append(Player(user))
        if emoji:
            self.players[self.currentplayers].attributes["emoji"] = emoji
        else:
            if self.currentplayers == 0:
                self.players[0].attributes["emoji"] = ":x:"
            else:
                self.players[1].attributes["emoji"] = ":o:"
        self.currentplayers += 1
        return f"{user.name} registered as Player {self.currentplayers} with emoji {self.players[self.currentplayers-1].attributes['emoji']}"
    
    async def start(self, ctx):
        self.started = True
        self.cycleplayers = cycle(self.players)
        self.currentplayer = next(self.cycleplayers)

        self.currentplayermsg = await ctx.send(f"It's {self.currentplayer.name}'s [{self.currentplayer.attributes['emoji']}] turn")
        self.gamemessage = await ctx.send(self.gamestring)

        if not self.hascustomsize:
            for reaction in self.reactions():
                await self.gamemessage.add_reaction(EMJ.EMOJI_ALIAS_UNICODE_ENGLISH[reaction])


        return f"{self.players[0].name} is playing against {self.players[1].name}. Good luck and have fun!"

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id == self.gamemessage.id and user.name == self.currentplayer.name:
            await reaction.clear()
            result = await self.move(EMJ.demojize(reaction.emoji))
            if result:
                await self.updatemsgs()
            

    @commands.command(aliases=["move, Move"])
    async def movecommand(self, ctx, x ,y):
        if not self.hascustomsize:
            raise InvalidStateError
        if ctx.author.name == self.currentplayer.name:
            _msg = ctx.message
            if self.move(int(y) * self.n + int(x)):
                await self.updatemsgs()
            await _msg.delete()
            

    async def updatemsgs(self):
        await self.gamemessage.edit(self.gamestring)    
        await self.currentplayermsg.edit(f"It's {self.currentplayer.name}'s [{self.currentplayer.attributes['emoji']}] turn")

    async def move(self, dir):
        if not self.hascustomsize:
            pos = self.getpos(dir)
        else:
            pos = dir
        
        self.field[pos] = self.players.index(self.currentplayer) + 1
        newgamelist = self.gamestring.split()
        newgamelist[pos] = self.currentplayer.attributes["emoji"]
        newgamestring = ""
        for i in range(self.n * self.n):
            newgamestring += newgamelist[i] + " "
            if (i + 1) % 3 == 0:
                newgamestring += '\n'
        self.gamestring = newgamestring
        result = await self.checkwin(dir)
        return result

    async def checkwin(self, dir):
        endcode = 0
        board = [self.field[i:i+self.n] for i in range(0, self.n*self.n, self.n)]
        if not self.hascustomsize:
            x = self.getpos(dir) // self.n
            y = self.getpos(dir) % self.n
        else:
            x = dir // self.n
            y = dir % self.n
            
        state = self.players.index(self.currentplayer) + 1
        for i in range(self.n):
            if board[i][y] != state:
                break
            if i == self.n - 1:
                endcode = 1

        for i in range(self.n):
            if board[x][i] != state:
                break
            if i == self.n - 1:
                endcode = 1
        
        if (x == y):
            for i in range(self.n):
                if (board[i][i]) != state:
                    break
                if i == self.n - 1:
                    endcode = 1

        if (x + y == 2):
            for i in range(self.n):
                if (board[i][(self.n - 1) - i]) != state:
                    break
                if (i == self.n - 1):
                    endcode = 1

        if (":black_large_square:" not in self.gamestring):
            endcode = 2

        if endcode != 0:
            await self.closegame(endcode)
            return False

        self.currentplayer = next(self.cycleplayers)
        return True

    async def closegame(self, endcode):
        await self.gamemessage.edit(self.gamestring)
        if endcode == 1:
            await self.gamemessage.channel.send(f"{self.currentplayer.name} has won the game! Congratulatios!")
        elif endcode == 2:
            await self.gamemessage.channel.send(f"Draw between the two players! Well played!")
        for reac in self.gamemessage.reactions:
            await reac.clear()
        self.__init__(self.client)

        

def setup(client):
    client.add_cog(TicTacToe(client))