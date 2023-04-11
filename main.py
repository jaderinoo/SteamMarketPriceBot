import keys
import itemlist

import json
import requests
import discord

from pathlib import Path
from datetime import date

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
    embed = discord.Embed(title="Tyloo Price Bot", description=str(date.today()), color=0xf8d91c)
    newData = []
    old_values = {}
    boolFile = Path('priceData.json').is_file()

    if boolFile:
        with open('priceData.json', 'r') as openfile:
            old_values = json.load(openfile)
    
    for idx, item in enumerate(itemlist.itemList):
        response = requests.get(f'https://steamcommunity.com/market/priceoverview/?appid={item["AppID"]}&currency=1&market_hash_name={item["HashedName"]}')
        jsonresponse = response.json()
        currentItem = {}

        medianPrice = "N/A" 
        vol = "N/A"
        percentChange = "N/A"
        symbol = ""
        
        if 'median_price' in jsonresponse:
            medianPrice = jsonresponse["median_price"]
            medianPrice = float(medianPrice.replace('$',''))
            
            # Percentage change based off last run
            if boolFile:
                if old_values[idx]['Name'] == item['Name'] and old_values[idx]['medianPrice'] != "N/A":
                    previousPrice = float(old_values[idx]['medianPrice'])
                    percentChange = round((abs(medianPrice - previousPrice) / previousPrice) * 100.0, 2)
                    if medianPrice > previousPrice:
                        symbol = "+"
                    elif medianPrice < previousPrice:
                        symbol = "-"

        if 'volume' in jsonresponse:
            vol = jsonresponse["volume"]

        currentItem['Name'] = item["Name"]
        currentItem['Date'] = str(date.today())
        currentItem['medianPrice'] = medianPrice
        currentItem['vol'] = vol

        embed.add_field(name=item["Name"], value=f'Median Price - ${medianPrice} ({symbol}{percentChange}%) \t|\t 24hr Vol - {vol} \n', inline=False)        
        newData.append(currentItem)

    # Send message
    await channel.send(embed=embed)

    # Save data to json file
    with open("priceData.json", "w") as outfile:
        jsonDump = json.dumps(newData, indent=4)
        outfile.write(jsonDump)

    await client.close()

client.run(TOKEN)