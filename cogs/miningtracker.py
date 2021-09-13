import PIL, pyautogui, discord, time, os, pytesseract
from discord.ext.commands.errors import MissingPermissions
from discord.errors import DiscordException
from discord.ext import commands
from PIL import ImageOps
from constants import COGSPATH

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class MiningTracker(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.PATH = COGSPATH + "\\data"
        self.status = "Stopped"

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def starttracking(self, ctx):
        self.status = "Tracking"
        await ctx.send("Now tracking mining.")
        
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def miningupdate(self, ctx, cycles = 1, interval = 2):
        if self.status == "Tracking":
            await ctx.send("Collecting...")
            timestamps = []
            shots = []
            for i in range(1, cycles + 1):
                image = pyautogui.screenshot(region=(0, 0, 1850, 510))
                relpath = self.PATH + f"miners{i}" + ".png"
                image.save(relpath)
                timestamps.append(f"**[{i}]** " + time.strftime("%H:%M:%S %d.%m.%Y"))
                shots.append(relpath)
                time.sleep(int(interval))
            await ctx.send(content='\n'.join(timestamps), files=[discord.File(x) for x in shots])
            [os.remove(x) for x in shots]
        else:
            raise MissingPermissions

    @commands.command()
    async def miningsummary(self, ctx):
        screenshot = ImageOps.invert(pyautogui.screenshot(region=(0, 0, 1000, 510)))
        screenshot.show()
        result = pytesseract.image_to_string(screenshot)
        print(result)
        await ctx.send(result)
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def stoptracking(self, ctx):
        self.status = "Stopped"
        await ctx.send("Stopped tracking.")

    @starttracking.error
    @miningupdate.error
    @stoptracking.error
    async def errorhandler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            ctx.send("Lacking permissions for this command.")

    

def setup(client):
    client.add_cog(MiningTracker(client))