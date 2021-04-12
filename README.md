# MarvelAPI
## Sequential, synchronous requests with Requests (urllib)
*To switch to the asynchronous implementation, checkout the `dev` branch.*

This implementation retrieves basic information about Spectrum and stores it in a sqlite database. It then finds all the comics that she's appeared in, and extracts all the characters from those comics, and stores their basic information as well.

This is a O(n^2) implementation (see crawl_and_save_contacts()). For each comic that Spectrum appeared in, I make a REST GET call to retrieve all the characters in that comic. Then, for each character in the returned results for the particular comic in question, I store their information in a dictionary hashed on the marvel_id of the character. (A for loop inside a for loop).

This is why in this implementation, the entire process takes about ~11 seconds on my MacBook Pro. The responses come back, and only then does the program attempt to request the next REST GET call to get characters in the next comic id. In otherwords, notice how the HTTP GET requests are occurring sequentially.

To improve this, we'd want to make multiple asynchronous requests and/or leverage multi-threading/multi processing using Workers and Pools/ThreadPools. Since I think performing concurrent requests using multi-threading or multi-processing on top of async requests will be overkill for this particular project, the next implementation will solely use asyncio to make asynchronous requests to speed up the entire process.

