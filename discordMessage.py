import requests, os
#This file should notify the discord that the new game has been added... for now

def notify():
    payload = {
        'content' : "-Summary Time"
    }
    header = {
        'Authorization' : F'Bot {os.environ["DISCORD_TOKEN"]}'
    } 
    #Test discord directly below
    #requests.post("https://discord.com/api/v9/channels/1105249488702030026/messages", data=payload, headers = header)
    
    #Our main discord
    requests.post("https://discord.com/api/v9/channels/1091583699746836511/messages", data=payload, headers = header)
    return