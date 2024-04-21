import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Configura os intents
intents = discord.Intents.all()

# Cria o bot com os intents configurados
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready!")
    guild_count = 0  # Inicializa o contador de servidores

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1  # Incrementa o contador para cada guilda

    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

@bot.event
async def on_message(message):
    if message.content == 'hello':
        print(message.chaneel.name)
        await message.channel.send("hello world")
    
    # Isso é necessário para processar comandos se você sobrescrever o evento on_message
    await bot.process_commands(message)


bot.run(DISCORD_TOKEN)
