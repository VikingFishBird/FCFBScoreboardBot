from team import Team
from game import Game
from reddit import reddit
from reddit import subreddit
import re

teams = []
games = []

rankings = """SMU
Louisiana–Monroe
New Mexico State
Iowa
Kansas
NC State
Oklahoma State
Army
UNLV
Appalachian State
North Texas
Purdue
Coastal Carolina
Boise State
South Florida
West Virginia
UAB
UTEP
Colorado State
Stanford
Southern Mississippi
Missouri
Charlotte
Boston College
TOledo"""

manualGames = """
Arkansas | Alabama | 51 | **54** | **F/4OT**
"""
skipGames = """

"""
fcs = """
Columbia
James Madison
Eastern Kentucky
Kennesaw State
Lehigh
Maine
Missouri State
Montana
Northern Iowa
Rhode Island
South Carolina State
Southern Utah
"""

gameString = """UCF|Cincinnati
Connecticut|Tulsa
East Carolina|SMU
USF|Houston
Tulane|Memphis
Navy|Temple
Notre Dame|Boston College
Clemson|Syracuse
Duke|Pittsburgh
Florida State|Wake Forrest
BYU|Georgia Tech
Arkansas|Louisville
Virginia|Miami (FL)
North Carolina|Virginia Tech
NC State|Missouri
Illinois|Wisconsin
Indiana|Ohio State
Northwestern|Iowa
Maryland|Michigan
Michigan State|Nebraska
Penn State|Minnesota
Purdue|Rutgers
Kansas State|Baylor
West Virginia|Iowa State
TCU|Kansas
Texas|Oklahoma
Texas Tech|Oklahoma State
FIU|Charlotte
Marshall|FAU
Louisiana Tech|UAB
Old Dominion|Middle Tennessee
Rice|North Texas
Southern Mississippi|Western Kentucky
UTEP|UTSA
Central Michigan|Akron
Kent State|Ball State
Bowling Green|Toledo
Eastern Michigan|Buffalo
Western Michigan|Miami (OH)
Ohio|Northern Illinois
Utah State|Air Force
UNLV|Boise State
Colorado State|Nevada
Fresno State|San Jose State
Hawaii|San Diego State
Wyoming|New Mexico
Arizona|USC
Utah|Arizona State
UCLA|California
Colorado|Washington State
Oregon|Stanford
Washington|Oregon State
Texas A&M|Alabama
Auburn|LSU
Florida|Vanderbilt
Georgia|Mississippi State
Kentucky|Tennessee
Ole Miss|South Carolina
Appalachian State|Georgia State
Arkansas State|Troy
Coastal Carolina|Louisiana-Monroe
Georgia Southern|Texas State
Louisiana-Lafayette|Liberty
South Alabama|New Mexico State
Massachusetts|Army"""


teamsPage = subreddit.wiki["teams"]


# Load Teams
for teamLine in teamsPage.content_md.splitlines():
    items = teamLine.split('|')
    team = Team(n=items[1], t=items[0])
    teams.append(team)
for Team in teams:
    if Team.name in rankings:
        div = rankings.splitlines()
        for i in range(div.__len__()):
            if Team.name == div[i]:
                Team.rank = "#" + str(i+1)
                break


def editScoreboard(content):
    wikiPage = subreddit.wiki["week_6_scores"]
    wikiPage.edit(content)


def loadGames():
    gameStrings = gameString.splitlines()
    for x in range(gameStrings.__len__()):
        line = gameStrings[x].split('|')
        games.append(Game())
        for i in range(teams.__len__()):
            if games[-1].away is not 0 and games[-1].home is not 0:
                break

            if teams[i].name == line[0]:
                games[-1].away = i
            elif teams[i].name == line[1]:
                games[-1].home = i

        for submission in subreddit.new(limit=250):
            if line[0] in submission.title and line[1] in submission.title and "[GAME THREAD]" in submission.title:
                splitURL = submission.url.split(".")
                splitURL.insert(1, "old")
                ".".join(splitURL)
                games[-1].gameThread = ".".join(splitURL)
                break

        teams[games[-1].home].inGame = True
        teams[games[-1].away].inGame = True

        print(line)

    '''
    for submission in subreddit.new(limit=130):
        if "[GAME THREAD]" in submission.title:
            for i in range(teams.__len__()):
                if re.search(teams[i].name, submission.title) is not None and teams[i].inGame == False:
                    if teams[findTeamInText(submission.title)].name != teams[i].name:
                        continue
                    elif re.search(r'@\s' + teams[i].name, submission.title) is not None:

                        awayID = findTeamInText(submission.title, teams[i].name)

                        if teams[awayID].inGame == False and checkGameSkipped(teams[i].name, teams[awayID].name) is True:
                            games.append(Game())

                            splitURL = submission.url.split(".")
                            splitURL.insert(1, "old")
                            ".".join(splitURL)
                            games[-1].gameThread = ".".join(splitURL)
                            games[-1].home = i
                            games[-1].away = awayID
                            teams[games[-1].home].inGame = True
                            teams[games[-1].away].inGame = True
                    else:
                        homeID = findTeamInText(submission.title, teams[i].name)

                        if teams[homeID].inGame == False and checkGameSkipped(teams[homeID].name, teams[i].name) is True:
                            games.append(Game())
                            splitURL = submission.url.split(".")
                            splitURL.insert(1, "old")
                            ".".join(splitURL)
                            games[-1].gameThread = ".".join(splitURL)
                            games[-1].home = homeID
                            games[-1].away = i
                            teams[games[-1].home].inGame = True
                            teams[games[-1].away].inGame = True '''


