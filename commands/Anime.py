import discord, requests, random, asyncio
from discord.ext import commands
from discord import app_commands
       
def get_anime(pessoa):
    genero = []
    anime_list = []
    
    with open("./database/Anime/filtro.txt", "r") as arquivo:
        for id in arquivo:
            genero.append(id)
            
    with open("./database/Anime/animes.txt", "r") as arquivo:
        for anime in arquivo:
            anime_list.append(anime[:-1])
    page = 1       
    genero_id = int(genero[0][:-1])
    check = False
    anime_Database = requests.get(f"https://api.jikan.moe/v4/anime?genres={genero_id}&min_score=8.0&page={page}&type=tv")
    anime_Database = anime_Database.json()
    print(f"[{pessoa}] Está procurando por animes")

    while page <= anime_Database["pagination"]["last_visible_page"]:
        for anime in anime_Database["data"]:
            if anime["title"] not in anime_list and len(anime["themes"]) != 0:   
                print("Encontrei!")  
                check = True
                break
       
        if check == True:
            break
        else:
            page += 1
            anime_Database = requests.get(f"https://api.jikan.moe/v4/anime?genres={genero_id}&min_score=8.0&page={page}&type=tv")
            anime_Database = anime_Database.json()
            print(anime["title"]) 

    
    print(anime["title"])
    with open("./database/Anime/animes.txt", "a") as arquivo:
        arquivo.write(f"{anime['title']}\n")
    print("Mensagem enviada!")
    return anime 
    
class Buttons(discord.ui.View):
    
    @discord.ui.button(label="Procurar mais Animes", emoji="🔎",style=discord.ButtonStyle.blurple)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        genero = []
        with open("./database/Anime/filtro.txt", "r") as arquivo:
            for filtro in arquivo:
                genero.append(filtro)
                
        await interaction.followup.send(f"Procurando por mais animes de **{genero[1]}**...")
        self.anime_Database = get_anime(interaction.user.name)
        self.list_sinopse = []
        
        self.anime_Info_title = self.anime_Database["title"]
        self.anime_Info_link = self.anime_Database["url"]
        self.list_sinopse.append(self.anime_Database["synopsis"].split("."))
        self.anime_Info_score = self.anime_Database["score"]
        self.anime_info_theme =  self.anime_Database["themes"][0]["name"]
        self.anime_Info_popularity = self.anime_Database["popularity"]
        self.img = self.anime_Database["images"]["jpg"]["large_image_url"]#  Imagem grande do anime
        
        embed_Message = discord.Embed(title=f"{self.anime_Info_title}", color=discord.Color.blurple())
        embed_Message.add_field(name="Sinopse", value=f"{self.list_sinopse[0][0]}", inline=False)
        embed_Message.add_field(name="", value=f"", inline=False)
        embed_Message.add_field(name="Anime Theme", value=f":game_die: **{self.anime_info_theme}**")
        embed_Message.add_field(name="Rating", value=f":star: **{self.anime_Info_score}**")
        embed_Message.add_field(name="Popularity", value=f":medal: **#{self.anime_Info_popularity}**")
        embed_Message.set_image(url=f"{self.img}")
        embed_Message.add_field(name="MyAnimeList", value=f"{self.anime_Info_link}")  
        
        self.view = Buttons(timeout=None)
        await interaction.followup.send(embed=embed_Message, view=self.view)
        
class Anime(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    
        
    @app_commands.command(name="recomenda-anime", description="Te recomenda uns animes")
    async def recomenda_Anime(self, interaction: discord.Interaction):
        
        await interaction.response.defer(thinking=False)
        genero = []
        with open("./database/Anime/filtro.txt", "r") as arquivo:
            for filtro in arquivo:
                genero.append(filtro)
        
        await interaction.channel.send(f"O filtro selecionado é de: **{genero[1]}**")
        self.anime_Database = get_anime(interaction.user.name)
        self.list_sinopse = []
        
        self.anime_Info_title = self.anime_Database["title"]
        self.anime_Info_link = self.anime_Database["url"]
        self.list_sinopse.append(self.anime_Database["synopsis"].split("."))
        self.anime_Info_score = self.anime_Database["score"]
        self.anime_info_theme =  self.anime_Database["themes"][0]["name"]
        self.anime_Info_popularity = self.anime_Database["popularity"]
        self.img = self.anime_Database["images"]["jpg"]["large_image_url"]#  Imagem grande do anime
        
        embed_Message = discord.Embed(title=f"{self.anime_Info_title}", color=discord.Color.blurple())
        embed_Message.add_field(name="Sinopse", value=f"{self.list_sinopse[0][0]}", inline=False)
        embed_Message.add_field(name="", value=f"", inline=False)
        embed_Message.add_field(name="Anime Theme", value=f":game_die: **{self.anime_info_theme}**")
        embed_Message.add_field(name="Rating", value=f":star: **{self.anime_Info_score}**")
        embed_Message.add_field(name="Popularity", value=f":medal: **#{self.anime_Info_popularity}**")
        embed_Message.set_image(url=f"{self.img}")
        embed_Message.add_field(name="MyAnimeList", value=f"{self.anime_Info_link}")  
        
        self.view = Buttons(timeout=None)
        await interaction.followup.send(embed=embed_Message, view=self.view)
        
    
async def setup(client):
    await client.add_cog(Anime(client))