import asyncio
import aiohttp

from src.lib.Utility import *
from www import rest


class IntelGatherer:
    _character = ""
    _characterID = ""
    characters = {}

    def __init__(self, character):
        self.Utility = Utility
        self._character = character

    def retrieve_and_save_profile(self):
        basic_profile = {0: self.get_basic_info(self)}
        Utility.store_character_data(self.Utility, basic_profile)

        return basic_profile

    @staticmethod
    def get_basic_info(self):
        if not self._character:
            self._character = self._characterID

        response = rest.get_character_by_name(self._character, ENDPOINT_CHARACTERS)

        data = Utility.extract_basic_info_from_response(response)
        self._characterID = data['id']

        return data

    @staticmethod
    def get_all_comics_for_character(character_id):
        comics = []
        response = rest.get_all_comics(character_id)

        # Parse Response and store the comic ID for each entry returned in the data results
        for comic in response['data']['results']:
            comics.append(comic['id'])

        return comics

    async def crawl_and_save_contacts(self, character_id=None):
        """Gets and saves every Marvel character in the comics that Spectrum's appeared in

            Parameters
            ----------
            character_id : str
                Use the passed in character id if, otherwise get it from the class object variable


            Returns
            -------
            results : list
                a list of the characters and their relevant metadata
            """

        results = []
        session = aiohttp.ClientSession()

        if not character_id:
            character_id = self._characterID

        print("Gathering all comics appeared in...")
        all_comics = self.get_all_comics_for_character(character_id)

        print("Found " + str(len(all_comics)) + " comics appeared in...")
        print("Searching for all characters in comics...")

        for comic_id in all_comics:
            data = await rest.get_all_characters_in_comic(comic_id, session)

            for result in data['data']['results']:
                desired_fields = {'id': result['id'], 'name': result['name'], 'description': result['description'],
                                    'picture': result['thumbnail']['path'] + "." + result['thumbnail']['extension']}

                if desired_fields not in results:
                    results.append(desired_fields)

        await session.close()

        for character in results:
            await Utility.async_store_character_data(character)

        return results


if __name__ == '__main__':
    name = "Spider Man"

    SpiderManIntelGatherer = IntelGatherer(name)

    print("Retrieving " + name + "\'s" + " Basic Profile Information...")

    basic_profile_data = SpiderManIntelGatherer.retrieve_and_save_profile()

    print("Finding All of Spider Man's 1st Degree Contacts...")

    start_time = int(time.time())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(SpiderManIntelGatherer.crawl_and_save_contacts())

    print("Total time to run: " + str((int(time.time()) - start_time)) + " seconds")

    elapsed_time = int(time.time()) - start_time

    print("Elapsed Time: " + str(elapsed_time))
