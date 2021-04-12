# Required API Constants
API_URL = "https://gateway.marvel.com/v1/public/"
API_HOST = "https://developer.marvel.com"
#API_KEY = "b9530947af28f24155b1f3822f706584"
API_KEY = "01afb308dab4d57fcab977371007c0a6"
API_KEY_PARAMS = "apikey=" + API_KEY

# Limits
DAILY_RATE_LIMIT = 3000
MAX_RECORDS_ALLOWED_PER_ENDPOINT_LIMIT = 100

# Endpoints
ENDPOINT_CHARACTERS = 'characters'
ENDPOINT_COMICS = 'comics'

# Database Schemas
sql_create_character_table = """ CREATE TABLE IF NOT EXISTS MarvelCharacter (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    marvelID integer UNIQUE,
                                    description text NULL,
                                    picture text NOT NULL,
                                    createdTime text NOT NULL
                                ); """

