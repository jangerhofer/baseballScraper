from bs4 import BeautifulSoup
import requests
import re

page = requests.get("http://www.baseballpress.com/lineups")
soup = BeautifulSoup(page.text, 'html.parser')

games = soup.select(".game")

# Seperate name from handedness: input e.g. "Travis Wood (L)"
def parsePitcher(combinedString):
    matches = re.search("(.*)\((.*)\)", combinedString)
    return matches.group(1).strip(), matches.group(2).strip()

# Seperate weather data: input e.g. "Gametime Forecast: 76°F • Partly Cloudy • 0% PoP"
def parseWeather(forecastString):
    matches = re.search(":\s(.*)°.*•\s(.*)•\s*(.*)%", forecastString)
    return matches.group(1).strip(), matches.group(2).strip(), matches.group(3).strip()


def getLineups():
    saveData = []

    for game in games:
        if game.select("div .team-name"):
            gameData = {"away" : {}, "home": {}}

            # Team Names
            gameData["away"]["team"] = game.select("div .team-name")[0].string
            gameData["home"]["team"] = game.select("div .team-name")[1].string

            # Starting Pitchers
            awayPitcher, awayPitcherHand = parsePitcher(game.select(".text")[0].select('div')[1].text)
            gameData["away"]["startingPitcher"] = awayPitcher
            gameData["away"]["startingPitcherHand"] = awayPitcherHand

            homePitcher, homePitcherHand = parsePitcher(game.select(".text")[1].select('div')[1].text)
            gameData["home"]["startingPitcher"] = homePitcher
            gameData["home"]["startingPitcherHand"] = homePitcherHand

            # Weather Forecast
            temp, forecast, precipChance = parseWeather(game.select_one(".weather").a.string.strip())
            gameData["weather"] = {
                "temp" : temp,
                "forecast" : forecast,
                "precipChance" :  precipChance
            }


            saveData.append(gameData)

    return saveData

print(getLineups())
