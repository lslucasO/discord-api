import requests
page = 1
num = 1
genre_id = 36
anime_list = []

frase = "Isso ai vai dar ban no nbot"
f = open(f"database/Obs/hasanchez.txt", "r")
for item in f:
    if item[:-1] in frase:
        print("peguei")
    else:   
        print(item[:-1])

# with open("./database/Anime/animes.txt", "r") as arquivo:
#     for anime in arquivo:
#         anime_list.append(anime[:-1])
        
# anime_Database = requests.get(f"https://api.jikan.moe/v4/anime?genres={genre_id}&min_score=7.0&page={page}&type=tv")
# anime_Database = anime_Database.json()
# print(anime_Database["pagination"])

# while num <= anime_Database["pagination"]["last_visible_page"]:
#     for anime in anime_Database["data"]:
#         print(len(anime["themes"]))
#     num += 1
    
#     print(num)
#     anime_Database = requests.get(f"https://api.jikan.moe/v4/anime?genres={genre_id}&min_score=7.0&page={num}&type=tv")
#     anime_Database = anime_Database.json()
