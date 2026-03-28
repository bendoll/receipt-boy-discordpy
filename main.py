# import deps
import os
import discord
import requests
from dotenv import load_dotenv
from escpos.printer import Network
from PIL import Image
from io import BytesIO

# load config from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
PRINTER_IP = os.getenv("PRINTER_IP")
PRINTER_PORT = int(os.getenv("PRINTER_PORT", 9100))

# discord stuff
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# printer stuff
def get_printer():
    return Network(PRINTER_IP, port=PRINTER_PORT)

def print_text(content, author):
    printer = get_printer()
    printer.set(align='left', bold=True)
    printer.text(f"{author}\n")
    printer.set(bold=False)
    printer.text(content + "\n\n")
    printer.cut()

def print_image_from_url(url):
    printer = get_printer()
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    # force resize image to printer width
    target_width = 576
    img = img.resize((target_width, int(img.height * target_width / img.width)))

    # convert image to monochrome
    img = img.convert("L")
    img = img.point(lambda x: 0 if x < 128 else 255, '1')

    printer.image(img)

    # add 8 newlines of feed (roughly 20mm)
    printer.text("\n" * 8)
    printer.cut()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID:
        return

    if message.author.bot:
        return
    
    # print message text
    if message.content:
        print_text(message.content, message.author.name)

    # print image attachment
    for attachment in message.attachments:
        if attachment.content_type and attachment.content_type.startswith("image"):
            print_image_from_url(attachment.url)

client.run(TOKEN)