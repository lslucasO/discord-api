import discord
from discord.ext import commands
from discord import app_commands


class Buttons(discord.ui.View):
    
    @discord.ui.button(label="Adicionar tarefa", emoji="📚",style=discord.ButtonStyle.success)
    async def adicionar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        await interaction.channel.send("Digite a tarefa que deseja adicionar a sua lista, use `+` no inicio")
        
        self.tarefa = await interaction.client.wait_for("message")
        
        
        await interaction.channel.send(f"Tarefa adicionada!")
       
        
        

    @discord.ui.button(label="Remover tarefa", emoji="🔧",style=discord.ButtonStyle.danger)
    async def remover_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        await interaction.followup.send("teste")
        
        
class ListadeTarefas(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    
        
    @app_commands.command(name="lista-de-tarefas", description="Mostra os seus afazeres")
    async def tarefas(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        
       
        
        embed_Titulo = discord.Embed(title=f"Sua Lista de Tarefas", description="Perfeito para monitorar e controlar suas atividades!", color=discord.Color.green())
        embed_Titulo.set_thumbnail(url=interaction.client.guilds[0].icon.url)
        
        embed_Tarefas = discord.Embed(title=f":blue_book: Atividades de @{interaction.user.name.capitalize()}", description=f"Voce pode adicionar, remover e gerenciar por este embed", color=discord.Color.blurple())
        embed_Tarefas.add_field(name=f"A serem cumpridas:", value="")
        embeds = [embed_Titulo, embed_Tarefas]
        
        self.view = Buttons()
        
        await interaction.followup.send(embeds=embeds, view=self.view)
        
        

async def setup(client):
    await client.add_cog(ListadeTarefas(client))