import os
import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN');
GOOGLE_CREDENTIALS_JSON = os.getenv('GOOGLE_CREDENTIALS_JSON');

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_JSON, scope)
client_gs = gspread.authorize(creds)
sheet = client_gs.open('financial_inflows_auto').sheet1

intents = discord.Intents.all()
intents.messages = True  # Habilitar eventos de mensagens
intents.message_content = True  # Habilitar conteúdo de mensagens
intents.guilds = True  # Permitir eventos de guilds


bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command(name='inflow_test')
async def inflow_test(ctx):
    await ctx.send('Hello world')


@bot.event
async def on_message(message):
    print(f'Recebido: {message.content} de {message.author}')
    # Certifique-se de que o bot não responde às próprias mensagens
    if message.author == bot.user:
        return

    # Verificar se a mensagem é no canal correto
    if message.channel.name == "new-billings":
        # Extrair as informações da mensagem
        if message.content.startswith('Descrição:'):
            try:
                lines = message.content.split('\n')
                description = lines[0].split(': ', 1)[1].strip()
                date = lines[1].split(': ', 1)[1].strip()
                value = lines[2].split(': ', 1)[1].strip().replace('R$', '').replace(',', '.').strip()
                responsor = lines[3].split(': ', 1)[1].strip()
                is_paid = 'FALSE'

                # Inserir na planilha
                next_row = len(sheet.get_all_values()) + 1
                sheet.insert_row([description, date, value, responsor, is_paid], next_row)
                await message.channel.send('Conta adicionada com sucesso!')
                await bot.process_commands(message)
            except Exception as e:
                await message.channel.send(f'Erro ao adicionar conta: {str(e)}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado!")
    else:
        await ctx.send(f"Erro: {error}")


bot.run(DISCORD_TOKEN);