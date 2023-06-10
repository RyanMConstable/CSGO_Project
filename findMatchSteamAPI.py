import requests, time, os
try:
    import CSGOsql
except:
    from . import CSGOsql

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
    newestCode = CSGOsql.findMostRecentGame(steamID)
    if newestCode == None:
        return
    codeList = giveCodes(steamID, newestCode, steamidkey)
    return codeList