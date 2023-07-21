import requests, time, os, simplesql, logging

steamAPIKey = os.environ["STEAM_API_KEY"]

#Return list of game codes since given code (include code given)
def giveCodes(steamID, knownCode, steamidkey):
    gamesList = []
    gamesList.append(knownCode)
    sharedUrl = 'https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1?key={}&steamid={}&steamidkey={}&knowncode={}'.format(steamAPIKey, steamID, steamidkey, knownCode)
    r = requests.get(sharedUrl)
    #Create loop until status code is not 200
    #This will find every code until the newest, or it times out with 429 HTTP status code
    while r.status_code == 200:
        time.sleep(1/5)
        newCode = r.json()['result']['nextcode']
        gamesList.append(newCode)
        sharedUrl = 'https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1?key={}&steamid={}&steamidkey={}&knowncode={}'.format(steamAPIKey, steamID, steamidkey, newCode)
        r = requests.get(sharedUrl)
    #Print Ending Code
    print("Ending status: {}".format(r.status_code))
    return gamesList

#This function takes your steam info and generates new codes by finding the newest code from the database
#Returns a list of new codes or None if it's the newest
def generateNewCodes(steamID, steamidkey):
    newestCode = simplesql.findMostRecentGame(steamID)
    if newestCode == None:
        return
    codeList = giveCodes(steamID, newestCode, steamidkey)
    codeList.remove(newestCode)
    return codeList

#Test to validate a steam id, need to find a way to also validate steamidkey
def validateUser(steamid, steamidkey):
    testRequest = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={}&steamid={}'.format(steamAPIKey, steamid)
    if requests.get(testRequest).status_code != 200:
        return False
    return True