# Imports
import requests
import time
import discord
import datetime
import pytz
from os import getenv
from discord.ext import commands

set(pytz.all_timezones_set)
# Set Prefix
client = commands.Bot(command_prefix = '!')

# To send message with the bot (for the bot can to update the message)
@client.command()
@commands.has_permissions(administrator = True)
async def embed(ctx):
  await ctx.channel.purge(limit=1)
  embed = discord.Embed(
    colour = discord.Colour.blue(),
    title = f'Embed'
  )
  await ctx.send(embed=embed)

# Setting variables **U need change this**
IP = getenv('server_ip')
TOKEN = getenv('DISCORD_BOT_TOKEN')
server_name = getenv('server_name')
channel_id = getenv('channel_id')


# Send when the bot in online
@client.event
async def on_ready():
   print(f'Logged as {client.user.name}')
   client.loop.create_task(players())

# Update a message and status every minute
async def players():
  
  while True:

    chn_id = channel_id
    
    try:
      # Players Information
      x = requests.get(f'http://139.99.125.178:30120/players.json')
      info = x.json()
      # Server Information 
      p = requests.get(f'http://139.99.125.178:30120/dynamic.json')
      server = p.json()
      # maxPlayers & Players
      players, maxPlayers = server['clients'], server['sv_maxclients']
      # Players list 
      playernames = ''
      for player in info:
        playernames += f"[{player['id']}] `{player['name']}` {player['ping']}ms"

        for info in player['identifiers']:
          if 'discord' in info:
            playernames += f' <@{info[8:]}>\n'
 
      # Embed 
      if players < 75:
          chn = client.get_channel(983271665477779466)
          tz = pytz.timezone('Asia/Colombo')
          ct = datetime.datetime.now(tz=tz).strftime('%d/%m/%Y %H:%M:%S')
          embed = discord.Embed(
            colour = discord.Colour.blue(),
            title = f'Status: {players}/{maxPlayers} \n{ct}',
            description= playernames
          )
          embed.timestamp = datetime.datetime.now()
          embed.set_footer(text= f'© {server_name} • ( {players}/{maxPlayers} )')
          await chn.send(embed=embed)
      else:
          text1 = x = "\n".join(playernames.split("\n")[:70])
          text2 = x = "\n".join(playernames.split("\n")[70:])
          chn = client.get_channel(983271665477779466)
          tz = pytz.timezone('Asia/Colombo')
          ct = datetime.datetime.now(tz=tz).strftime('%d/%m/%Y %H:%M:%S')
          embed = discord.Embed(
            colour = discord.Colour.blue(),
            title = f'Status: {players}/{maxPlayers} \n{ct}',
            description= text1
          )
          await chn.send(embed=embed)
          chn = client.get_channel(983271665477779466)
          embed = discord.Embed(
            colour = discord.Colour.blue(),
            description= text2
          )
          embed.timestamp = datetime.datetime.now()
          embed.set_footer(text= f'© {server_name} • ( {players}/{maxPlayers} )')
          await chn.send(embed=embed)
                
    except:
      chn = client.get_channel(983271665477779466)
      embed = discord.Embed(
        colour = discord.Colour.red(),
        title = f'Status: Offline',
      )
      embed.timestamp = datetime.datetime.now()
      embed.set_footer(text= f'© {server_name} ')
      await chn.send(embed=embed)

    # Update every minute (60 seconds)
    time.sleep(120)

# Run the bot
client.run(TOKEN)
