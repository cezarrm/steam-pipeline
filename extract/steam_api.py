import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"


def get_owned_games(): 
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
        return response.json()

def save_raw_json(data):
        os.makedirs("data/raw", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f'data/raw/owned_games_{timestamp}.json'

        with open (path, 'w', encoding="utf-8") as f:
                   json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Raw salvo em {path}")

def main():
        print('Extraindo dados da API')
        data = get_owned_games()
        save_raw_json(data)

if __name__ == "__main__":
    main()
