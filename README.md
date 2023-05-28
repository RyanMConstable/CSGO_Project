# CSGO_Project
A project to retrieve all information about recent CSGO games given a game code. A frontend will eventually grab the data from the database and display it on a browser.

# main.py
Run this to run the project, currently only populates a table for you



# Reminder:
Remove files after they are created...

### CSGOsql.py 
addGameCodes(gameShareCode): Takes list of game codes, and adds them to a sql table if they're not already in there
addGameStats(listPlayerStats): This takes a list of 10 lists (players), which gets added to the table if they're not duplicates
returnAllCodes(): Returns list of all codes from the first table

### findMatchSteamAPI.py
giveCodes(steamInformation): Takes your steam information, to make an API call, to find all games after a given code up to the newest

### getJSONInfo.py
getJSONInfo(gameShareCode): Takes a game code, then downloads the game, analyzes it, and returns a JSON file with info if the code existed, returns 'Failure' otherwise
returnGameInfo(gameShareCode, json): Takes a JSON formatted input and outputs the statistics of the 10 players that played a game
clearReplayDir(): Takes nothing and removes all files from the csgo replay directory, util function.

### dbdatasetup.py
populateStats(): Takes nothing and populates the gamestats table by analyzing and parsing JSON files from every game in the gamecode table


