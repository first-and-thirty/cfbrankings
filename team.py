import configparser
from pandas import read_excel as pdFromExcel

from statplot import StatDist, StatPlot
from schedule import Schedule

class Color:

    def __init__(self, hue, saturation, lightness):
        self.h = hue
        self.s = saturation
        self.l = lightness

class TeamLogo:

    def __init__(self, foregroundColor, backgroundColor, logoPath):
        self.fg = foregroundColor
        self.bg = backgroundColor
        self.logo = None if logoPath is None else logoPath

class TeamMetadata:

    def __init__(self,
                 name,
                 abbreviation,
                 conference,
                 foregroundColor = Color(0, 1.0, 0.0),
                 backgroundColor = Color(0, 1.0, 1.0),
                 logoPath = None
                 ):

        self.id = name
        self.name = name
        self.abbreviation = abbreviation
        self.conference = conference
        self.logo = TeamLogo(foregroundColor, backgroundColor, logoPath)

class TeamSchedule:

    def __init__(self, name, schedList):
        self.schedule = schedList
        #self.oppFirstOrderWins = (sum([m.teamA.wins for m in self.schedule if m.teamA.name != name]) +
        #                          sum([m.teamB.wins for m in self.schedule if m.teamB.name != name]))

    def __playedGames(self):
        return sum([1 for m in self.schedule if m.gamePlayed == True]) # equivalent to len of matching m's

class TeamRecord:

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.favoritePcnt = 0.0
        self.underdogPcnt = 0.0
        self.winPcntAsFavorite = 0.0
        self.winPcntAsUnderdog = 0.0

    def __totalGames(self):
        return self.wins + self.losses + self.ties

    def __recordStr(self):
        return "-".join([self.wins, self.ties, self.losses])

    def __recordAts(self):
        winsAts = self.favoritePcnt * self.__totalGames() * self.winPcntAsFavorite
        lossesAts = self.underdogPcnt * self.__totalGames() * self.winPcntAsUnderdog
        return [winsAts, self.__totalGames() - winsAts - lossesAts, lossesAts]

    def __recordAtsStr(self):
        return "-".join(self.__recordAts())

    def addResults(self, wins, losses, ties):
        self.wins += wins
        self.losses += losses
        self.ties += ties

class TeamReliability:

    def __init__(self):
        self.reliabilityAsFavorite = 0.5
        self.reliabilityAsUnderdog = 0.5
        
    def __reliability(self, gamesAsFavorite, gamesAsUnderdog):
        return (self.reliabilityAsFavorite * gamesAsFavorite + self.reliabilityAsUnderdog * gamesAsUnderdog) / (gamesAsFavorite + gamesAsUnderdog)

class TeamPower:

    def __init__(self):
        self.power = 0

    def __rank(self):
        return 1

class TeamStat:

    def __init__(self, name, data):
        self.name = name
        self.distWindow = StatDist(data)
        self.distCurSeason = StatDist(data[-1])
        self.plotWindow = StatPlot(self.name, data)
        self.plotCurSeason = StatPlot(self.name, data[-1])

class Team:

    def __init__(self,
                 name,
                 abbreviation,
                 conference,
                 foregroundColor = None,
                 backgroundColor = None,
                 logoPath = None,
                 schedList = [],
                 statList = None
                ):

        if foregroundColor is None or backgroundColor is None:
            self.meta = TeamMetadata(name, abbreviation, conference, logoPath = logoPath)
        else:
            self.meta = TeamMetadata(name, abbreviation, conference, foregroundColor, backgroundColor, logoPath)

        self.schedule = TeamSchedule(name, schedList)
        self.record = TeamRecord()
        #newWins = 0
        #newLosses = 0
        #newTies = 0
        #for matchup in self.schedule.schedule:
        #    if matchup.gamePlayed:
        #        if matchup.winner.name == name:
        #            newWins += 1
        #        elif matchup.winner.name == "TIE":
        #            newTies += 1
        #        else:
        #            newLosses += 1
        #self.record.addResults(newWins, newLosses, newTies)

        self.reliability = TeamReliability()
        self.power = TeamPower()

        self.stats = self.__readInAvailableStats(statList)

        #self.secondOrderWins = sum(self.schedule.oppFirstOrderWins)

    def __readInAvailableStats(self, statList):
        config = configparser.ConfigParser()
        defaults = config["DEFAULT"]

        statSrc = pdFromExcel(defaults["MASTER_STAT_SRC"], defaults["MASTER_STAT_SHEET"])
        statsToRead = statList if statList is not None else [s for s in statSrc.columns if s.startswith("STAT_")]

        stats = []
        for stat in statsToRead:
            stats.append(TeamStat(stat, statSrc[stat]))

        return stats
        