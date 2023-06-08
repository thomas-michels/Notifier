import discord
import os
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

url = 'http://localhost:5005/webhooks/rest/webhook'

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$rasa'):
        content_message = message.content.replace("$rasa ", "")
        if content_message == "ping":
            await message.channel.send("pong")

        else:
            raw_message = {
                'sender': message.author.name,
                'message': content_message
            }

            response = requests.post(url, json=raw_message)

            # Obter a resposta do chatbot
            bot_responses = response.json()

            # Exibir as respostas do chatbot
            for bot_response in bot_responses:
                await message.channel.send(bot_response['text'])
        

client.run(os.getenv("TOKEN"))
