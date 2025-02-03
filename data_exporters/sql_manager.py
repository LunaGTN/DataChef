import boto3
from botocore.exceptions import ClientError
import json
import logging
import psycopg2
from typing import List
import re

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    encoding="utf-8",    
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M"
)

logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("s3transfer").setLevel(logging.WARNING)


def get_secret():

    secret_name = "rds_datachef"
    region_name = "eu-west-3"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    
    return json.loads(secret)


class DatabaseConnection():
    def __init__(self):
        self.connexion_data = get_secret()

    def __enter__(self):
        self.db_connector = psycopg2.connect(
            host=self.connexion_data['host'],
            database=self.connexion_data['engine'],
            user=self.connexion_data['username'],
            password=self.connexion_data['password']
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


    def check_db(self, id:str, table:str)->bool:
        """
            Check if an ingredient already exists in database

            Attribut
            -----------
            id: id of the ingredient
            db: database to check 
                ingredient
                recipe

            Return
            -----------
            boolean
        """

        with DatabaseConnection() as db_connexion:
            try :
                c = db_connexion.cursor()
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

    
    def add_recipe(self, recipe_data)->None:
        """
        Add recipe to recipe database 

        Attributs
        -------------
        recipe_data: json
            titre: str
            lien: str
            id: str
            temps_preparation: str
            tems_repos: str
            temps_cuisson: str
            image: str
            nb_personne: str
            temps_total: str
            difficulty: str
            cost: str
            steps: list of str
            ingredients: list of dict
        """

        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()

                request = """
                INSERT INTO recipe (id, name, nb_person, time_preparation, time_rest, time_cooking, time_total, difficulty, cost, image_link)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            
                datas = (
                    int(recipe_data['id']),
                    recipe_data['titre'].capitalize(),
                    int(recipe_data['nb_personne']),
                    self.fomat_time(recipe_data['temps_preparation']),
                    self.fomat_time(recipe_data['tems_repos']),
                    self.fomat_time(recipe_data['temps_cuisson']),
                    self.fomat_time(recipe_data['time_total']),
                    recipe_data['difficulty'],
                    recipe_data['cost'],
                    recipe_data['image'],
                )

                c.execute(request, datas)
                db_connexion.commit()

                self.logger.info(f"{recipe_data['titre']} was successfully add to database\n")
        
            except psycopg2.OperationalError as err:
                self.logger.error(f"Insert error: {err}")

            finally:
                c.close()




    def add_steps(self, id_recipe:int, steps:List[str])->None:
        """
        Add recipe to recipe database 

        Attributs
        -------------
        id_recipe: str
            id of recipe
        steps: list of str
            list of steps
        """
        
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

                self.logger.info(f"Steps were successfully add to database\n")

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
            quantite: float
                quantity of the ingredient
            unite: str
                unity for this quantity
        """
        
        with DatabaseConnection() as db_connexion:
            try : 
                c = db_connexion.cursor()

                request = """
                INSERT INTO ingredient (id, name)
                VALUES (%s, %s)
                """
                
                datas = [
                        int(ingredient['id']),
                        ingredient['name'].capitalize()
                ]

                c.execute(request, datas)
                db_connexion.commit()

                self.logger.info(f"{ingredient['name'].capitalize()} was successfully add to database")

            except psycopg2.OperationalError as err:
                self.logger.error(f"Insert error: {err}")

            finally:
                c.close()


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

        with DatabaseConnection() as db_connexion:
            c = db_connexion.cursor()
            request = """INSERT INTO ingredient_recipe (id_recipe, id_ingredient, quantity, unit)
            VALUES (%s, %s, %s, %s)"""

            datas =[
                (int(id_recipe),
                int(ingredient['id']),
                int(ingredient['quantity']),
                ingredient['unit']
                ) for ingredient in ingredients
            ]

            try:
                for row in datas:
                    c.execute(request, row)
                    db_connexion.commit()                
        
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
            lien: str
                url of recipe to Marmiton
            id: int
                id of recipe
            temps_preparation: str
                preparation time can be XXmin, XXh, XXhXXmin format
            tems_repos: str
                rest time, can be XXmin, XXh, XXhXXmin format
            temps_cuisson: str
                cooking time can be XXmin, XXh, XXhXXmin format
            image: str
                url of image 
            nb_personne: int
                number of people for whom this recipe is intended
            time_total: str
                total_time can be XXmin, XXh, XXhXXmin format
            difficulte: str
                difficulty of recipe
            cout: str
                cost for this recipe
            etapes: list of str
                list of steps for this recipe
            ingredients: list of dict
                list of ingredients with id, name, quantity and unite for each
        """

        if not self.check_db(id=recipe_data['id'], table="recipe"):
            self.add_recipe(recipe_data=recipe_data)
            self.add_steps(id_recipe=recipe_data['id'], steps=recipe_data['etapes'])
            
            for ingredient in recipe_data['ingredients']:

                if not self.check_db(id=ingredient['id'], table="ingredient"):
                    self.add_ingredient(ingredient=ingredient)
                else:
                    self.logger.info(f"{ingredient['nom']} is already in database")

            self.add_quantity(ingredients=recipe_data['ingredients'], id_recipe=recipe_data['id'])
                
        else:
            self.logger.info(f"{recipe_data['titre']} is already in database")

