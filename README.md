# API OpenAI in Discord
This is an open-source Discord Bot written in Python using OpenAI API. It allows users to interact with OpenAI-powered AI services and perform various tasks such as natural language processing or create images. It is easy to use and integrate with existing Discord servers.


Paste your OpenAI API key here
> os.environ['OPENAI_API_KEY'] = 'THE-KEY-TO-YOUR-API-OPENAI'

Paste your Discord token here
> client.run('TOKEN-FROM-YOUR-DISCORD-BOT')

# botfree.py
Version where all users can use the bot

# botprivate.py
Version where only users from file users.txt can use the bot

Example file users.txt:
```
USER-ID-DISCORD NUMBER-AVAILABLE-REQUESTS
123456789 50
```

# It has 2 built-in limiters to protect against abuse of the system
Custom query size limiter (number of characters 1000)
> if len(arg) > 1000:

Limiting the rate of sending requests (1 request per 10 seconds)
> await asyncio.sleep(10)

# Would you like to support me financially?
* My Bitcoin wallet - *14AA4FAdUYnTVTx5pSQjq2h8UJoA8Na89R*
* My Litecoin wallet - *MSevKqUirTvQTkGxYechhNmBgAtDiZJq2x*
