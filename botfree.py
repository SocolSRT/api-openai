import discord
import openai
import os
import asyncio
# Set up Discord client and OpenAI API key
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
os.environ['OPENAI_API_KEY'] = 'THE-KEY-TO-YOUR-API-OPENAI' # Paste your OpenAI API key here
openai.api_key = os.environ['OPENAI_API_KEY']
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Activity(name = f'$q text | $i image', type = discord.ActivityType.playing))
    print(f'{client.user} has connected to Discord!')
# Define command prefix
PREFIX = '$'
# Keep track of processed users
processed_users = {}
# Respond to messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(PREFIX):
        # Get command and argument
        command = message.content.split()[0][1:]
        arg = ' '.join(message.content.split()[1:])
        # Check user and message length limits
        if message.author.id in processed_users:
            await message.channel.send(f"{message.author.mention}, you have already made a request. Please wait for a response before making another one.")
            return
        if len(arg) > 1000:
            await message.channel.send(f"{message.author.mention}, your request is too long. Please limit your request to 1000 characters or less.")
            return
        # Process request
        if command == 'q':
            # Answer a question
            response = openai.Completion.create(
                engine='text-davinci-002',
                prompt=f'Q: {arg}\nA:',
                max_tokens=1024,
                n=1,
                stop='A:',
                temperature=0.5
            )
            await message.channel.send(f"{message.author.mention}\n" + response.choices[0].text)
        elif command == 'i':
            # Generate an image
            response = openai.Image.create(
                model='image-alpha-001',
                prompt=arg,
                size='512x512'
            )
            # Send all image URLs
            for image_data in response.data:
                await message.channel.send(f"{message.author.mention}\n" + image_data.url)
        # Mark user as processed
        processed_users[message.author.id] = True
        # Remove user from processed list after 10 sec
        await asyncio.sleep(10)
        try:
            processed_users.pop(message.author.id)
        except KeyError:
            pass
# Run the bot
client.run('TOKEN-FROM-YOUR-DISCORD-BOT') # Paste your Discord token here