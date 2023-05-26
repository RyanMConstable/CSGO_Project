import os


#Need a function to use the path
#1 download command to download with share code
#2 Find where it downloaded, analyze it
#3 Download into JSON file
#4 Parse JSON file for DATA
#5 Add information to database
#6 Delete Files
def getJSONInfo(code):
    pathToCSGODm = os.path.abspath(r'C:/\"Program Files (x86)\"/\"CSGO Demos Manager\"/csgodm.exe')
    pathToCSGOreplays = os.path.abspath(r'C:/Program Files (x86)/Steam/steamapps/common/Counter-Strike Global Offensive/csgo/replays')
    os.system(pathToCSGODm + " download " + str(code))
    files = os.listdir(pathToCSGOreplays)
    pathToAnlyze = None
    for file in files:
        if file.split(".")[-1] == "dem":
            pathToAnlyze = pathToCSGODm + " analyze " + r'C:/"Program Files (x86)"/Steam/steamapps/common/"Counter-Strike Global Offensive"/csgo/replays/' + file
            os.system(pathToAnlyze)
    pathToJSON = None
    if pathToAnlyze:
        pathToJSON = pathToCSGODm + " json " + r'C:/"Program Files (x86)"/Steam/steamapps/common/"Counter-Strike Global Offensive"/csgo/replays/'
        os.system(pathToJSON)
    if pathToJSON:
        pathToJSON = pathToCSGODm + " json " + r'C:/"Program Files (x86)"/Steam/steamapps/common/"Counter-Strike Global Offensive"/csgo/replays/' + file
        w = open(pathToCSGOreplays + "/" + file)
        info = w.read()
        w.close()
        return info
    return "Failure"