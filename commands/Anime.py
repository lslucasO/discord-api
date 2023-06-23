import discord, requests, random, asyncio
from discord.ext import commands
from discord import app_commands


       
def get_anime():
    anime_Database = requests.get(f"https://api.jikan.moe/v4/random/anime")
    anime_Database = anime_Database.json()
    
    
    
    while True:
        if anime_Database["data"]["score"] != None and anime_Database["data"]["synopsis"] != None and anime_Database["data"]["popularity"] <= 5000:
            break
        else:       
            anime_Database = requests.get(f"https://api.jikan.moe/v4/random/anime")
            anime_Database = anime_Database.json()
            print(anime_Database["data"]["title"]) 
    return anime_Database    


class Buttons(discord.ui.View):
    
    @discord.ui.button(label="", emoji="⏩",style=discord.ButtonStyle.blurple)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        self.anime_Database = get_anime()
        
        
        self.anime_Info_title = self.anime_Database["data"]["title"]
        self.anime_Info_link = self.anime_Database["data"]["url"]
        self.anime_Info_sinopse = self.anime_Database["data"]["synopsis"]
        self.anime_Info_score = self.anime_Database["data"]["score"]
        self.img = self.anime_Database["data"]["images"]["jpg"]["large_image_url"]#  Imagem grande do anime
        
        embed_Message = discord.Embed(title=f"{self.anime_Info_title}", color=discord.Color.blurple())
        embed_Message.add_field(name="Sinopse", value="")
        embed_Message.add_field(name="", value=f"{self.anime_Info_sinopse}")
        embed_Message.add_field(name="MyAnimeList", value=f"{self.anime_Info_link}")
        embed_Message.add_field(name="Rating", value=f":star: **{self.anime_Info_score}**")
        embed_Message.set_image(url=f"{self.img}")
            
        self.view = Buttons(timeout=None)
        await interaction.followup.send(embed=embed_Message, view=self.view)
        
        
    @discord.ui.button(label="", emoji="💖",style=discord.ButtonStyle.blurple)
    async def love_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        

class Anime(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
        
    @app_commands.command(name="recomenda-anime", description="Te recomenda uns animes")
    async def recomenda_Anime(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=False)
        
        self.anime_Database = get_anime()
        
        
        self.anime_Info_title = self.anime_Database["data"]["title"]
        self.anime_Info_link = self.anime_Database["data"]["url"]
        self.anime_Info_sinopse = self.anime_Database["data"]["synopsis"]
        self.anime_Info_score = self.anime_Database["data"]["score"]
        self.img = self.anime_Database["data"]["images"]["jpg"]["large_image_url"]#  Imagem grande do anime
        
        embed_Message = discord.Embed(title=f"{self.anime_Info_title}", color=discord.Color.blurple())
        embed_Message.add_field(name="Sinopse", value="")
        embed_Message.add_field(name="", value=f"{self.anime_Info_sinopse}")
        embed_Message.add_field(name="MyAnimeList", value=f"{self.anime_Info_link}")
        embed_Message.add_field(name="Rating", value=f":star: **{self.anime_Info_score}**")
        embed_Message.set_image(url=f"{self.img}")
            
        self.view = Buttons(timeout=None)
        await interaction.followup.send(embed=embed_Message, view=self.view)
        
        

async def setup(client):
    await client.add_cog(Anime(client))