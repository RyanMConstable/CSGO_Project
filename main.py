

import findMatchSteamAPI
import CSGOsql
import getJSONInfo
import dbdatasetup

#Variables to be passed to function (Should eventually move the given parameters to different file)
key = '0B37DAADAD3282EF893D03A43D3CA522'
steam = '76561198068939539'
steamKEY = '7B6T-RSWHW-RNNK'
oldMatchCode = 'FILL IN YOURS'
knownMatchCode = 'FILL IN YOURS'


#This function gives us a list of match codes from steam
#myGames = findMatchSteamAPI.giveCodes(key, steam, steamKEY, knownMatchCode)
#CSGOsql.addGameCodes(myGames)

#This populates the databases if there is nothing in them, need a better way of doing this
#dbdatasetup.populateStats()
