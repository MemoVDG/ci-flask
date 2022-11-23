import json
import sqlite3 as sql
from sqlite3 import Cursor
from typing import NoReturn


class DatabaseManager:

    def get_connecion(self) -> Cursor:
        # TODO: DB name from .env
        connection = sql.connect('tours.db', isolation_level=None)
        connection.commit()
        return connection.cursor()

    def close_connection(
            self,
            connection: Cursor,
    ) -> NoReturn:
        connection.close()

    def create_users(self) -> NoReturn:
        users_json = open('mocks/users.json')
        users = json.load(users_json)
        values = ''
        for user in users:
            values += f"{user['full_name'], user['phone'], user['user_name']},"

        values = values[:-1]
        query = f"""INSERT INTO Users (full_name, phone, user_name) VALUES {values};"""
        connection = self.get_connecion()
        connection.execute(query)
        self.close_connection(connection=connection)

    def create_cities(self) -> NoReturn:
        cities_json = open('mocks/cities.json')
        cities = json.load(cities_json)
        values = ''
        for city in cities:
            values += f"(\'{city['name']}\'),"
            if city['country'].startswith('B'):
                break

        values = values[:-1]
        query = f"""INSERT INTO Cities (name) VALUES {values};"""
        connection = self.get_connecion()
        connection.execute(query)
        self.close_connection(connection=connection)

    def create_database(self):
        connection = self.get_connecion()

        connection.execute("""CREATE TABLE Cities (
                           CityID INTEGER PRIMARY KEY AUTOINCREMENT,
                           name varchar(100)
                           );"""
                           )
        connection.execute("""CREATE TABLE Tours (
                           TourID INTEGER PRIMARY KEY AUTOINCREMENT,
                           CityID INTEGER,
                           UserID INTEGER,
                           name VARCHAR(100),
                           description VARCHAR(150),
                           days VARCHAR(100),
                           FOREIGN KEY(CityID) REFERENCES Cities(CityID),
                           FOREIGN KEY(UserID) REFERENCES Users(UserID)
                           );"""
                           )
        connection.execute("""CREATE TABLE Users (
                           UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                           full_name VARCHAR(100),
                           phone VARCHAR(20),
                           user_name VARCHAR(10)
                           );"""
                           )
        self.close_connection(connection=connection)

    def create_tours(self) -> NoReturn:
        tours_json = open('mocks/tours.json')
        tours = json.load(tours_json)

        values = ''
        for tour in tours:
            values += f"{tour['city_id'], tour['user_id'], tour['name'], tour['description'], tour['days']},"

        values = values[:-1]
        query = f"""INSERT INTO Tours (CityID, UserID, name, description, days) VALUES {values};"""
        connection = self.get_connecion()
        connection.execute(query)
        self.close_connection(connection=connection)
