import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from fonctions.dashboard_func import get_weekly_recipe, get_weekly_ingredient, metric_system, conversion, card, nb_conso_per_recipe,get_nb_repas

user_id = st.session_state['user_info']['id']

color_palet = px.colors.sequential.RdBu
recettes_hebdo = pd.DataFrame(get_weekly_recipe(str(user_id)))

# Header / Title
st.markdown("<h2 style='color: #DE684D;'> Votre Dashboard hebdomadaire 🧐</h2>", unsafe_allow_html=True)
st.write('---')

if len(recettes_hebdo) != 0:

    data_ingredient = get_weekly_ingredient(str(user_id))
    dico_qtity = []  # Liste pour stocker les nouvelles quantités d'ingrédients
    conso_recette_hebdo = nb_conso_per_recipe(user_id,recettes_hebdo)  # Nombre de fois que la personne consomme chaque recette

    for ingredient in data_ingredient:
        quantity_g = metric_system(ingredient)
        # Normalisation à 1 personne et ajustement pour la consommation hebdomadaire
        normalized_quantity = round((quantity_g /ingredient['nb_person']) * conso_recette_hebdo)
        if ingredient["category"] != 'Autre':  # Exclusion des catégories "Autre"
            dico_qtity.append({
                "Nom":ingredient["name"],
                "Catégorie": ingredient["category"],
                "Quantité": normalized_quantity})

    df = pd.DataFrame(dico_qtity)


    st.markdown(f"<h5 '> Cette semaine, vous cuisinerez {recettes_hebdo.shape[0]} recettes ! </h5>", unsafe_allow_html=True)
    st.write('')

    st.subheader(f"Il y a {recettes_hebdo.shape[0]} recettes dans votre semainier !")
    st.write('')

    col1, col2 , col3, col4 = st.columns([2,2,2,3])
    with col1 :
        prep_mean = card(recettes_hebdo['prepa'].mean(), 'Temps de préparation moyen')
        st.plotly_chart(prep_mean)
    with col2:
        prep_sum = card(recettes_hebdo['prepa'].sum(), 'Temps de préparation Total')
        st.plotly_chart(prep_sum)
    with col3:
        sum_cook = card(recettes_hebdo['cuisson'].sum(), 'Temps de cuisson Total')
        st.plotly_chart(sum_cook)

    with col4:
        st.write("""**Top 3 des ingrédients** """)
        top_3 = df.sort_values(by = 'Quantité', ascending = False).head(3).reset_index(drop = True)
        top_3.index = top_3.index + 1
        st.write(top_3)
        with st.expander("Explications"):
            st.write("""Voici les 3 ingrédients les plus consommés cette semaine en termes de quantité.
                    Il s'agit des quantités **en grammes, pour une personne**.
                    Cette visualisation vous montre les ingrédients qui apparaissent le plus souvent dans
                    vos repas, vous permettant ainsi de mieux comprendre les tendances de votre alimentation hebdomadaire. """)


    col1, col2, col3 = st.columns([1,1.5,1.5])
    with col1:
        # Pie chart Nationalité
        data_origin = recettes_hebdo['pays'].value_counts()
        origin_chart = px.pie(data_origin, data_origin.index, values=data_origin.values, title='Répartition de la nationalité des recettes',
                    color_discrete_sequence=color_palet,
                    width = 400, height = 400 )

else:
    st.subheader(f"Il n'y a pas de recettes dans votre semainier !")
    st.write('')
    st.write('Selectionnez des recettes depuis votre livre pour profiter de votre tableau de bord')
    if st.button('**Mes recettes**', icon='📕'):
        st.switch_page('app_page_recipe_book.py')

# Style 
st.markdown('''<style>
           
            </style>''', unsafe_allow_html=True)
