import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

# Charger les variables depuis .env
load_dotenv()

API_KEY = os.getenv("API_KEY") #in .env file
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

"""Fonctions qui concernent les noms d'ingrédients"""

# A quel catégorie l'ingrédient appartient-il ?
def categorize_ingredient(name)-> str:
    prompt = name
    context = "Catégorise l'ingrédient en fonction des catégories suivantes: viande, fruits&légumes, produits laitiers, poisson&fruits de mer, céréales ou autre si l'ingrédient ne correspond à aucune catégorie. Si c'est une herbe aromatique, classe-là dans Autre. Répond uniquement avec le nom de la catégorie."
    question = f"Contexte : {context} Question : {prompt}"
    reponse = model.generate_content(question).text
    return reponse.strip()

# Combien pèse l'ingrédient à l'unité ?
def weight_per_unit(name):
    prompt = name
    context = "Donne-moi le poids moyen, en gramme, d'une unité de cet ingrédient.Ta réponse est un chiffre"
    question = f"Contexte : {context} Question : {prompt}"
    reponse = model.generate_content(question).text
    return reponse.strip()

"""Fonctions qui concernent les titres des recettes"""
#De quel pays du monde provient la recette ?
def map_recipe(titre):
    prompt = titre
    context = "Attribu à chaque recette son pays de provenance, pas sa région (Italienne, Vietnamienne, française... pas Alsacienne ou Vosgienne). Ne répond qu'avec le nom de l'origine et rien d'autre."
    question = f"Contexte : {context} Question : {prompt}"
    reponse = model.generate_content(question).text
    return reponse.strip()

# La recette est-elle sucrée ou salée ?
def sweet_salt(titre):
    prompt = titre
    context = "Attribu à chaque recette la valeur 'sucré' si c'est une recette qui se mange au dessert ou 'salé' si c'est une recette qui se mange en entrée ou en plat. Ne répond que 'sucré' ou 'salé'"
    question = f"Contexte : {context} Question : {prompt}"
    reponse = model.generate_content(question).text
    return reponse.strip()