import findMatchSteamAPI
import CSGOsql

#Variables to be passed to function (Should eventually move the given parameters to different file)
key = 'FILL IN YOURS'
steam = 'FILL IN YOURS'
steamKEY = 'FILL IN YOURS'
oldMatchCode = 'FILL IN YOURS'
knownMatchCode = 'FILL IN YOURS'




#This function gives us a list of match codes from steam
myGames = findMatchSteamAPI.giveCodes(key, steam, steamKEY, knownMatchCode)
CSGOsql.addGameCodes(myGames)

