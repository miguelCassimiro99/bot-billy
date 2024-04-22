import os
from dotenv import load_dotenv
import discord
import base64
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

encoded_cred = os.getenv('GOOGLE_CREDENTIALS_BASE')
decoded_cred = base64.b64decode(encoded_cred)
credentials_json = json.loads(decoded_cred)
# GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON');

intents = discord.Intents.all()
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
        print(message.channel.name)
        await message.channel.send("hello world")
    
    await bot.process_commands(message)


@bot.command(name='inflow')
async def update_spreadsheet(ctx):
    message = ctx.message.content
    try:
        lines = message.split('\n')
        if len(lines) < 4:
            await ctx.send("Formato da mensagem incorreto. Certifique-se de incluir descrição, data, valor e responsável.")
            return

        description_line = lines[1].split(': ', 1)
        date_line = lines[2].split(': ', 1)
        value_line = lines[3].split(': ', 1)
        responsor_line = lines[4].split(': ', 1)

        if len(description_line) < 2 or len(date_line) < 2 or len(value_line) < 2 or len(responsor_line) < 2:
            await ctx.send("Erro na formatação de uma das linhas. Cada linha deve conter um ':' seguido de um espaço.")
            return

        description = description_line[1].strip()
        date = date_line[1].strip()
        value = value_line[1].strip().replace('R$', '').replace('.', '').replace(',', '.')
        value = float(value)  # Convertendo o valor para float
        responsor = responsor_line[1].strip()
        is_paid = False  # Usando valor booleano

        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
        client_gs = gspread.authorize(creds)
        sheet = client_gs.open('financial_inflows_auto').sheet1

        next_row = len(sheet.get_all_values()) + 1
        sheet.insert_row([description, date, value, responsor, is_paid], next_row)
        await ctx.send('Conta adicionada com sucesso!')
        
    except Exception as e:
        print(e)
        await ctx.send(f'Erro ao adicionar conta: {str(e)}')


bot.run(DISCORD_TOKEN)
