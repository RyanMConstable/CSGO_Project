import requests, time, os, simplesql

steamAPIKey = os.environ["STEAM_API_KEY"]

#Return list of game codes since given code (include code given)
def giveCodes(steamID, knownCode, steamidkey):
    gamesList = []
    gamesList.append(knownCode)
    sharedUrl = 'https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1?key={}&steamid={}&steamidkey={}&knowncode={}'.format(steamAPIKey, steamID, steamidkey, knownCode)
    r = requests.get(sharedUrl)
    #Create loop until status code is not 200
    #This will find every code until the newest, or it times out with 429 HTTP status code
    while r.status_code == 200 or r.status_code == 429:
        if r.status_code == 429:
            time.sleep(2)
        time.sleep(1/5)
        newCode = r.json()['result']['nextcode']
        gamesList.append(newCode)
        sharedUrl = 'https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1?key={}&steamid={}&steamidkey={}&knowncode={}'.format(steamAPIKey, steamID, steamidkey, newCode)
        r = requests.get(sharedUrl)
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

#This is still in use, should depreciate it
def validateUser(steamid, steamidkey):
    testRequest = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={}&steamid={}'.format(steamAPIKey, steamid)
    if requests.get(testRequest).status_code != 200:
        return False
    return True



#A true validation, this should replace previous validation for only checking a users steamid exists
def trueValidation(steamID, steamidkey, knownCode):
    testRequest = 'https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1?key={}&steamid={}&steamidkey={}&knowncode={}'.format(steamAPIKey, steamID, steamidkey, knownCode)
    if requests.get(testRequest).status_code in [202,200]:
        return True
    return False