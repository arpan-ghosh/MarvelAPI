import hashlib
import pprint
import sqlite3
import time
import aiosqlite3

from www.rest import *
from sqlite3 import Error
from src.lib.defines import *


class Utility:
    db = ''
    db_handle = sqlite3.connect('marvel.db')

    def __init__(self):
        pass

    def __del__(self):
        if self.db_handle:
            self.db_handle.close()
            print("The SQLite connection is closed")

    def initialize_db(self):
        db = self.create_connection('marvel.db')
        self.create_tables(db)
        db.commit()

        self.db_handle = sqlite3.connect('marvel.db')

    def extract_basic_info_from_response(response):
        marvel_id = ""
        name = ""
        description = ""
        image = ""

        for key in response['data']['results']:
            name = key['name']
            marvel_id = key['id']
            description = key['description']
            image = key['thumbnail']['path'] + "." + key['thumbnail']['extension']

        character = dict(name=name, id=marvel_id, description=description, picture=image)

        return character

    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_tables(connection):
        try:
            c = connection.cursor()
            c.execute(sql_create_character_table)
        except Error as e:
            print(e)

    def store_character_data(self, data):
        self.initialize_db(self)

        if len(data) > 1:
            for id, character in data:
                print("Found a Spectrum contact! Inserting Character: " + str(character['name']))
                self.insert_into_db(self, character)
        else:
            print("Inserting Character: " + str(data[0]['name']))
            self.insert_into_db(self, data[0])

        self.db_handle.commit()

    @staticmethod
    async def async_store_character_data(data):
        sqlite_insert_with_param = """INSERT OR IGNORE INTO MarvelCharacter
                             (marvelID, name, description, picture, createdTime) 
                             VALUES (?, ?, ?, ?, ?);"""
        data_tuple = (data['id'], data['name'], data['description'], data['picture'], time.time())

        async with aiosqlite3.connect('marvel.db') as db:
            await db.execute(sqlite_insert_with_param, data_tuple)
            await db.commit()

    @staticmethod
    def insert_into_db(self, data):
        try:
            sqlite_insert_with_param = """INSERT OR IGNORE INTO MarvelCharacter
                                 (marvelID, name, description, picture, createdTime) 
                                 VALUES (?, ?, ?, ?, ?);"""

            data_tuple = (data['id'], data['name'], data['description'], data['picture'], time.time())
            self.db_handle.cursor().execute(sqlite_insert_with_param, data_tuple)

        except sqlite3.Error as error:
            print("Failed to insert basic Character data into sqlite table", error)

    @staticmethod
    def merge_dictionaries(dict1, dict2):
        ''' Merge dictionaries and keep values of common keys in list'''
        dict3 = {**dict1, **dict2}
        for key, value in dict3.items():
            if key in dict1 and key in dict2:
                dict3[key] = [value, dict1[key]]

        return dict3

    @staticmethod
    def write_json(data, filename):
        with open(filename, "w") as f:
            json.dump(data, f, indext=4)

    @staticmethod
    def generate_hash():
        public_key = 'b9530947af28f24155b1f3822f706584'
        private_key = '19d7969661e220260832c7dfc20f7b74999de9e9'
        # public_key = '01afb308dab4d57fcab977371007c0a6'
        # private_key = 'c8ba611bb5ea061d548925548e447b4664c81e16'
        ts = str(int(time.time()))
        string_to_hash = ts + private_key + public_key
        return "?ts=" + ts.strip(), "&hash=" + hashlib.md5(string_to_hash.strip().encode('utf-8')).hexdigest()

    @staticmethod
    def __get_pretty_printer__() -> object:
        return pprint.PrettyPrinter(indent=4)
