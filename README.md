# CSGO_Project V2.0
A project to retrieve all information about users CSGO games automatically. Once entering a users steamid, and steamkey into the table information will be automatically updated into the database.


### Setup
Extra Tools Needed:
1) CSGO Demos Manager (A program that downloads and analyzes your CSGO games), make sure that this is added to PATH so that it can be called anywhere via 'csgodm'

Add the following environment variables:
1) 'STEAM_API_KEY' = Your steam API key

Files that need to be created
1) dbconnection.py -> this will be a connection to your own personal database

### Runtime
1) Run downloadDemsMain.py as much as possible to continuously check for new user games.