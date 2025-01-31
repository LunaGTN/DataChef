import io
import pandas as pd
import requests
from bs4 import BeautifulSoup


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    urls = [
    'https://www.marmiton.org/recettes/top-internautes-plat-principal.aspx',
    'https://www.marmiton.org/recettes/top-internautes-entree.aspx',
    "https://www.marmiton.org/recettes/top-internautes-dessert.aspx"
    ]

    recipe_links = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        recipe_link = soup.find_all('a', {"class" : "recipe-card-link"})
        for link in recipe_link:        
            href = link.get('href')
            recipe_links.append(href)

    return list(recipe_links)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
