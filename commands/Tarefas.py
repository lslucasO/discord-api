import discord
from discord.ext import commands
from discord import app_commands


class ListadeTarefas(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @app_commands.command(name="lista-de-tarefas", description="Mostra os seus afazeres")
    async def tarefas(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        tarefas_file = open("./database/Tarefas/tarefas.txt", "r")
        
        embed_Titulo = discord.Embed(title=f"Sua Lista de Tarefas", description="Perfeito para monitorar e controlar suas atividades!", color=discord.Color.green())
        embed_Titulo.set_thumbnail(url=interaction.client.guilds[0].icon.url)
        
        embed_Tarefas = discord.Embed(title=f":blue_book: Atividades de {interaction.user.name}", description=f"Voce pode adicionar, remover e gerenciar por este embed", color=discord.Color.blurple())
        embed_Tarefas.add_field(name="", value="1.\n")
        embeds = [embed_Titulo, embed_Tarefas]
        
        await interaction.followup.send(embeds=embeds)
        
        

async def setup(client):
    await client.add_cog(ListadeTarefas(client))