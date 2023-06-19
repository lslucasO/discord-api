import discord, os, asyncio
from discord.ext import commands
from key import DISCORD_API_TOKEN

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_ready(ctx):
    await client.tree.sync()
    print(f"{client.user.name} is connected!")


@client.command()
async def teste(ctx):
    await ctx.send("Working!")


async def load():   
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'{filename} is ready!')


async def main():
    async with client:
        await load()
        await client.start(DISCORD_API_TOKEN)


asyncio.run(main()) 