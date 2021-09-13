import os, random, discord, logging, datetime, asyncio
from discord.ext import commands
from constants import getbotkey, logcommand, logmsg
import discord_components

CLIENT = commands.Bot(command_prefix="!")
CLIENT.remove_command('help')

@CLIENT.event
async def on_ready():
    print("Bot is online.")
    discord_components.DiscordComponents(CLIENT)
    trace = f'[{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}] '
    trace += 'Bot is online. \n'
    with open('qntmbot.log', 'a+') as file:
        file.write(trace)
    
@CLIENT.event
async def on_member_join(member):
    print(f'{member} has joined the server!')


@CLIENT.event
async def on_member_remove(member):
    print(f'{member} has left the server')

@CLIENT.event
async def on_command_completion(ctx, *args):
    trace = logcommand(ctx)
    print(trace)
    with open('qntmbot.log', 'a+') as file:
        file.write(trace)

@CLIENT.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found. Type !help for a list of commands.')
    trace = logcommand(ctx)
    trace += f'[ERROR: {error}]\n'
    print(trace)
    with open('qntmbot.log', 'a+') as file:
        file.write(trace)

@CLIENT.event
async def on_message(message):
    await CLIENT.process_commands(message)
    await asyncio.sleep(0.2)
    if str(message.author) == "Quantum Bot#0604":
        msg = logmsg(message)
        print(msg)
        with open('qntmbot.log', 'a+') as file:
            try:
                file.write(str(msg).replace("\n", " "))
            except UnicodeEncodeError:
                file.write("*Ignoring unicode chars in message* " + msg.encode("ascii", "ignore").decode().replace("\n", " "))

@CLIENT.command(aliases=["PING", "Ping"])
async def ping(ctx):
    result = f":repeat: Ping: **{round(CLIENT.latency * 1000)} ms**"
    await ctx.send(result)


@CLIENT.command(aliases=["Dice", "DICE"])
async def dice(ctx, size=6):
    result = random.choice(range(1, size + 1))
    await ctx.send(f':game_die: (1-{size}): **{result}**')


@commands.has_permissions(administrator=True)
@CLIENT.command()
async def load(ctx, extension):
    CLIENT.load_extension(f'cogs.{extension}')
    print(f'{extension} succesfully loaded.')
    await ctx.send(f'{extension} succesfully loaded.')


@commands.has_permissions(administrator=True)
@CLIENT.command()
async def unload(ctx, extension):
    CLIENT.unload_extension(f'cogs.{extension}')
    print(f'{extension} succesfully unloaded.')
    await ctx.send(f'{extension} succesfully unloaded.')

@commands.has_permissions(administrator=True)
@CLIENT.command()
async def refresh(ctx, extension='all'):
    if extension == 'all':
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename != '__init__.py':
                CLIENT.unload_extension(f'cogs.{filename[:-3]}')
                print(f'Unloading {filename}...')
                CLIENT.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loading {filename}')
                await ctx.send(f'Extension reloaded succesfully: {filename}')
    else:
        CLIENT.unload_extension(f'cogs.{extension}')
        print(f'{extension} succesfully unloaded.')
        CLIENT.load_extension(f'cogs.{extension}')
        print(f'{extension} succesfully loaded.')
        await ctx.send(f'{extension} succesfully reloaded.')


@commands.has_permissions(administrator=True)
@CLIENT.command(aliases=['status'])
async def changestatus(ctx, status, *, custom=None):
    if status == "idle":
        await CLIENT.change_presence(status=discord.Status.idle,
                                     activity=discord.Game('Currently testing...'))
        await ctx.send(":orange_circle: Changed status to idle.")
    elif status == "offline":
        await CLIENT.change_presence(status=discord.Status.offline,
                                     activity=discord.Game('Currently offline.'))
        await ctx.send(":black_circle: Changed status to offline.")
    elif status == "custom":
        await CLIENT.change_presence(status=discord.Status.online,
                                     activity=discord.Game(custom))
        await ctx.send(f':green_circle: Changed status to: {status}. Activity: {custom}')
    else:
        await ctx.send('Not a status.')

@CLIENT.command()
@commands.is_owner()
async def shutdown(ctx):
    confirm = input(f'Shutdown bot?\n y/n >')
    if confirm == 'y':
        await ctx.bot.logout()
    else:
        await ctx.send('Shutdown aborted.')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and '__init__' not in filename:
        CLIENT.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loading {filename}...')

# Error handling

@load.error
@unload.error
@refresh.error
@changestatus.error
async def errorhandler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required argument.')

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Lacking permissions.')

@dice.error
async def diceerror(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('Invalid amount of faces')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Please enter valid a number')

DESCRIPTION = f'''```MAIN BOT COMMANDS:
!ping |-> Shows the ping of the bot.
!dice **number** |-> Rolls a dice. If no specific number is entered, 6 sides are assumed.
!load *module* |-> Loads a module. FOR ADMINS ONLY.
!unload *module* |-> Unloads a module. FOR ADMINS ONLY.
!refresh **module** |-> Refreshes a module. If no module is specified, all will be refreshed.
!changestatus *status* **activity** |-> Changes the bot status. If 'custom' is entered as status, activity can be changed.
---------------------------------------------------------------------
        *: required | **: optional```'''

CLIENT.run(getbotkey())
