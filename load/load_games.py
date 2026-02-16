import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv
from pathlib import Path
from load.create_views import create_views

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = BASE_DIR / "data" / "processed" / "games_enriched.csv"


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games(
            appid INT PRIMARY KEY,
            game_name VARCHAR(255),
            playtime_hours FLOAT,
            playtime_last_2weeks_hours FLOAT,
            genre TEXT
        )
    """)


def load_data():
    df = pd.read_csv(INPUT_PATH)

    conn = get_connection()
    cursor = conn.cursor()

    create_table(cursor)

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO games
            (appid, game_name, playtime_hours, playtime_last_2weeks_hours, genre)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                game_name = VALUES(game_name),
                playtime_hours = VALUES(playtime_hours),
                playtime_last_2weeks_hours = VALUES(playtime_last_2weeks_hours),
                genre = VALUES(genre)
        """, (
            int(row["appid"]),
            row["game_name"],
            float(row["playtime_hours"]),
            float(row["playtime_last_2weeks_hours"]),
            row["genre"]
        ))

    
    create_views(cursor)

    conn.commit()
    cursor.close()
    conn.close()

    print("Dados carregados e views atualizadas no MySQL")


if __name__ == "__main__":
    load_data()
