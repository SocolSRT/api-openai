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
# Read user request counts from file
def read_user_requests():
    with open('users.txt') as f:
        user_requests = {}
        for line in f:
            user_id, requests = line.strip().split()
            user_requests[int(user_id)] = int(requests)
        return user_requests
# Write user request counts to file
def write_user_requests(user_requests):
    with open('users.txt', 'w') as f:
        for user_id, requests in user_requests.items():
            f.write(f'{user_id} {requests}\n')
# Keep track of processed users
processed_users = set()
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
        # Check user request count
        user_requests = read_user_requests()
        if message.author.id not in user_requests:
            await message.channel.send(f"{message.author.mention}, you do not have any requests remaining.")
            return
        if user_requests[message.author.id] == 0:
            del user_requests[message.author.id]
            write_user_requests(user_requests)
            await message.channel.send(f"{message.author.mention}, you have used all of your requests.")
            return
        # Process request
        if command == 'q':
            # Answer a question
            response = openai.Completion.create(
                engine='text-davinci-003',
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
                prompt=arg,
                size='1024x1024'
            )
            # Send all image URLs
            for image_data in response.data:
                await message.channel.send(f"{message.author.mention}\n" + image_data.url)
        # Decrement user request count
        user_requests[message.author.id] -= 1
        write_user_requests(user_requests)
        # Mark user as processed
        processed_users.add(message.author.id)
        # Remove user from processed list after 10 sec
        await asyncio.sleep(10)
        processed_users.remove(message.author.id)
# Run the bot
client.run('TOKEN-FROM-YOUR-DISCORD-BOT') # Paste your Discord token here