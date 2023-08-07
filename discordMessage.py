import requests, os
#This file should notify the discord that the new game has been added... for now



#In here we want to actually find what discords this should be sent to...
#We might want to send directly to users after a game?



def notify(game = None):
    payload = {
        'content' : "-Summary Time"
    }
    header = {
        'Authorization' : F'Bot {os.environ["DISCORD_TOKEN"]}'
    } 
    requests.post("https://discord.com/api/v9/channels/1091583699746836511/messages", data=payload, headers = header)
    return