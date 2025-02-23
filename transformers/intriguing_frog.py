from bs4 import BeautifulSoup

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
    
from transformers.utils import info_recettes, get_time_diff_cost, get_instructions, get_ingredient, reconstitution

@transformer
def transform(recipe_soup_list, *args, **kwargs):
    dict_recipes= []
    for recipe in recipe_soup_list:
        soup = BeautifulSoup(recipe, "html.parser")
        recette = info_recettes(soup)
        time_diff_cost = get_time_diff_cost(soup)
        instructions = get_instructions(soup)
        ingredient = get_ingredient(soup)
        dict_recipes.append(reconstitution(recette, time_diff_cost, instructions, ingredient))
    return dict_recipes
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
