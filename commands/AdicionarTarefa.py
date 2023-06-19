import discord
from discord.ext import commands
from discord import app_commands


class AdicionarTarefa(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    pass
        
        
async def setup(client):
    await client.add_cog(AdicionarTarefa(client))