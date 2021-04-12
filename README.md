# MarvelAPI 
## Asynchrnous Implementation w/ asyncio, aiohttp, aiosqlite3

This version of the code retrieves the list of comicIDs in which Spectrum appears using requests (not async). Since we're only making one request to this endpoint with the id of Spectrum, there's really no use to asynchronously call once to this endpoint. We either get the response back or we don't.

However, the more API intensive part of the code, the calls out to the /comics/{id}/characters::GET endpoint to retrieve the list of all the characters that appear in the comics that Spectrum appears in, does happen asynchronously using asyncio and aiohttp. We then store this in the sqlite database asynchronously as well.

This implementation is about ~7 seconds. If we did everything using async, including getting the Spectrum's initial information AND the comicIDs list, it could be slightly faster. But the overhead for such a small list of results could also make it such that it's not really that much faster.
