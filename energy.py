import discord
import asyncio
import key
import logging
import random

asyncio.get_event_loop().set_debug(True)
# logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG)

import discordmarkov as dm
from load_skype import SM as skype_markov
from person_defs import person_defs

import datetime as dt

client = discord.Client()
lock = asyncio.Lock()
voice_client = None
player = None

discord_markov = dm.DiscordMarkov(skype_markov, person_defs)
upd_date = dt.datetime.now()

def shutdown_voice():
  global voice_client, player
  print("shutting down voice")
  if voice_client is not None:
    loop = asyncio.get_event_loop()
    print("disconnecting client")
    asyncio.run_coroutine_threadsafe(voice_client.disconnect(), loop)
    # loop.close()
    #  voice_client.disconnect()
    voice_client = None
  player = None
  print("client disconnected")
  
async def read_logs(after=dt.datetime.min):
  global upd_date
  i = 0
  upd_date = dt.datetime.now()
  for channel in client.get_all_channels():
    async for log in client.logs_from(channel, limit=9999999, before=upd_date, after=after):
      discord_markov.update(log.author.id, log.content)
      i += 1
  print('done reading log, %d messages' % i)
  
async def gamestats(channel, name):
  tmp = await client.send_message(channel, 'Analyzing game stats for user %s.' % name)
  await asyncio.sleep(.5)
  await client.edit_message(tmp, 'Analyzing game stats for user %s..' % name)
  await asyncio.sleep(.5)
  await client.edit_message(tmp, 'Analyzing game stats for user %s...' % name)
  await asyncio.sleep(.5)
  await client.edit_message(tmp, 'Analyzing game stats for user %s....' % name)
  await asyncio.sleep(.5)
  await client.edit_message(tmp, 'Analyzing game stats for user %s.....' % name)
  await asyncio.sleep(.5)
  await client.send_message(channel, 'Analysis complete.')
  
  if name == 'enzo_d':
    await client.send_message(channel, 'User %s is Pro as Fuck.' % name)
  else:
    await client.send_message(channel, 'User %s is a noob.' % name)

async def energy(channel, voice_channel, lock):
  global voice_client, client, player
  await client.send_message(channel, '<:energygap:263306701120208907>')
  
  member_voice_channel = voice_channel
  if member_voice_channel is not None:
    await lock
    try:
      if voice_client is None:
        voice_client = await client.join_voice_channel(member_voice_channel)
        print("joined voice channel")
      elif voice_client.channel is not member_voice_channel:
        print("already in voice channel, but caller is in different voice channel")
      
      if (player is not None and not player.is_playing()) or (player is None):
        player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=qnIpG7E3eOQ', after= shutdown_voice)
        print("ytdl player created")
        player.start()
        print("player started")
    finally:
      lock.release()

async def stop_energy(lock):
  global player
  await lock
  try:
    if player is not None:
      player.stop()
  finally:
    lock.release()
    
@client.event
async def on_ready():
    global upd_date
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    asyncio.ensure_future(read_logs())
    
@client.event
async def on_message(message):
    global lock, voice_client, upd_date
    if message.author.id != client.user.id:
          
      if 'energy' in message.content:
        asyncio.ensure_future(energy(message.channel, message.author.voice.voice_channel, lock))
      elif 'stop' in message.content:
        asyncio.ensure_future(stop_energy(lock))
      elif message.content.startswith('-gamestats'):
        asyncio.ensure_future(gamestats(message.channel, message.author.name))
      elif message.content.startswith('-fakeme'):
        
        tmp = await client.send_message(message.channel, 'Impersonating...')
        
        args = message.content.split(' ')
        
        asyncio.ensure_future(read_logs(upd_date))
        
        if len(args) == 1:
          mgens = [discord_markov.generate(discord_id=message.author.id)]
        elif len(args) > 1 and not args[1].isdigit():
          if len(args) > 2 and args[2].isdigit():
            num_msg = min(int(args[2]), 20)
          else:
            num_msg = 1
            
          mgens = []
          for member in client.get_all_members():
            if (member.nick is not None and member.nick == args[1]) or member.name == args[1]:
              mgen = discord_markov.generate(discord_id=member.id, num_msg=num_msg)
              mgens.append(mgen)
            
        elif args[1].isdigit():
          mgens = [discord_markov.generate(num_msg=min(int(args[1]), 20))]
        else:
          mgens = [discord_markov.generate()]
        
        smsg = ''
        for nname, nmsg in mgens[random.randrange(len(mgens))]:
          str_name = await client.get_user_info(nname)
          smsg += "%s: %s\n" % (str_name.name, nmsg)
          await client.edit_message(tmp, smsg)

client.run(key.secret)