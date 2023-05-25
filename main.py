import findMatchSteamAPI

#Variables to be passed to function (Should eventually move the given parameters to different file)
key = 'Not my own key'
steam = '76561198068939539'
steamKEY = 'No idea what this one does'
#The old match code will run 231 or more games
oldMatchCode = 'CSGO-s4AOd-ax7Ph-mVi54-Ac77w-vrzED'
knownMatchCode = 'CSGO-TmtKB-aMoKk-FqZYO-ZJO3z-ozioE'




#This function gives us a list of match codes from steam
findMatchSteamAPI.giveCodes(key, steam, steamKEY, knownMatchCode)
