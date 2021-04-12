# MarvelAPI 
## Asynchrnous Implementation w/ asyncio, aiohttp, aiosqlite3

This version of the code retrieves the list of comicIDs in which Spectrum appears using requests (not async). Since we're only making one request to this endpoint with the id of Spectrum, there's really no use to asynchronously call once to this endpoint. We either get the response back or we don't.

However, the more API intensive part of the code, the calls out to the `/comics/{id}/characters::GET` endpoint to retrieve the list of all the characters that appear in the comics that Spectrum appears in, does happen asynchronously using asyncio and aiohttp. We then store this in the sqlite database asynchronously as well.

This implementation is about ~7 seconds. If we did everything using async, including getting the Spectrum's initial information AND the comicIDs list, it could be slightly faster. But the overhead for such a small list of results could also make it such that it's not really that much faster.

## Docker instructions
1. Download the repository, and then run the following commands from the root directory of the repo (marvel-api)
2. `docker build -t marvel-api .`
3. `docker run -it --rm --name my-marvel-app marvel-api /bin/bash`
4. The container should've already executed the task and updated the database. If you want, delete the 'marvel.db' database and run the file IntelGatherer.

```
rm -f marvel.db
python3 IntelGatherer.py
```

IntelGatherer.py's main looks like the following:
```
if __name__ == '__main__':
    name = "Spectrum"

    SpectrumIntelGatherer = IntelGatherer(name)

    basic_profile_data = SpectrumIntelGatherer.retrieve_and_save_profile()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(SpectrumIntelGatherer.crawl_and_save_contacts())
```

The output of the run should look similar to the following:

```
root@8763771d5996:/app# python3 IntelGatherer.py 
Retrieving Spectrum's Basic Profile Information...
Inserting Character: Spectrum
Finding All of Spectrum's 1st Degree Contacts...
Gathering all comics Spectrum's appeared in...
Found 33 comics Spectrum's appeared in...
Searching for all characters in comics...
Total time to run: 6 seconds
Elapsed Time: 6
```
