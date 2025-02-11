from dotenv import load_dotenv
from fonctions.gemini import categorize_ingredient, map_recipe, sweet_salt, weight_per_unit
import json
import logging
import os
import pandas as pd
import psycopg2
from typing import List, Literal
from random import randint
import re


load_dotenv()

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    encoding="utf-8",    
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M"
)


class DatabaseConnection():
    def __init__(self):
        self.username=os.getenv('UTILISATEUR')
        self.password=os.getenv('PASSWORD')
        self.engine=os.getenv('ENGINE')
        self.host=os.getenv('HOST')
        self.port=os.getenv('PORT')

    def __enter__(self):
        self.db_connector = psycopg2.connect(
            host=self.host,
            database=self.engine,
            user=self.username,
            password=self.password
        )
        return self.db_connector

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_connector.close()
        pass


class SQL_recipe_manager():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

     
    @staticmethod
    def fomat_time(time:str)->int:
        """
        Format string time to number of minutes int
        """
        if type(time) == int:
            return time
        else:
            h_m = re.findall(r"\d+", time)
            if not bool(h_m) :
                return 0
            if "h" in time and len(h_m) == 2 :
                return int(h_m[0])*60 + int(h_m[1])
            elif "h" in time and len(h_m) == 1 :
                return int(h_m[0])*60
            else :
                return int(h_m[0])
        

    def is_connected(self):
        with DatabaseConnection() as db_connexion:
            if not db_connexion.closed:
                self.connexion = db_connexion
                logging.info("Successfully connected")
                return True
            else:
                return False


    def check_db_by_id(self, id:str, table:Literal['ingredient', 'recipe', 'users'])->bool:
        """
            Check if an item already exists in database

            Attribut
            -----------
            id: id of the item
            db: database to check 
                ingredient
                recipe
                users

            Return
            -----------
            boolean
        """

        with DatabaseConnection() as db_connexion:
            try :
                c = db_connexion.cursor()
                if table == 'users':
                    request = f"SELECT * FROM {table} WHERE id = '{id}'"
                else:
                    request = f"SELECT * FROM {table} WHERE id = '{int(id)}'"
                c.execute(request)
                row_count = len(c.fetchall())
                return bool(row_count)
            
            except psycopg2.OperationalError as err:
                self.logger.error(f"Checking Error: {err}")

            finally:
                if c.description is not None:
                    c.fetchall()
                c.close()

    
    def check_db_by_name(self, name:str, table:Literal['ingredient', 'recipe']= 'ingredient')->bool:
        """
            Check if an item already exists in database

            Attribut
            -----------
            name: name of the item
            db: database to check 
                ingredient
                recipe

            Return
            -----------
            id of item
        """

        with DatabaseConnection() as db_connexion:
            try :
                c = db_connexion.cursor()
                request = f"SELECT * FROM {table} WHERE name = '{name.capitalize().replace("'", "\'\'")}'"
                c.execute(request)
                results = c.fetchall()
                return bool(results)
            
            except psycopg2.OperationalError as err:
                self.logger.error(f"Checking Error: {err}")

            finally:
                if c.description is not None:
                    c.fetchall()
                c.close()


    def add_recipe(self, recipe_data)->None:
        """
        Add recipe to recipe database 

        Attributs
        -------------
        recipe_data: json
            name: str
            link: str
            id: str
            time_preparation: str
            time_repos: str
            time_cuisson: str
            image: str
            nb_person: str
            time_total: str
            difficulty: str
            cost: str
            steps: list of str
            ingredients: list of dict
        """

        recipe_data['sweet_salt'] = sweet_salt(recipe_data['name'])
        recipe_data['country'] = map_recipe(recipe_data['name'])

        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()

                request = """
                INSERT INTO recipe (id, name, nb_person, time_preparation, time_rest, time_cooking, time_total, difficulty, cost, image_link, sweet_salt, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            
                datas = (
                    int(recipe_data['id']),
                    recipe_data['name'].capitalize().replace("'", "\'\'"),
                    int(recipe_data['nb_person']),
                    self.fomat_time(recipe_data['time_preparation']),
                    self.fomat_time(recipe_data['time_rest']),
                    self.fomat_time(recipe_data['time_cooking']),
                    self.fomat_time(recipe_data['time_total']),
                    recipe_data['difficulty'],
                    recipe_data['cost'],
                    recipe_data['image_link'],
                    recipe_data['sweet_salt'],
                    recipe_data['country']
                )

                c.execute(request, datas)
                db_connexion.commit()

                self.logger.info(f"{recipe_data['name']} was successfully add to database")
        
            except psycopg2.OperationalError as err:
                self.logger.error(f"Insert error: {err}")

            finally:
                c.close()


    def add_steps(self, steps:List[str], id_recipe:int)->None:
        """
        Add recipe to recipe database 

        Attributs
        -------------
        id_recipe: str
            id of recipe
        steps: list of str
            list of steps
        """

        if type(steps[0])==dict:
            steps = [step['detail'] for step in steps]
        
        with DatabaseConnection() as db_connexion:
            c = db_connexion.cursor()
            request = """INSERT INTO step (id_recipe, step_number, detail)
            VALUES(%s, %s, %s)"""
            datas=[
                [int(id_recipe),
                id+1,
                step
                ] for id, step in enumerate(steps)
            ]

            try:
                c.executemany(request, datas)
                db_connexion.commit()

                self.logger.info(f"Steps were successfully add to database")

            except psycopg2.OperationalError as err:
                self.logger.error(f"Insert error: {err}")

            finally:
                if c.description is not None:
                    c.fetchall()
                c.close()
            

    def add_ingredient(self, ingredient:dict)->None:
        """
        Add an ingredient to ingredient db

        Attributs
        -------------
        ingredient: dict
            id: int
                id of ingredient
            name: str
                name of the ingredient
            quantity: float
                quantity of the ingredient
            unit: str
                unit for this quantity
        """
        ingredient['category'] = categorize_ingredient(ingredient['name'])
        if ingredient['unit'] == '' and ingredient['quantity'] != 0 and ingredient['category'] != 'Autre':
            ingredient['weigh'] = weight_per_unit(ingredient['name'])
        else:
            ingredient['weigh'] = None

        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()

                request = """
                INSERT INTO ingredient (id, name, category, weigh)
                VALUES (%s, %s, %s, %s)
                """
                
                datas = [
                        int(ingredient['id']),
                        ingredient['name'].capitalize().replace("'", "\'\'"),
                        ingredient['category'],
                        ingredient['weigh']
                ]

                c.execute(request, datas)
                db_connexion.commit()

                self.logger.info(f"{ingredient['name'].capitalize()} was successfully add to database")

            except psycopg2.OperationalError as err:
                self.logger.error(f"Insert error: {err}")

            finally:
                c.close()


    def check_duplicate_ingredient(self, ingredients:List[dict], id_recipe:int)->List[dict]:
        """
        Check if an ingredient appears twice or more in ingredients list.
        If it happens, add quantity in a single row

        Attributs
        -------------
        ingredients: list of dict
            list of ingredients with name, id, quantity and unit
        id_recipe: int
            id of the recipe

        Return
        -------------
        datas : list of dict
            clean list of ingredients datas
        """

        list_id = []
        datas = []
        for ingredient in ingredients :
            if ingredient['id'] not in list_id :
                list_id.append(ingredient['id'])
                datas.append(
                    [int(id_recipe),
                    int(ingredient['id']),
                    float(ingredient['quantity']),
                    ingredient['unit']
                    ])
            else:
                idx = list_id.index(ingredient['id'])
                datas[idx][2] += float(ingredient['quantity'])
        
        self.logger.info(f"Ingredients list of recipe n°{id_recipe} clean")

        return datas


    def add_quantity(self, ingredients:List[dict], id_recipe:int)->None:
        """
        Add an quantity and unite to recipe_ingredient db

        Attributs
        -------------
        id_recipe :int
            id of recipe
        ingredient: dict
            id: int
                id of ingredient
            name: str
                name of the ingredient
            quantity: float
                quantity of the ingredient
            unit: str
                unity for this quantity
        """

        datas = self.check_duplicate_ingredient(ingredients, id_recipe)

        with DatabaseConnection() as db_connexion:

            c = db_connexion.cursor()
            request = """INSERT INTO ingredient_recipe (id_recipe, id_ingredient, quantity, unit)
            VALUES (%s, %s, %s, %s)"""

            try:
                for row in datas:
                    c.execute(request, row)
                    db_connexion.commit()  

                self.logger.info(f"Quantities added for recipe n°{id_recipe}")
        
            except psycopg2.OperationalError as err:
                self.logger.error(f"Insert error: {err}")

            finally:
                c.close()


    def manage_recipe(self, recipe_data:json)-> None:
        """
        Add recipe to recipe database 
        Add ingredients to ingredient database
        Add step to step database
        Add connexion to recipe_ingredient database

        Attributs
        -------------
        recipe_data: json
            titre: str
                name of recipe
            link: str
                url of recipe to Marmiton
            id: int
                id of recipe
            time_preparation: str
                preparation time can be XXmin, XXh, XXhXXmin format
            time_repos: str
                rest time, can be XXmin, XXh, XXhXXmin format
            time_cuisson: str
                cooking time can be XXmin, XXh, XXhXXmin format
            image: str
                url of image 
            nb_person: int
                number of people for whom this recipe is intended
            time_total: str
                total_time can be XXmin, XXh, XXhXXmin format
            difficulty: str
                difficulty of recipe
            cost: str
                cost for this recipe
            steps: list of str
                list of steps for this recipe
            ingredients: list of dict
                list of ingredients with id, name, quantity and unite for each
        """

        if not self.check_db_by_id(id=recipe_data['id'], table="recipe"):
            self.add_recipe(recipe_data=recipe_data)
            self.add_steps(steps=recipe_data['steps'], id_recipe=recipe_data['id'])
            
            for ingredient in recipe_data['ingredients']:

                if not self.check_db_by_id(id=ingredient['id'], table="ingredient"):
                    self.add_ingredient(ingredient=ingredient)
                else:
                    self.logger.info(f"{ingredient['name']} is already in database")

            self.add_quantity(ingredients=recipe_data['ingredients'], id_recipe=recipe_data['id'])
                
        else:
            self.logger.info(f"{recipe_data['title']} is already in database")


    def get_all_recipes(self)->pd.DataFrame:
        """
        Return all recipes name from recipe database
        """
        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()
                request = 'select id, name, image_link from recipe'

                c.execute(request)
                return pd.DataFrame(c.fetchall(), columns=['id', 'name', 'image_link'])

            except psycopg2.OperationalError as err:
                self.logger.error(f"Select error: {err}")

            finally:
                c.close()


    def request_recipe(self, id_recipe:int)->dict:
        """
        Request recipe database for recipe datas from recipe id

        Attributs
        -------------
        id_recipe: int
            The id of the recipe

        Return
        -------------
        recipe details: dict
            - id
            - title
            - nb_person
            - time_preparation
            - time_rest
            - time_cooking
            - time_total
            - difficulty
            - cost
            - image_link
        """
        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()
                request_recipe = f"""
                SELECT 
                    id,
                    name,
                    nb_person,
                    time_preparation, 
                    time_rest,
                    time_cooking,
                    time_total,
                    difficulty,
                    cost,
                    image_link
                FROM recipe WHERE id={id_recipe}
                """
                c.execute(request_recipe)
                result = c.fetchone()
                recipe_data = {
                    'id': result[0],
                    'name': result[1],
                    'nb_person': result[2],
                    'time_preparation': result[3],
                    'time_rest': result[4],
                    'time_cooking': result[5],
                    'time_total': result[6],
                    'difficulty': result[7],
                    'cost': result[8],
                    'image_link': result[9]
                }

                return recipe_data

            except psycopg2.OperationalError as err:
                    self.logger.error(f"Select error: {err}")

            finally:
                c.close()


    def request_ingredient(self, id_recipe:int)->List[dict]:
        """
        Request ingredients and ingredients_recipe databases for ingredients datas from recipe id

        Attributs
        -------------
        id_recipe: int
            The id of the recipe

        Return
        -------------
        ingredients_data: list of dict with:
            - name
            - quantity
            - unit
        """
        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()
                request_ingredients = f"""
                    select 
                        i.name,
                        ir.quantity,
                        ir.unit,
                        i.id
                    from ingredient_recipe ir
                    join ingredient i on ir.id_ingredient = i.id
                    where ir.id_recipe = {id_recipe}
                """
                
                c.execute(request_ingredients)
                results = c.fetchall()
                ingredients_data = [{
                    'name': result[0],    
                    'quantity': result[1],
                    'unit': result[2],
                    'id': result[3]
                } for result in results]

                return ingredients_data

            except psycopg2.OperationalError as err:
                    self.logger.error(f"Select error: {err}")

            finally:
                c.close()


    def request_steps(self, id_recipe:int)->List[dict]:
        """
        Request step database for ingredients datas from recipe id

        Attributs
        -------------
        id_recipe: int
            The id of the recipe

        Return
        -------------
        steps_data: list of dict with:
            - number of the step
            - details
        """
        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()
                request_step = f"""
                    select 
                        step_number,
                        detail
                    from step
                    where id_recipe = {id_recipe}
                    """
                
                c.execute(request_step)
                results = c.fetchall()

                steps_data = [{
                    'step_number': result[0],    
                    'detail': result[1],
                } for result in results]

                return steps_data

            except psycopg2.OperationalError as err:
                    self.logger.error(f"Select error: {err}")

            finally:
                c.close()


    def get_recipe_detail(self, id_recipe:int)->dict:
        """
        Return recipe details

        Attributs
        -------------
        id_recipe: int
            The id of the recipe

        Return
        -------------
        recipe details: dict
            - id
            - title
            - nb_person
            - time_preparation
            - time_rest
            - time_cooking
            - time_total
            - difficulty
            - cost
            - image_link
            - steps: list of str
            - ingredients: dict of ingredient with
                - name
                - quantity
                - unit
        """

        recipe_data = self.request_recipe(id_recipe=id_recipe)
        recipe_data['ingredients'] = self.request_ingredient(id_recipe=id_recipe)
        recipe_data['steps'] = self.request_steps(id_recipe=id_recipe)

        return recipe_data


    def get_ids(self, table:str)->list:
        """
        Get all ids from a table

        Attributs
        -------------
        table: str
            table from which to take the id

        Return
        -------------
        ids: list(int)
            
        """

        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()
                request = f"SELECT id FROM {table};"
                c.execute(request)
                results = c.fetchall()
                list_ids = [result[0] for result in results]

                return list_ids

            except psycopg2.OperationalError as err:
                self.logger.error(f"Select error: {err}")
            
            finally:
                c.close()


    def generate_id(self, table:str)->int:
        """
        Generate a random unique id

        Attributs
        -------------
        table: str
            table in which the id is unique

        Return
        -------------
        id: int
        """

        list_ids = self.get_ids(table)
        random_id = randint(1, 99999)
        while random_id in list_ids:
            random_id = randint(1, 99999)
        return random_id


    def add_user(self, user_info:dict)->None:
        """
        Add user to database

        Attributs
        -------------
        user_info: dict
            Info of user with his ID, name, picture link
        """

        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()
                request = """
                INSERT INTO users (id, name, picture)
                VALUES (%s, %s, %s)
                """

                datas = [
                        user_info['id'],
                        user_info['given_name'],
                        user_info['picture']
                ]

                c.execute(request, datas)
                db_connexion.commit()

            except psycopg2.OperationalError as err:
                self.logger.error(f"Select error: {err}")

            finally:
                c.close()


    def connect_user_recipe(self, id_user:str, id_recipe:int)->None:
        """
        Add a row to user_recipe database.

        Attributs
        -------------
        id_user: str
            id of the user
        id_recipe: int
            id of the recipe
        """
        
        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()
                request = """
                INSERT INTO user_recipe (id_user, id_recipe)
                VALUES (%s, %s)
                """

                datas = [
                        id_user,
                        id_recipe
                ]

                c.execute(request, datas)
                db_connexion.commit()

            except psycopg2.OperationalError as err:
                self.logger.error(f"Select error: {err}")

            finally:
                c.close()


    def add_user_recipe(self, recipe_data:dict, user_id:str)->None:
        """
        Add user's version of recipe in recipe database.
        Call other functions to add ingredients and quantities
        Finally, connect the new recipe and user in recipe_user database

        Attributs
        -------------
        recipe_data: dict
            datas of the recipe
        user_id: str
            id of the user
        """
        print(recipe_data['id'])
        recipe_data['id'] = self.generate_id('recipe')
        self.add_recipe(recipe_data=recipe_data)
        print(recipe_data['id'])
        for ingredient in recipe_data['ingredients']:
            if not self.check_db_by_name(name=ingredient['name'], table='ingredient'):
                ingredient['id'] = self.generate_id('ingredient')
                # Catégorise l'ingrédient
                self.add_ingredient(ingredient=ingredient)

        self.add_quantity(ingredients=recipe_data['ingredients'], id_recipe=recipe_data['id'])

        self.add_steps(steps=recipe_data['steps'], id_recipe=recipe_data['id'])

        self.connect_user_recipe(id_user=str(user_id), id_recipe=recipe_data['id'])


    def get_user_recipes(self, user_id:str)->pd.DataFrame:
        """
        Return all recipes name of user from recipe database

        Attributs
        -------------
        user_id: str
            Id of the user

        Return
        -------------
        DataFrame of recipes with
            - id
            - name
            - picture
        """

        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()
                request = f"""
                select 
                    r.id,
                    r.name,
                    r.image_link 
                from recipe r
                join user_recipe ur on ur.id_recipe = r.id
                where ur.id_user = '{user_id}'
                """

                c.execute(request)
                return pd.DataFrame(c.fetchall(), columns=['id', 'name', 'image_link'])

            except psycopg2.OperationalError as err:
                self.logger.error(f"Select error: {err}")

            finally:
                c.close()

    def request_planner(self, user_id:str)->pd.DataFrame:
        """
        Return all recipes from user's planner

        Attibuts
        -----------
        - user_id: str
            ID of the user
        
        Return
        -----------
        planner_recipe: pd.DataFrame
            DataFrame with recipes informations
        """

        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()
                request = f"""
                SELECT 
                    id,
                    name,
                    nb_person,
                    sweet_salt,
                    time_preparation,
                    time_rest,
                    time_cooking,
                    time_total,
                    difficulty,
                    cost,
                    image_link,
                    country
                FROM recipe r
                JOIN user_recipe ur ON r.id = ur.id_recipe
                WHERE ur.id_user = '{user_id}'
                AND ur.planner = TRUE
                """
                c.execute(request)
                return pd.DataFrame(c.fetchall(), columns=[
                    'id',
                    'name',
                    'nb_person',
                    'sweet_salt',
                    'time_preparation',
                    'time_rest',
                    'time_cooking',
                    'time_total',
                    'difficulty',
                    'cost',
                    'image_link',
                    'country'
                ])

            except psycopg2.OperationalError as err:
                self.logger.error(f"Select error: {err}")

            finally:
                c.close()
    


    def get_profile_info (self, user_id:str) -> dict :

        with DatabaseConnection() as db_connexion :
            try : 
                c = db_connexion.cursor()
                request = f"""
                select name, nb_person, diet, week_lunch, week_we
                from users
                where id  = '{user_id}'
                """
                c.execute(request)
                result = list(c.fetchall()[0])
                result[2] = result[2].split(',') if result[2] != None else result[2]
                return result

            except psycopg2.OperationalError as err:
                self.logger.error(f"Select error: {err}")

            finally:
                c.close()

    def add_user_info(self,user_info, profil_parameters:dict)->None:
        """
        Add user profile info into database

        Attributs
        -------------
        user_info: dict
            Info of user with his ID, name, picture link
        """

        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()
                request = f"""
                UPDATE users
                SET nb_person = {profil_parameters['size']},
                    week_lunch = {profil_parameters['lunch']} ,
                    week_we = {profil_parameters['weekend']}
                WHERE id = '{user_info['id']}'
                """

                c.execute(request)
                db_connexion.commit()

            except psycopg2.OperationalError as err:
                self.logger.error(f"Select error: {err}")

            finally:
                c.close()

