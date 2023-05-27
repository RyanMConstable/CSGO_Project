import requests, time

#Return list of game codes since given code (include code given)
def giveCodes(steamAPIKey, steamID, steamIDKey, knownCode):
    gamesList = []
    gamesList.append(knownCode)
    sharedUrl = 'https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1?key={}&steamid={}&steamidkey={}&knowncode={}'.format(steamAPIKey, steamID, steamIDKey, knownCode)
    r = requests.get(sharedUrl)

    #Create loop until status code is not 200
    #This will find every code until the newest, or it times out with 429 HTTP status code
    while r.status_code == 200:
        time.sleep(1/5)
        newCode = r.json()['result']['nextcode']
        #print(r.status_code, newCode)
        gamesList.append(newCode)
        sharedUrl = 'https://api.steampowered.com/ICSGOPlayers_730/GetNextMatchSharingCode/v1?key={}&steamid={}&steamidkey={}&knowncode={}'.format(steamAPIKey, steamID, steamIDKey, newCode)
        r = requests.get(sharedUrl)
    #Print Ending Code
    print("Ending status: {}".format(r.status_code))
    return gamesList
