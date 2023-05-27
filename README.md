# CSGO_Project
Currently to set up, you need to fill in the strings within main.py
All it does is add game codes to a database (the database sql commands are hidden so that you cannot see my login, this is an early edition)

# main.py
Run this to run the project



# Reminder:
Remove files after they are created...

### CSGOsql.py 
addGameCodes: Takes list of game codes, and adds them to a sql table if they're not already in there
addGameStats: This takes a list of 10 lists (players), which gets added to the table if they're not duplicates

### findMatchSteamAPI.py
giveCodes: Takes your steam information, to make an API call, to find all games after a given code up to the newest

### getJSONInfo.py
getJSONInfo: Takes a game code, then downloads the game, analyzes it, and returns a JSON file with info if the code existed, returns 'Failure' otherwise
returnGameInfo: Takes a JSON formatted input and outputs the statistics of the 10 players that played a game


