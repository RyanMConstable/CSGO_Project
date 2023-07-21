import requests, os, logging
#This file should notify the discord that the new game has been added... for now

def notify():
    payload = {
        'content' : "Game Added"
    }
    header = {
        'Authorization' : F'Bot {os.environ["DISCORD_TOKEN"]}'
    } 
    requests.post("https://discord.com/api/v9/channels/1105249488702030026/messages", data=payload, headers = header)
    return