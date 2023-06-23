import discord, requests, random, asyncio
from discord.ext import commands
from discord import app_commands


       
def get_anime():
    anime_Database = requests.get(f"https://api.jikan.moe/v4/random/anime")
    anime_Database = anime_Database.json()
    anime_list = []
    
    with open("./database/Anime/animes.txt", "r") as arquivo:
        for anime in arquivo:
            anime_list.append(anime[:-1])
                    
    while True:
        if anime_Database["data"]["score"] != None and anime_Database["data"]["synopsis"] != None and anime_Database["data"]["approved"] == True and anime_Database["data"]["popularity"] <= 5000 and anime_Database["data"]["title"] not in anime_list and anime_Database["data"]["rating"] not in "Rx - Hentai" and len(anime_Database["data"]["themes"]) != 0:
            break
        else:       
            anime_Database = requests.get(f"https://api.jikan.moe/v4/random/anime")
            anime_Database = anime_Database.json()
            print(anime_Database["data"]["title"]) 
    
   
    with open("./database/Anime/animes.txt", "a") as arquivo:
        arquivo.write(f"{anime_Database['data']['title']}\n")
        
    return anime_Database    
    
class Buttons(discord.ui.View):
    
    @discord.ui.button(label="", emoji="🔎",style=discord.ButtonStyle.success)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        await interaction.followup.send("Procurando por mais animes...")
        self.anime_Database = get_anime()
        self.list_sinopse = []
        
        self.anime_Info_title = self.anime_Database["data"]["title"]
        self.anime_Info_link = self.anime_Database["data"]["url"]
        self.list_sinopse.append(self.anime_Database["data"]["synopsis"].split("."))
        self.anime_Info_score = self.anime_Database["data"]["score"]
        self.anime_Info_popularity = self.anime_Database["data"]["popularity"]
        self.anime_info_theme =  self.anime_Database["data"]["themes"][0]["name"]
        self.img = self.anime_Database["data"]["images"]["jpg"]["large_image_url"]#  Imagem grande do anime
        
        embed_Message = discord.Embed(title=f"{self.anime_Info_title}", color=discord.Color.blurple())
        embed_Message.add_field(name="Sinopse", value="", inline=False)
        embed_Message.add_field(name="", value=f"{self.list_sinopse[0][0]}", inline=False)
        embed_Message.add_field(name="Anime Theme", value=f"{self.anime_info_theme}")
        embed_Message.add_field(name="Rating", value=f":star: **{self.anime_Info_score}**")
        embed_Message.add_field(name="Popularity", value=f":medal: **#{self.anime_Info_popularity}**")
        embed_Message.add_field(name="MyAnimeList", value=f"{self.anime_Info_link}")
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
        self.list_sinopse = []
        
        self.anime_Info_title = self.anime_Database["data"]["title"]
        self.anime_Info_link = self.anime_Database["data"]["url"]
        self.list_sinopse.append(self.anime_Database["data"]["synopsis"].split("."))
        self.anime_Info_score = self.anime_Database["data"]["score"]
        self.anime_info_theme =  self.anime_Database["data"]["themes"][0]["name"]
        self.anime_Info_popularity = self.anime_Database["data"]["popularity"]
        self.img = self.anime_Database["data"]["images"]["jpg"]["large_image_url"]#  Imagem grande do anime
        
        embed_Message = discord.Embed(title=f"{self.anime_Info_title}", color=discord.Color.blurple())
        embed_Message.add_field(name="Sinopse", value="", inline=False)
        embed_Message.add_field(name="", value=f"{self.list_sinopse[0][0]}", inline=False)
        embed_Message.add_field(name="Anime Theme", value=f"{self.anime_info_theme}")
        embed_Message.add_field(name="Rating", value=f":star: **{self.anime_Info_score}**")
        embed_Message.add_field(name="Popularity", value=f":medal: **#{self.anime_Info_popularity}**")
        embed_Message.set_image(url=f"{self.img}")
        embed_Message.add_field(name="MyAnimeList", value=f"{self.anime_Info_link}")  
        
        self.view = Buttons(timeout=None)
        await interaction.followup.send(embed=embed_Message, view=self.view)
        
        

async def setup(client):
    await client.add_cog(Anime(client))