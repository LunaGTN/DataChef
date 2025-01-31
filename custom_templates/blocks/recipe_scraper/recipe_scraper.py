if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(_soup):
    time = _soup.find('div', {"class" : "time__details"}).find_all('div')
    time_preparation = time[1].get_text()
    time_rest = time[3].get_text()
    time_cooking = time[5].get_text()
    image_link = _soup.find('img',{"class":"lazyload mrtn-print-only"}).get("data-src")
    nb_person = _soup.find("div",{"class":'mrtn-recette_ingredients-counter'}).get("data-servingsnb")


    difficulty = _soup.find_all('div',{"class": 'recipe-primary__item'})
    result = []
    for div in difficulty:
        # Trouver la balise <span> et extraire son texte
        span = div.find('span')
        if span:
            result.append(span)

    time_total = result[0].get_text()
    difficulty= result[1].get_text()
    cost = result[2].get_text()



    instructions = _soup.find_all("div",{"class":'recipe-step-list__container'})
    steps = []
    for i in range(len(instructions)):
        for p in instructions[i].find_all("p"):
            steps.append(p.get_text())
    

    ingredient_recipe = []
    ingredients = _soup.find_all("span",{"class":"card-ingredient-title"})
    ids_ingredient = _soup.find_all("div",{"class":"card-ingredient-checkbox"})

    for i in range(len(ingredients)):
        name = ingredients[i].find("span",{"class":"ingredient-name"}).get("data-ingredientnameplural")
        quantity_unit = ingredients[i].find("span", {"class":"card-ingredient-quantity"})
        quantity = quantity_unit.get("data-ingredientquantity")
        unit = quantity_unit.find("span", {"class":"unit"}).get("data-unitsingular")
        id_ingredient= ids_ingredient[i].find("input").get("id")
        
        ingredient_recipe.append({
            "nom":name,
            "quantite": quantity,
            "unite":unit,
            "id": id_ingredient[6:]
        })


    recipe = {
        "temps_preparation" : time_preparation,
        "tems_repos" : time_rest,
        "temps_cuisson": time_cooking ,
        "image" : image_link ,
        "nb_personne": nb_person,
        "temps_total": time_total ,
        "difficulte":difficulty,
        "cout": cost,
        "etapes": steps,
        "ingredients": ingredient_recipe
    }

    return recipe


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
