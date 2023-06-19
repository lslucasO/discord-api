import discord
from discord.ext import commands
from discord import app_commands


class Buttons(discord.ui.View):
    
    @discord.ui.button(label="Adicionar tarefa", emoji="📚",style=discord.ButtonStyle.success)
    async def adicionar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        self.adicionar_lista = await interaction.channel.send("Digite a tarefa que deseja adicionar a sua lista")
        self.tarefa = await interaction.client.wait_for("message")

        self.tarefas_file = open("./database/Tarefas/tarefas.txt", "a")
        self.msg = self.tarefa.content
        self.emoji_tarefa_fazer = ":white_large_square:"
        self.tarefas_file.write(f"{self.emoji_tarefa_fazer} {self.msg.capitalize()}\n")
        
        self.tarefas_file = open("./database/Tarefas/tarefas.txt", "r")
        
        
        embed_Titulo = discord.Embed(title=f"Sua Lista de Tarefas", description="Perfeito para monitorar e controlar suas atividades!", color=discord.Color.green())
        embed_Titulo.set_thumbnail(url=interaction.client.guilds[0].icon.url)
        embed_Tarefas = discord.Embed(title=f":blue_book: Atividades de @{interaction.user.name.capitalize()}", description=f"Voce pode adicionar, remover e gerenciar por este embed", color=discord.Color.blurple())
        embed_Tarefas.add_field(inline=True, name=f"Lista a cumprir:\n", value=f"\n{self.tarefas_file.read()}")
        embed_Tarefas.add_field(inline=True, name=f"Já completadas:\n", value=f"")
        embeds = [embed_Titulo, embed_Tarefas]
        self.view = Buttons()
        
        self.add = await interaction.channel.send("Sua tarefa está sendo adicionada...")
        self.msg_list = [self.tarefa, self.adicionar_lista, self.add]
        await interaction.delete_original_response()
        await interaction.channel.delete_messages(messages=self.msg_list)
        await interaction.channel.send(embeds=embeds, view=self.view)
        


    @discord.ui.button(label="Remover tarefa", emoji="🔧",style=discord.ButtonStyle.danger)
    async def remover_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        
        await interaction.followup.send("In progress")
        
        
class ListadeTarefas(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @app_commands.command(name="lista-de-tarefas", description="Mostra os seus afazeres")
    async def tarefas(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        self.content = []
        self.aviso = ""
        self.fazer = open("./database/Tarefas/tarefas.txt", "a")
        self.fazer = open("./database/Tarefas/tarefas.txt", "r")
        
        
        embed_Titulo = discord.Embed(title=f"Sua Lista de Tarefas", description="Perfeito para monitorar e controlar suas atividades!", color=discord.Color.green())
        embed_Titulo.set_thumbnail(url=interaction.client.guilds[0].icon.url)
        embed_Tarefas = discord.Embed(title=f":blue_book: Atividades de @{interaction.user.name.capitalize()}", description=f"Voce pode adicionar, remover e gerenciar por este embed", color=discord.Color.blurple())
        
        with open("./database/Tarefas/tarefas.txt", "r") as arquivo:
            for item in arquivo:
                self.content.append(item)
                
        if len(self.content) == 0:
            embed_Tarefas.add_field(inline=True, name=f"Você ainda não possui tarefas, adicione algumas!", value="")
            embed_Tarefas.add_field(inline=True, name=f"Já completadas:", value=f"")
        else:
            embed_Tarefas.add_field(inline=True, name=f"Lista a cumprir:", value=f"\n{self.fazer.read()}")
            embed_Tarefas.add_field(inline=True, name=f"Já completadas:", value=f"")
        
        
        embeds = [embed_Titulo, embed_Tarefas]
        
        self.view = Buttons()
        
        await interaction.followup.send(embeds=embeds, view=self.view)
           

async def setup(client):
    await client.add_cog(ListadeTarefas(client))