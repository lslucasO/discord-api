import discord
from discord.ext import commands
from discord import app_commands


class Buttons(discord.ui.View):
    
    @discord.ui.button(label="Adicionar Tarefa", emoji="📚",style=discord.ButtonStyle.success)
    async def adicionar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        self.adicionar_lista = await interaction.channel.send("Digite a tarefa que deseja adicionar a sua lista")
        self.tarefa = await interaction.client.wait_for("message")

        self.tarefas_file = open(f"./database/Tarefas/{interaction.user.name}.txt", "a")
        self.msg = self.tarefa.content
        self.tarefas_file.write(f"> {self.msg.capitalize()}\n")
        
        self.tarefas_file = open(f"./database/Tarefas/{interaction.user.name}.txt", "r")
        
        
        embed_Titulo = discord.Embed(title=f"Sua Lista de Tarefas", description="Perfeito para monitorar e controlar suas atividades!", color=discord.Color.green())
        embed_Titulo.set_thumbnail(url=interaction.user.avatar.url)
        embed_Tarefas = discord.Embed(title=f":blue_book: Atividades de @{interaction.user.name.capitalize()}", description=f"Voce pode adicionar, remover e gerenciar por este embed", color=discord.Color.blurple())
        embed_Tarefas.add_field(inline=True, name=f"Lista a cumprir:\n", value=f"\n{self.tarefas_file.read()}")
        embed_Tarefas.add_field(inline=True, name=f"Já completadas:\n", value=f"")
        embeds = [embed_Titulo, embed_Tarefas]
        self.view = Buttons()
        
        self.add = await interaction.channel.send("Sua tarefa está sendo **adicionada**...")
        self.msg_list = [self.tarefa, self.adicionar_lista, self.add]
        await interaction.delete_original_response()
        await interaction.channel.delete_messages(messages=self.msg_list)
        await interaction.channel.send(embeds=embeds, view=self.view)
        


    @discord.ui.button(label="Remover Tarefa", emoji="🔧",style=discord.ButtonStyle.danger)
    async def remover_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        self.msg1 = await interaction.channel.send("Qual tarefa você deseja remover?")
        self.tarefa_remover = await interaction.client.wait_for("message")
        
        self.check = []
        self.tarefas_list = []
        
        
        with open(f"./database/Tarefas/{interaction.user.name}.txt", "r") as arquivo:
            for tarefa in arquivo:
                self.tarefas_list.append(tarefa[2:-1])
                
        
        
        if self.tarefa_remover.content.capitalize() in self.tarefas_list:
            
            self.tarefas_file = open(f"./database/Tarefas/{interaction.user.name}.txt", "r")
            self.tarefas_list.remove(self.tarefa_remover.content.capitalize())
            
            with open(f"./database/Tarefas/{interaction.user.name}.txt", "w") as arquivo:
                for item in self.tarefas_list:
                    arquivo.write(f"> {item}\n")
            
            embed_Titulo = discord.Embed(title=f"Sua Lista de Tarefas", description="Perfeito para monitorar e controlar suas atividades!", color=discord.Color.green())
            embed_Titulo.set_thumbnail(url=interaction.user.avatar.url)
            embed_Tarefas = discord.Embed(title=f":blue_book: Atividades de @{interaction.user.name.capitalize()}", description=f"Voce pode adicionar, remover e gerenciar por este embed", color=discord.Color.blurple())
            
            if len(self.tarefas_list) == 0:
                embed_Tarefas.add_field(inline=True, name=f"Você ainda não possui tarefas", value="")
            else:
                embed_Tarefas.add_field(inline=True, name=f"Lista a cumprir:", value=f"\n{self.tarefas_file.read()}")
                embed_Tarefas.add_field(inline=True, name=f"Já completadas:", value=f"")
        
        
            embeds = [embed_Titulo, embed_Tarefas]
            self.view = Buttons()
            
            self.remove = await interaction.channel.send("Sua tarefa está sendo **removida**...")
            self.msg_list = [self.msg1, self.tarefa_remover, self.remove]
            await interaction.delete_original_response()
            await interaction.channel.delete_messages(messages=self.msg_list)
            await interaction.channel.send(embeds=embeds, view=self.view)
            
        else:
            
            await interaction.followup.send("Essa tarefa não faz parte da sua lista!", ephemeral=True)

     
        
class ListadeTarefas(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @app_commands.command(name="lista-de-tarefas", description="Mostra os seus afazeres")
    async def tarefas(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        
        self.content = []
        self.aviso = ""
        self.fazer = open(f"./database/Tarefas/{interaction.user.name}.txt", "a")
        self.fazer = open(f"./database/Tarefas/{interaction.user.name}.txt", "r")
        
        
        embed_Titulo = discord.Embed(title=f"Sua Lista de Tarefas", description="Perfeito para monitorar e controlar suas atividades!", color=discord.Color.green())
        embed_Titulo.set_thumbnail(url=interaction.user.avatar.url)
        embed_Tarefas = discord.Embed(title=f":blue_book: Atividades de @{interaction.user.name.capitalize()}", description=f"Voce pode adicionar, remover e gerenciar por este embed", color=discord.Color.blurple())
        
        with open(f"./database/Tarefas/{interaction.user.name}.txt", "r") as arquivo:
            for item in arquivo:
                self.content.append(item)
                
        if len(self.content) == 0:
            embed_Tarefas.add_field(inline=True, name=f"Você ainda não possui tarefas", value="")
        else:
            embed_Tarefas.add_field(inline=True, name=f"Lista a cumprir:", value=f"\n{self.fazer.read()}")
            embed_Tarefas.add_field(inline=True, name=f"Já completadas:", value=f"")
        
        
        embeds = [embed_Titulo, embed_Tarefas]
        
        self.view = Buttons()
        
        await interaction.followup.send(embeds=embeds, view=self.view)
           

async def setup(client):
    await client.add_cog(ListadeTarefas(client))