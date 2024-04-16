import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials

client = discord.Client();

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client_gs = gspread.authorize(creds)
sheet = client_gs.open('Financial Inflows').sheet1

@client.event
async def on_message(message):
    if message.channel.name == 'new-billings' and message.content.startswith('Descrição:'):
        try:
            lines = message.content.split('\n')
            description = lines[0].split(':')[1].strip()
            date = lines[1].split(':')[1].strip()
            value = lines[2].split(':')[1].strip()
            responsor = lines[3].split(':')[1].strip()

            # Inserir na planilha
            next_row = len(sheet.get_all_values()) + 1
            sheet.insert_row([description, date, value, responsor, 'FALSE'], next_row)
            await message.channel.send("Conta adicionada com sucesso!")
        except Exception as e:
            await message.channel.send(f"Erro ao adicionar conta: {str(e)}")

client.run('your_discord_bot_token')