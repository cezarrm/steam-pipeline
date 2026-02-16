def create_views(cursor):
    cursor.execute("""
        CREATE OR REPLACE VIEW vw_top_games AS
        SELECT game_name, playtime_hours
        FROM games
        ORDER BY playtime_hours DESC
    """)

    cursor.execute("""
        CREATE OR REPLACE VIEW vw_playtime_bucket AS
            SELECT
                CASE
                    WHEN playtime_hours < 10 THEN '0-10h'
                    WHEN playtime_hours < 50 THEN '10-50h'
                    WHEN playtime_hours < 100 THEN '50-100h'
                    ELSE '100h+'
                END AS playtime_range,
                COUNT(*) AS total_games
            FROM games
            GROUP BY playtime_range;

    """)

    cursor.execute("""
        CREATE OR REPLACE VIEW vw_playtime_by_genre AS
        SELECT genre,
               SUM(playtime_hours) AS total_hours,
               COUNT(*) AS total_games
        FROM games
        GROUP BY genre
        ORDER BY total_hours DESC
    """)
