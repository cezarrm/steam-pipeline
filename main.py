from extract.steam_api import main as extract_main
from transform.transform_games import main as transform_main
from transform.enrich_data import main as enrich_main
from load.load_games import load_data

if __name__ == "__main__":
    extract_main()
    transform_main()
    enrich_main()
    load_data()