import discord
from discord.ext import commands
from constants import logcommand



class Banning(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Banning loaded.')

    # Commands
    @commands.command(aliases=["Kick", "KICK"])
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} has been kicked.')

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["Ban", "BAN"])
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member.mention} has been permanently banned. Reason: {reason}')

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["Unban", "UNBAN"])
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} has been unbanned.')
                return

    # Error handling

    @kick.error
    @ban.error
    @unban.error
    async def missingargs(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required arguments.')

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Lacking permissions.')


    DESCRIPTION = f'''```BANNING:

!ban *user* **reason**
!unban *user*
!kick *user* **reason**
-----------------------------------
    *: required | **: optional```'''

def setup(client):
    client.add_cog(Banning(client))
