from mysql.connector import connect, Error
import requests
# import json
from getpass import getpass

create_db_query = "CREATE DATABASE pokemon_list"
create_pokemon_table_query = """
    CREATE TABLE IF NOT EXISTS pokemon(
        id INT PRIMARY KEY,
        name VARCHAR(20),
        hp INT, attack INT,
        defense INT,
        special_attack INT,
        special_defense INT,
        speed INT,
        first_type VARCHAR(20),
        second_type VARCHAR(20),
        sprite_url VARCHAR(20)
        ) ;
"""

try:
    with connect(
        host="localhost",
        # user=input("Enter username: "),
        password=getpass("Enter password: "),
        user="root",
        database="pokemon_list",
    ) as connection:
        print(connection)
        with connection.cursor() as cursor:
            for number in range(5,133):
                pokemonChoiceData = requests.get(f"https://pokeapi.co/api/v2/pokemon/{number}/")

                id = pokemonChoiceData.json()['id']
                name = pokemonChoiceData.json()['name']
                hp = pokemonChoiceData.json()['stats'][0]['base_stat']
                attack = pokemonChoiceData.json()['stats'][1]['base_stat']
                defense = pokemonChoiceData.json()['stats'][2]['base_stat']
                special_attack = pokemonChoiceData.json()['stats'][3]['base_stat']
                special_defense = pokemonChoiceData.json()['stats'][4]['base_stat']
                speed = pokemonChoiceData.json()['stats'][5]['base_stat']
                sprite_url = pokemonChoiceData.json()['sprites']['front_shiny']
                first_type = pokemonChoiceData.json()['types'][0]['type']['name']
                try:
                    second_type = pokemonChoiceData.json()['types'][1]['type']['name']
                except IndexError:
                    second_type = "NULL"

                insert_row_query = f"""
                    INSERT IGNORE INTO pokemon(id, name, hp, defense, special_attack, special_defense, speed, first_type, second_type)
                    VALUES
                        ({id}, "{name}", {hp}, {defense}, {special_attack}, {special_defense}, {speed}, "{first_type}", "{second_type}");
                """
                cursor.execute(insert_row_query)
                connection.commit()
except Error as e:
    print(e)
