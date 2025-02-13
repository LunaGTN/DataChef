from fonctions.sql_manager import SQL_recipe_manager
from typing import Dict

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(dict_recipes:Dict[str, str]):
    """
    Exports data to AWS RDS.

    Args:
        data: The output from the upstream parent block

    
    """
    connector = SQL_recipe_manager()
    if connector.is_connected:
        for recipe in dict_recipes:
            connector.manage_recipe(recipe)




