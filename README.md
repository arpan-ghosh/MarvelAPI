# MarvelAPI 
## Asynchronous Implementation w/ asyncio, aiohttp, aiosqlite3
*To switch to the synchronous implementation, checkout the `master` branch or switch to the desired tag/release*

## Instructions to Run (Docker)
1. Download the repository, and then run the following commands from the root directory of the repo (marvel-api)
2. `docker build -t marvel-api .`
3. `docker run -it --rm --name my-marvel-app marvel-api /bin/bash`
4. The container should've already executed the task, created, and updated the database. But you can delete the 'marvel.db' database and run the file IntelGatherer to generate this entire database again:

```
rm -f marvel.db
python3 IntelGatherer.py
```

## Summary

This implementation retrieves basic information about Spectrum and stores it in a sqlite database. It then finds all the comics that she's appeared in, and extracts all the characters from those comics, and stores their basic information as well.

This version of the code retrieves the list of comicIDs in which Spectrum appears using requests (basically urrlib). Since we're only making one request to this endpoint with the id of Spectrum, there's really no use to asynchronously call once to this endpoint. We either get the response back or we don't. 

However, the more API intensive part of the code, the calls out to the `/comics/{id}/characters::GET` endpoint to retrieve the list of all the characters that appear in the comics that Spectrum appears in, does happen asynchronously using asyncio and aiohttp. We then store this in the sqlite database asynchronously as well.

This implementation is about ~7 seconds. If we did everything using async, including getting the Spectrum's initial information AND the comicIDs list, it could be slightly faster. But the overhead for such a small list of results could also make it such that it's not really that much faster.

## APIs Queried
1. `GET /v1/public/characters` - Fetches lists of characters given a Name (aka. "Spectrum", save data, especially the character ID)
2. `GET /v1/public/characters/{characterId}/comicsFetches` - lists of comics filtered by a character id (aka. Spectrum's Marvel ID, parse and store comic IDs in memory)
3. `GET /v1/public/comics/{comicId}/characters` - Fetches lists of characters filtered by a comic id (Make a GET here for each comic ID stored from the request above, then parse for the Characters and save their data).

## File Structure
1. There is a `/src/lib` and `/www` directory. 
2. The `src` directory has Python files like constants and a Utility class which has helper functions that could be used by any class. 
3. The `www` directory holds a `rest.py` which are `get()`/`fetch()` functions that make the `Request`/`aiohttp request`. 
4. The main "engine" is an object oriented class titled `IntelGatherer.py` which is stored in the root directory. This class runs a main function that runs the logic to get Spectrum's information and her contacts' information. 
5. The `Dockerfile` is also in the root directory, and it uses the `requirements.txt` file which contain the minimum python3 libraries needed to run the program.

`IntelGatherer.py's` main looks like the following. To only run the first portion, which stores only Spectrum's information, comment out the call to crawl_and_save_contacts():
```
if __name__ == '__main__':
    name = "Spectrum"

    SpectrumIntelGatherer = IntelGatherer(name)

    basic_profile_data = SpectrumIntelGatherer.retrieve_and_save_profile()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(SpectrumIntelGatherer.crawl_and_save_contacts())
```

The output of the run should look similar to the following:

```Bash
TNS8379L:marvel aghosh$ docker build -t marvel-api .
[+] Building 2.4s (12/12) FINISHED                                                                                     
 => [internal] load build definition from Dockerfile                                                              0.0s
 => => transferring dockerfile: 43B                                                                               0.0s
 => [internal] load .dockerignore                                                                                 0.0s
 => => transferring context: 2B                                                                                   0.0s
 => [internal] load metadata for docker.io/library/python:3.8-slim                                                0.8s
 => [auth] library/python:pull token for registry-1.docker.io                                                     0.0s
 => [1/6] FROM docker.io/library/python:3.8-slim@sha256:bdc39f13da35be9a8e592f8f49d12a4552ffd3e90b1fb866f7ab628f  0.0s
 => [internal] load build context                                                                                 0.3s
 => => transferring context: 277.73kB                                                                             0.3s
 => CACHED [2/6] WORKDIR /app                                                                                     0.0s
 => CACHED [3/6] COPY requirements.txt requirements.txt                                                           0.0s
 => CACHED [4/6] RUN pip3 install -r requirements.txt                                                             0.0s
 => CACHED [5/6] RUN apt-get update && apt-get install -y --no-install-recommends                                 0.0s
 => [6/6] COPY . .                                                                                                0.8s
 => exporting to image                                                                                            0.4s
 => => exporting layers                                                                                           0.3s
 => => writing image sha256:478c184e81b1d6cef259127edcf74198609992d2622ae802e9cfb7c459e69326                      0.0s
 => => naming to docker.io/library/marvel-api                                                                     0.0s
TNS8379L:marvel aghosh$ docker run -it --rm --name my-marvel-app marvel-api /bin/bash
root@874846bd09a3:/app# python3 IntelGatherer.py 
Retrieving Spectrum's Basic Profile Information...
Inserting Character: Spectrum
Finding All of Spectrum's 1st Degree Contacts...
Gathering all comics Spectrum's appeared in...
Found 33 comics Spectrum's appeared in...
Searching for all characters in comics...
Total time to run: 6 seconds
Elapsed Time: 6
root@874846bd09a3:/app# sqlite3 marvel.db 'SELECT * FROM MarvelCharacter WHERE name="Spectrum";'
1|Spectrum|1010705||http://i.annihil.us/u/prod/marvel/i/mg/9/00/4c0030bee8c86.jpg|1618195093.64277
root@874846bd09a3:/app# sqlite3 marvel.db 
SQLite version 3.27.2 2019-02-25 16:06:06
Enter ".help" for usage hints.
sqlite> .mode line
sqlite> select count(*) from marvelcharacter;
count(*) = 41
```
