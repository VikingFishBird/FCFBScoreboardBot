from functions import loadGames
from functions import games
from functions import getGameDetails
from functions import createText
from functions import editScoreboard

loadGames()
print("Games Loaded")


scoreboardFormat = ""
while True:
    newText = ""
    for i in range(games.__len__()):
        print("Game ", i+1)
        getGameDetails(i)

    print("CompiledStats")
    newText = createText()
    if newText != scoreboardFormat:
        editScoreboard(newText)
        print("Edited Wiki")
        scoreboardFormat = newText

