from bs4 import BeautifulSoup


def info_recettes(_soup):
    titre = _soup.find('h1').text
    id = _soup.find('meta', {"name":"ad:rid"}).get("content")
    time = _soup.find('div', {"class" : "time__details"}).find_all('div')
    time_preparation = time[1].get_text()
    time_rest = time[3].get_text()
    time_cooking = time[5].get_text()
    image_link = _soup.find('img',{"class":"lazyload mrtn-print-only"}).get("data-src")
    nb_person = _soup.find("div",{"class":'mrtn-recette_ingredients-counter'}).get("data-servingsnb")
    return {
        "title":titre,
        "id": id,
        "time_preparation" : time_preparation,
        "time_repos" : time_rest,
        "time_cuisson": time_cooking ,
        "image" : image_link ,
        "nb_person": nb_person
    }

def get_time_diff_cost(_soup):
    result = []
    div_difficulty = _soup.find_all('div',{"class": 'recipe-primary__item'})
    for div in div_difficulty:
        # Trouver la balise <span> et extraire son texte
        span = div.find('span')
        if span:
            result.append(span)
    time_total = result[0].get_text()
    difficulty= result[1].get_text()
    cost = result[2].get_text()

    return {
        "time_total":time_total,
        "difficulty": difficulty,
        "cost": cost}

def get_instructions(_soup):
    instructions = _soup.find_all("div",{"class":'recipe-step-list__container'})
    steps = []
    steps_dict = []
    for i in range(len(instructions)):
        for p in instructions[i].find_all("p"):
            steps.append(p.get_text())
    return {"steps":steps}

def get_ingredient(_soup):
    ingredient_recipe = []
    ingredients = _soup.find_all("span",{"class":"card-ingredient-title"})
    ids_ingredient = _soup.find_all("div",{"class":"card-ingredient-checkbox"})

    for i in range(len(ingredients)):
        name = ingredients[i].find("span",{"class":"ingredient-name"}).get("data-ingredientnameplural")
        quantity_unit = ingredients[i].find("span", {"class":"card-ingredient-quantity"})
        quantity = quantity_unit.get("data-ingredientquantity")
        unit = quantity_unit.find("span", {"class":"unit"}).get("data-unitsingular")
        id_ingredient= ids_ingredient[i].find("input").get("id")
        ingredient_recipe.append(
            {
            "name":name,
            "quantity": quantity,
            "unit": unit,
            "id" : id_ingredient[5:]
        })
    
    return {"ingredients" : ingredient_recipe}

def reconstitution(info_recettes, time_diff_cost_dict, steps_dict,ingredient_recipe ):
    recipe = info_recettes |time_diff_cost_dict | steps_dict | ingredient_recipe
    return recipe


def load_data(recipe_text_list):
    dict_recipes= []
    for recipe in recipe_text_list:
        soup = BeautifulSoup(recipe, "html.parser")
        recette = info_recettes(soup)
        time_diff_cost = time_diff_cost(soup)
        instructions = instructions(soup)
        ingredient = ingredient(soup)
        dict_recipes.append(reconstitution(recette, time_diff_cost, instructions, ingredient))
    return dict_recipes