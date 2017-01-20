import discord
import asyncio
import key

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
  if voice_client is not None:
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(voice_client.disconnect(), loop)
    # loop.close()
    #  voice_client.disconnect()
    voice_client = None
  player = None
  
@client.event
async def on_ready():
    global upd_date
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    upd_date = dt.datetime.now()
    for channel in client.get_all_channels():
      async for log in client.logs_from(channel, limit=9999999):
        discord_markov.update(log.author.id, log.content)
    print('done reading log')
@client.event
async def on_message(message):
    global lock, voice_client, player, upd_date
    if message.author.id != client.user.id:
          
      if 'energy' in message.content:
          await client.send_message(message.channel, '<:energygap:263306701120208907>')
          
          member_voice_channel = message.author.voice.voice_channel
          if member_voice_channel is not None:
            await lock
            try:
              voice_client = await client.join_voice_channel(member_voice_channel)
              player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=qnIpG7E3eOQ', after= shutdown_voice)
              player.start()
            finally:
              lock.release()
      elif 'stop' in message.content:
        await lock
        try:
          if player is not None:
            player.stop()
        finally:
          lock.release()
      elif message.content.startswith('-gamestats'):
        tmp = await client.send_message(message.channel, 'Analyzing game stats for user %s.' % message.author.name)
        await asyncio.sleep(.5)
        await client.edit_message(tmp, 'Analyzing game stats for user %s..' % message.author.name)
        await asyncio.sleep(.5)
        await client.edit_message(tmp, 'Analyzing game stats for user %s...' % message.author.name)
        await asyncio.sleep(.5)
        await client.edit_message(tmp, 'Analyzing game stats for user %s....' % message.author.name)
        await asyncio.sleep(.5)
        await client.edit_message(tmp, 'Analyzing game stats for user %s.....' % message.author.name)
        await asyncio.sleep(.5)
        await client.send_message(message.channel, 'Analysis complete.')
        
        if message.author.name == 'enzo_d':
          await client.send_message(message.channel, 'User %s is Pro as Fuck.' % message.author.name)
        else:
          await client.send_message(message.channel, 'User %s is a noob.' % message.author.name)
      elif message.content.startswith('-fakeme'):
        
        tmp = await client.send_message(message.channel, 'Impersonating...')
        
        args = message.content.split(' ')
        
        for channel in client.get_all_channels():
          g = client.logs_from(channel, limit=9999999, after=upd_date)
          upd_date = dt.datetime.now()
          async for log in g:
            discord_markov.update(log.author.id, log.content)
        
        if len(args) == 1:
          mgen = discord_markov.generate(discord_id=message.author.id)
        elif len(args) > 1 and not args[1].isdigit():
          if len(args) > 2 and args[2].isdigit():
            num_msg = min(int(args[2]), 50)
          else:
            num_msg = 1
            
          for member in client.get_all_members():
            brk = False
            if (member.nick is not None and member.nick == args[1]) or member.name == args[1]:
              mgen = discord_markov.generate(discord_id=member.id, num_msg=num_msg)
              brk = True
              break
            if not brk:
              mgen = discord_markov.generate()
            
        elif args[1].isdigit():
          mgen = discord_markov.generate(num_msg=min(int(args[1]), 10))
        else:
          mgen = discord_markov.generate()
        
        smsg = ''
        for nname, nmsg in mgen:
          str_name = await client.get_user_info(nname)
          smsg += "%s: %s\n" % (str_name.name, nmsg)
          await client.edit_message(tmp, smsg)

client.run(key.secret)