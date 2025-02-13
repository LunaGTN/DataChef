from fonctions.sql_manager import  DatabaseConnection
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

color_palet = px.colors.sequential.RdBu

def get_weekly_recipe(user_id) -> dict:
    with DatabaseConnection() as db_connexion:
        try :
            c = db_connexion.cursor()
            request = f""" SELECT name, sweet_salt, time_preparation, time_cooking, time_total, difficulty, cost, country
                    from recipe r 
                    where r.id IN (
                    select id_recipe from user_recipe 
                    where id_user = '{user_id}' and planner = True);"""
            c.execute(request)
            columns = ["name", "sweet_salt", "prepa", "cuisson", "total", "difficulté","cout", 'pays']  # Récupère les noms des colonnes
            result = [dict(zip(columns, row)) for row in c.fetchall()]
        finally:
            return result
            c.close()

def get_weekly_ingredient(user_id):
    with DatabaseConnection() as db_connexion:
        try :
            c = db_connexion.cursor()
            request = f"""select i.id, i.name, quantity, r.nb_person, unit, weigh,category from recipe r 
                        inner join ingredient_recipe ir
                        on r.id = ir.id_recipe
                        inner join ingredient i 
                        on ir.id_ingredient = i.id
                        where r.id IN (
                        select id_recipe from user_recipe 
                        where id_user = '{user_id}' and planner = True);"""
            c.execute(request)
            columns = ["id", "name", "quantity", "nb_person", "unit", "weigh","category"]  # Récupère les noms des colonnes
            result = [dict(zip(columns, row)) for row in c.fetchall()]
        finally:
            return result
            c.close()

def metric_system(dico)-> int:
    conversion_factors = {
    "cl": 10,
    "cuillère à soupe": 15,
    "kg": 1000,
    "ml": 1,
    "cuillère à café": 5,
    "dl" : 100,
    "l": 1000}

    if dico.get("weigh") and dico["unit"] == '':  # Vérifie si 'weigh' existe et n'est pas None
        dico["quantity"] *= dico["weigh"]
    if dico["unit"] in conversion_factors:
        dico["quantity"] *= conversion_factors[dico["unit"]]
    
    return dico["quantity"]

def conversion(horaire_min:int) -> int:
    heures = horaire_min // 60
    minutes = horaire_min % 60
    return heures, minutes

def card(calculation, _title):
    heures = conversion(calculation)[0]
    minutes = conversion(calculation)[1]
    if heures == 0:
        fig = go.Figure(go.Indicator(
        mode = "number",
        value = minutes,
        number = {'suffix': " min", "font": {'color': color_palet[0]}},
        title = _title))

    else:
        fig = go.Figure(go.Indicator(
            mode="number",
            value=heures,  # Ajout des minutes sous forme décimale pour l'affichage
            number={'suffix': f" h {minutes} min", "font": {'color': color_palet[0]}},
            title=_title
        ))

    fig.update_layout(paper_bgcolor = color_palet[4],
                    width = 400, height = 225)

    return fig

def get_nb_repas(user_id)-> dict:
    with DatabaseConnection() as db_connexion:
        try :
            c = db_connexion.cursor()
            request = f""" select week_lunch, week_we 
                        from users
                        where id = '{user_id}'
            ;"""
            c.execute(request)
            columns = ["lunch", "we"]  # Récupère les noms des colonnes
            result = [dict(zip(columns, row)) for row in c.fetchall()]
        finally:
            return result
            c.close()

def nb_conso_per_recipe(user_id, data):
    nb_repas = get_nb_repas(user_id)[0]
    nb_recettes = data.shape[0]
    if nb_repas['lunch'] and not nb_repas['we']:
        return int(10 / nb_recettes)
    elif nb_repas['we'] and not nb_repas['lunch']:
        return int(9 /nb_recettes)
    elif nb_repas['lunch'] and nb_repas['we']:
        return int(14/nb_recettes)
    else:
        return int(5/nb_recettes)