def createText():
    sortGames()
    text = "**Away**| | |**Home**| | | Status | Game | Postgame\n:-:|-|:-:|:-:|-|:-:|:-:|:-:|:-:\n"
    for i in range(games.__len__()):
        text = text + getGameLine(games[i]) + "\n"
    text = text + "\n\nGame of the Week: **Alabama @ Arkansas**"
    text = text + "\n\n[Last Week](https://www.old.reddit.com/r/FakeCollegeFootball/wiki/week_5_scores)"
    text = text + "\n\n\nGO BRUINS! 33-28"
    return text


def getGameDetails(gameID):
    submission = reddit.submission(url=games[gameID].gameThread)
    matches = re.findall(r'\[.+\]\(#f/\w+\)\|\d+\|\d+\|\d+\|\d+\|\*\*\d+\*\*', submission.selftext)
    if matches.__len__() == 2 and checkGameManual(teams[games[gameID].home].name, teams[games[gameID].away].name) is True:
        g1 = matches[0].split('**')
        homeScore = g1[1]
        g2 = matches[1].split('**')
        awayScore = g2[1]

        matches = re.findall(r'\s\d:\d\d\|\d', submission.selftext)
        t1 = matches[0].split("|")
        quarter = t1[1]
        if re.search(r'\s0:00', submission.selftext) is not None:
            quarter = "**F**"
            if games[gameID].postThread == "":
                games[gameID].postThread = findPostGame(gameID)
            if homeScore > awayScore:
                homeScore = "**" + homeScore + "**"
            else:
                awayScore = "**" + awayScore + "**"
        else:
            if int(quarter) > 4:
                quarter = "OT"
            else:
                quarter = "Q" + quarter

        games[gameID].hScore = homeScore
        games[gameID].aScore = awayScore
        games[gameID].quarter = quarter
    else:
        print(games[gameID].gameThread)
        manMatches = re.findall(teams[games[gameID].home].name + r'\s|\s' + teams[games[gameID].away].name + r'\s|\s\d+\s|\s\d+\s|\s.+', manualGames)

        data = None
        for i in range(manMatches.__len__()):
            if teams[games[gameID].home].name in manMatches[i]:
                data = manMatches[i].split(" | ")

        games[gameID].hScore = data[2]
        games[gameID].aScore = data[3]
        games[gameID].quarter = data[4]
        if "F" in games[gameID].quarter and games[gameID].postThread == "":
            games[gameID].postThread = findPostGame(gameID)


def getGameLine(game):
    gameLine = teams[game.away].printSetup() + game.aScore + " | " + \
               teams[game.home].printSetup() + game.hScore + " | " + game.quarter + \
               "| [Thread](" + game.gameThread + ") | "

    if game.postThread != '':
        gameLine = gameLine + "[Thread](" + game.postThread + ")"

    return gameLine


def findPostGame(gameID):
    for submission in subreddit.new(limit=100):
        if "[POST GAME THREAD]" in submission.title:
            pos1 = teams[games[gameID].home].name + " defeats " + teams[games[gameID].away].name + ","
            pos2 = teams[games[gameID].away].name + " defeats " + teams[games[gameID].home].name + ","

            if pos1 in submission.title or pos2 in submission.title:
                splitURL = submission.url.split(".")
                splitURL.insert(1, "old")
                ".".join(splitURL)
                return ".".join(splitURL)
    return ""


def findTeamInText(text, other_team="U$C Sucks"):
    list = []
    for i in range(teams.__len__()):
        if teams[i].name == other_team:
            continue

        if teams[i].name in text:
            if teams[i].name in other_team:
                continue
            else:
                list.append(i)

    if list.__len__() > 1:
        id = list[0]
        for i in range(list.__len__()):
            if len(teams[list[i]].name) > len(teams[id].name):
                id = list[i]
        return id
    elif list.__len__() == 0:
        return None
    else:
        return list[0]


def checkGameSkipped(home, away):
    if home in skipGames and away in skipGames:
        return False
    else:
        return True


def checkGameManual(home, away):
    if home in manualGames and away in manualGames:
        return False
    else:
        return True


def sortGames():
    print("SORTING")
    for i in range(games.__len__()):
        games[i].sortValue = 0

        if "F" in games[i].quarter:
            games[i].sortValue = -100
        rankValue = 0
        if teams[games[i].home].rank != 0:
            div = rankings.splitlines()
            for j in range(div.__len__()):
                if teams[games[i].home].name == div[j]:
                    rankValue = 25 - j

            if teams[games[i].away].rank != 0:
                div = rankings.splitlines()
                for j in range(div.__len__()):
                    if teams[games[i].away].name == div[j]:
                        rankValue = 25 - j

        elif teams[games[i].away].rank != 0:
            div = rankings.splitlines()
            for j in range(div.__len__()):
                if teams[games[i].away].name == div[j]:
                    rankValue = 25 - j

        games[i].sortValue = games[i].sortValue - rankValue
        if re.search(r'\n' + teams[games[i].away].name + r'\n', fcs) is not None or re.search(r'\n' + teams[games[i].home].name + r'\n', fcs) is not None:
            games[i].sortValue = games[i].sortValue + 200

    games.sort(key=lambda Game: Game.sortValue)


'''
def setWatchValues():
'''