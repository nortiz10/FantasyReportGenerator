# <p style="text-align: center;">Fantasy Football Report Generator</p>
---
## Project Overview:
This Python backed discord bot provides functionality to analyze fantasy football projections for players based on their recent performance, matchup difficulty, and statistical projections. It utilizes web scraping techniques to gather data from Yahoo Fantasy Sports and interacts with the ESPN API for further player/matchup information. It also operates with  a custom SQLite database to store relevant player and matchup information.

---
### Features
- Web Scraping
  - Utilizes BeautifulSoup4 to scrape over 125 fantasy football data points from Yahoo Fantasy Sports. Currently(as of 2-13-24) using the data from the 2023 season.
- API Interaction
  - Requests to the ESPN NFL API for full roster information for all 32 teams as well as each of the 14-16 matchups for the current game week.
  - Parsed and filtered received JSON data for storage in custom databse
- SQLite Database
  - Employs a SQLite database for convenient storage of the 1,600+ unique player information sets into a players table with foreign keys to connect to a matchups table.
---
### Prerequisites
##### Discord Bot Setup
Follow steps to create one's own discord bot through the discord development portal like [this tutorial(up to 4:14)](https://www.youtube.com/watch?v=hoDLj0IzZMU) and paste your acquired token into the commented out `TOKEN` field in `bot.py` as well as use the invite link to invite the bot to desired server.
##### Python Packages
The following are needed to run the script and bot:
- BeautifulSoup4
- requests
- sqlite3
- discord
- json  
You can install the necessary dependencies using pip3:  
`pip3 install beautifulsoup4 requests sqlite3 discord json`
---
### Usage
1. Clone or download the repository
2. Make sure you have the necessary dependencies installed
3. With the discord bot properly set up and in a server execute the script  
`python3 main.py`
4. Typing a full player's name as shown in the png in this repo will produce the comprehensive player projection for the current game week.

##### Alternatively(if not using a discord bot):
1. Clone or download the repository
2. Make sure you have the necessary dependencies installed(except discord)
3. A simple print statement in `responses.py` will display the full output in the terminal:  
`print(ffstats.get_player_info("Travis Kelce")` where Travis Kelce is a placeholder for any skill position player.
4. Execute the `responses.py` script:  
`python3 responses.py`
---
### Disclaimer
Given the 2023 season is over, using `load_db.py` to update the SQLite3 databse is discouraged as functionality will vary. Additionally since the 'previous performance' calculations are on-demand accuracy may vary outside of active season play. The provided myDb.db is loaded with information up to game week 15 of the 2023 season for demo purposes in the off season.