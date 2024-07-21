from steam import Steam
from decouple import config
KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # botin tietoisuuden testaus
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')
        
    # Komennolla haetaan käyttäjän pelitietoja counter-strikestä
    # historiana se, että pohdittiin kaverin kanssa päivittyykö pelaajien statistiikat (eliminaatiot, pelatut kartat lkm, kuolemat, yms)
    # matsin aikana, ja jos ei, niin kuinka pitkä tilastojen päivittymisen viive on
    # selvisi että matsin jälkeen joku varttinen niin alettiin huomaamaan lukueroja
    if message.content.startswith('!cs'):
        
        # käyttäjän ID, muotoa esim "76561197960287930"
        # parempi olisi jos voisi ihan käyttäjänimen perusteella hakea,
        # mutta teki tehtävänsä siinä pohdiskelun tilassa
        user = message.content.split()[1]
    
        # haettavan tilaston avain sana,
        # esimerkiksi:
        # '!cs 12345 ak47' -> tulostuta steamID64:n 12345 omaavan tilastot, jotka sisältävät avainsanan "ak47" 
        # avainsanoja voi antaa monta, esim:
        # '!cs 12345 vertigo eliminations' -> palautteena tilastot joissa vertigo ja eliminaatiot mainittu
        params = message.content.split()[2:]
        
        # 730 = counter striken ID steamissa
        user_data = steam.apps.get_user_stats(user, 730)

        stats_in_string = ""
        for statistic in user_data["playerstats"]["stats"]:
            yes = True
            for stat in params:
                if stat not in statistic["name"]:
                    yes = False
            if yes:
                stats_in_string += statistic["name"] + " = " + str(statistic["value"]) + "\n"
        
        await message.channel.send(stats_in_string)

client.run('get_your_own_token')
