import json
import time

import requests

# Check your server ID on the battlemetrics URL for your server https://www.battlemetrics.com/servers/squad/999999 - That last one number is the server ID
serverID = "4078917"
# BM API URL where we get the data from
ServerInfoUrl = "https://api.battlemetrics.com/servers/" + serverID
# How many seconds between server check (and recording, if you put say, 1 second, it will record one entry per second CAREFUL with disk space. 60 seconds should result on an extreme data gather if you want to check what are the maps that works ffor your server
interval = 60
# Minimum amount of players needed to record data to the CSV
minimumPlayers = 10

# File generation stuff - Adding date and time to the filename
fileTimestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
fileName = fileTimestamp + "MapStats.csv"
file = open(fileName, "w")

# Writing the CSV header - Column names
file.write("Date;Map name;Amount of players")

# Opening the file in append mode, so we add lines to the file
file = open(fileName, "a")

# Infinite loop to keep recording until we stop the script
while True:
    # Generating the date for the current CSV row
    date = time.strftime("%d/%m/%Y %H:%M:%S")
    # Getting the data from the battlemetrics API and converting it to an json object
    jsonResponse = json.loads(requests.get(ServerInfoUrl).text)

    # Getting the amount of players
    playerAmountInt = jsonResponse["data"]["attributes"]["players"]
    # Converting it to string
    playerAmount = str(playerAmountInt)
    # Getting the mapname
    mapName = jsonResponse["data"]["attributes"]["details"]["map"]
    # If the player amount is less than minimumPlayers, then dont record a new row (To avoid filling the file during an unseeded server
    if playerAmountInt >= minimumPlayers:
        file.write("\n" + date + ";" + mapName + ";" + playerAmount)
    # Wait the interval time to record next data entry
    time.sleep(interval)
