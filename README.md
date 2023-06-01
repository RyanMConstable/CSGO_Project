# CSGO_Project
A project to retrieve all information about recent CSGO games given a game code. A frontend will eventually grab the data from the database and display it on a browser. A discord bot will eventually be run as well to further display information.

# main.py
Currently runs the backend admin user interface


### CSGOsql.py 
addGameCodes(gameShareCode): Takes list of game codes, and adds them to a sql table if they're not already in there, returns None
addGameStats(listPlayerStats): Takes a list of lists (players), which gets added to the table if they're not duplicates, returns None
returnAllCodes(): No parameters, returns list of all codes from the first table
findMostRecentGame(steamid): Takes a steamid and returns the most recent game code from that id in the database

### findMatchSteamAPI.py
giveCodes(steamInformation): Takes your steam information, to make an API call, to find all games after a given code up to the newest, returns a list of game codes
generateNewCodes(steamAPIKey, steamID, steamIDKey): Takes your steam information and adds all games since the most recent game, returns None

### getJSONInfo.py
getJSONInfo(gameShareCode): Takes a game code, then downloads the game, analyzes it, and returns a JSON file with info if the code existed
returnGameInfo(gameShareCode, json): Takes a JSON formatted input and outputs the statistics of the 10 players that played a game in the form of a list of lists
clearReplayDir(): Takes nothing and removes all files from the csgo replay directory, util function returns nothing

### dbdatasetup.py
populateStats(): Takes nothing and populates the gamestats table by analyzing and parsing JSON files from every game in the gamecode table

### findGameStats.py
selectCombinedUserStat(stat, steamid): Takes the column name in the database and a steamid and returns the sum of that statistic for the entirety of the table
findNumberOfGames(steamid): Takes a steamid and returns the amount of games saved in the database for the given id
returnAllUserRows: Takes a steamid and returns all rows currently saved within the database of that id

### userCommands.py
Contains commands and functions for admins