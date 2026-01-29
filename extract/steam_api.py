import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"



params = {
        "key": STEAM_API_KEY,
        "steamid" : STEAM_ID,
        "include_appinfo": True,
        "include_played_free_games": True,
        "format": "json"
    }
print('Chamando a API...')
response = requests.get(URL, params=params)
response.raise_for_status()

data = response.json()

print("\n Resposta da API:")
print(data)