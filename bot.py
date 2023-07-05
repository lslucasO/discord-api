import discord, os, asyncio, random
from discord.ext import commands
from key import DISCORD_API_TOKEN

intents = discord.Intents.default()
intents.message_content = True 
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"{client.user.name} is connected!")
    

@client.command()
async def teste(ctx):
    await ctx.send("teste")
    
@client.event
async def on_message(msg):
    
    sanchez = 240872587566120971
    if msg.author.id == sanchez:
        f = open(f"database/Obs/{msg.author.name}.txt", "a")
        f.write(f"{msg.content}\n")
    else:
        pass


async def load():   
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await client.load_extension(f'commands.{filename[:-3]}')
            print(f'{filename} is ready!')


async def main():
    async with client:
        await load()
        await client.start(DISCORD_API_TOKEN)


asyncio.run(main()) 