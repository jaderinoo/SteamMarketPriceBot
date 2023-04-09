import keys
import itemlist

import requests
import discord

TOKEN = keys.DISCORD_TOKEN
SERVER = keys.SERVER

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == SERVER:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    channel = client.get_channel(keys.CHANNEL)
    parsedMessage = ''
    for item in itemlist.itemList:
        response = requests.get(f'https://steamcommunity.com/market/priceoverview/?appid={item["AppID"]}&currency=1&market_hash_name={item["HashedName"]}')
        jsonresponse = response.json()

        medianPrice = "N/A" 
        vol = "N/A"
        
        if 'median_price' in jsonresponse:
            medianPrice = jsonresponse["median_price"]

        if 'volume' in jsonresponse:
            vol = jsonresponse["volume"]
        
        parsedMessage += f'{item["Name"]} \t|\t Median Price - {medianPrice} \t|\t 24hr Vol - {vol} \n'
        
    # Send message
    await channel.send(parsedMessage)

    await client.close()

client.run(TOKEN)