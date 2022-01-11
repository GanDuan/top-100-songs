import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


Client_ID = client_ID
Client_Secret = client_token
redirect_url = "http://127.0.0.1:9090"

#TODO find the top 100 songs from the date you choose from billboard website
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
path = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(url=path)
website = response.text

content = BeautifulSoup(website, "html.parser")
names = content.find_all(name="h3", id="title-of-a-story", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
song = [item.getText() for item in names]
song_titles = []
for items in song:
    data = items.split("\n")
    song_titles.append(data[1])

#TODO authentification with spotify
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                                scope=scope,
                                                client_id=Client_ID,
                                                client_secret=Client_Secret,
                                                redirect_uri=redirect_url,
                                                show_dialog=True,
                                                cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

#TODO search songs in spotipy
year = date.split("-")[0]
song_url = []
for item in song_titles:
    results = sp.search(q=f"track:{item} year:{year}", type="track")
    try:
        url = results["tracks"]["items"][0]["uri"]
        song_url.append(url)
    except IndexError:
        print(f"{item} doesn't exist in Spotify. Skipped.")


#TODO add the links of songs to a list in spotipy
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, description="top 100 songs from billborad")
sp.playlist_add_items(playlist_id=playlist["id"], items=song_url)
