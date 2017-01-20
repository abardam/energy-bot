import discord
import asyncio
import key

client = discord.Client()
lock = asyncio.Lock()
voice_client = None
player = None

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
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    global lock, voice_client, player
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

client.run(key.secret)