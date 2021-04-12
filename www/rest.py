import json

import requests

from src.lib.Utility import *
from src.lib.defines import *


def get_headers():
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'Origin': API_HOST,
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': API_HOST,
        'Accept-Language': 'en-US,en;q=0.9'
    }

    return headers


def get_character_by_name(character, endpoint):
    params = "?name=" + character + '&' + API_KEY_PARAMS
    url = API_URL + endpoint + params

    try:
        response = requests.request("GET", url, headers=get_headers(), data=None)
        json_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        return e

    return json_data


def get_all_comics(character_id):
    limit = MAX_RECORDS_ALLOWED_PER_ENDPOINT_LIMIT

    url = API_URL + ENDPOINT_CHARACTERS + "/" + str(character_id) + "/" + ENDPOINT_COMICS

    try:
        response = requests.request("GET", url + "?limit=" + str(limit) + '&' + API_KEY_PARAMS, headers=get_headers(),
                                    data=None)
        json_data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        return e

    count = json_data['data']['count']
    total = json_data['data']['total']

    while count != total:
        modified_url = url + "?offset=" + str(count) + '&' + API_KEY_PARAMS
        response = requests.request("GET", modified_url, headers=get_headers(), data=None)
        new_json_data = json.loads(response.text)

        count += new_json_data['data']['count']
        json_data['data']['results'].extend(new_json_data['data']['results'])

    return json_data


def generate_characters_in_comic_url(comic_id):
    ts, hash = Utility.generate_hash()

    return API_URL + ENDPOINT_COMICS + "/" + str(comic_id) + "/" + ENDPOINT_CHARACTERS + ts + "&" + API_KEY_PARAMS + hash


async def get_all_characters_in_comic(comic_id, session):
    url = API_URL + ENDPOINT_COMICS + "/" + str(comic_id) + "/" + ENDPOINT_CHARACTERS + "?" + API_KEY_PARAMS

    async with session.get(url, headers=get_headers()) as resp:
        resp_text = await resp.text()
        return json.loads(resp_text)
