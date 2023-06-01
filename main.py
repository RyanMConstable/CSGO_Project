#! C:\Users\ry4nm\AppData\Local\Programs\Python\Python311\python.exe
import findMatchSteamAPI
import CSGOsql
import getJSONInfo
import dbdatasetup
import userCommands

#Variables to be passed to functions
key = ''
steam = ''
steamKEY = ''
knownMatchCode = ''


#This function gives us a list of match codes from steam
#myGames = findMatchSteamAPI.giveCodes(key, steam, steamKEY, knownMatchCode)
#CSGOsql.addGameCodes(myGames)

#This populates the databases if there is nothing in them, need a better way of doing this
#dbdatasetup.populateStats()

#This function call adds all game codes since the most recent game code in the table to the code table
#CSGOsql.addGameCodes(findMatchSteamAPI.generateNewCodes(key, steam, steamKEY))


#Admin backend command line interface
userCommands.mainChainCommand()