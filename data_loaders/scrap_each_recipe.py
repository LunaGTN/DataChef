import io
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(liens, *args, **kwargs):
    """
    Fonction pour scraper les pages de recettes
    """

    recipe_soup_list = []
    for url in tqdm(liens):
        try:
            response_recipe = requests.get(url).text
           
            recipe_soup_list.append(response_recipe)
        except Exception:
            print(f"{url} was broken")
            # Ajouter un User-Agent pour éviter d'être bloqué
    return recipe_soup_list