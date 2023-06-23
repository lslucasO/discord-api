import discord, requests, random, asyncio
from discord.ext import commands
from discord import app_commands


class Filtro(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @app_commands.command(name="filtrar-anime", description="muda o filtro da pesquisa dos animes por genero")
    @app_commands.choices(genero=[
        discord.app_commands.Choice(name="Comedy", value=1),
        discord.app_commands.Choice(name="Adventure", value=2),
        discord.app_commands.Choice(name="Action", value=3),
        discord.app_commands.Choice(name="Romance", value=4),
        discord.app_commands.Choice(name="Fantasy", value=5),
    ])
    async def filtrar(self, interaction: discord.Interaction, genero: discord.app_commands.Choice[int]):
        await interaction.response.defer()
        await interaction.followup.send(f"{interaction.user.mention} Filtro alterado para **{genero.name}**")
        
async def setup(client):
    await client.add_cog(Filtro(client))