import discord, io, requests, PIL, matplotlib.pyplot as pyplot
from discord.ext import commands 
from PIL import Image, ImageFont, ImageDraw, ImageOps
from constants import COGSPATH

PIXEL_ON = 0
PIXEL_OFF = 255
path = COGSPATH + "\\data\PaintDotNet_AFEcis313j.ico"
datapath = COGSPATH + "\data\ascii.data"

class AsciiArt(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("AsciiArt loaded.")

    @commands.command()
    async def art(self, ctx):
        # Convert msg to ascii art
        image_file_temp = Image.open(io.BytesIO(requests.get(ctx.message.attachments[0].url).content))
        CODE_LIB = r"B8&WM#YXQO{}[]()I1i!pao;:,.    "
        count = len(CODE_LIB)
        image_file = image_file.convert("L")
        code_pic = ''
        for h in range(0, image_file.size[1]):
            for w in range(0, image_file.size[0]):
                gray = image_file.getpixel((w,h))
                code_pic = code_pic + CODE_LIB[int(((count-1)*gray)/256)]
            code_pic += "\n"
        with open(datapath, 'w+') as file:
            file.write(code_pic)
            with io.BytesIO() as image_binary:
                text_image(datapath).save(image_binary, format='PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))


def setup(client):
    client.add_cog(AsciiArt(client))



def text_image(text_path, font_path=None):
    """Convert text file to a grayscale image with black characters on a white background.

    arguments:
    text_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    grayscale = 'L'
    # parse the file into lines
    with open(text_path) as text_file:  # can throw FileNotFoundError
        lines = tuple(l.rstrip() for l in text_file.readlines())

    # choose a font (you can see more detail in my library on github)
    large_font = 20  # get better resolution with larger size
    font_path = font_path or 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    # make the background image based on the combination of font and lines
    pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # max height is adjusted down because it's too large visually for spacing
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    # crop the text
    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image
