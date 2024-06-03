import configparser
from pandas import read_excel as pdFromExcel

from statplot import StatDist

class Location:

    def __init__(self, locName):
        self.locName = locName

class StatDiff:

    def __init__(self, diff, importance, scale = 10):
        self.diff = diff
        self.diffSym = ("<" if diff < 0.1 else ">" if diff > 0.1 else "-") * int(abs(diff / scale))
        self.importance = importance
        self.prediction = self.diff * self.importance

class Matchup:

    def __init__(self, teamA, teamB, kickoffDate, kickoffTime, locName):
        self.teamA = teamA # TODO: change from a string to a Team object
        self.teamB = teamB
        self.kickoffDate = kickoffDate
        self.kickoffTime = kickoffTime
        self.loc = Location(locName)
        self.gamePlayed = False
        self.spreadEligible = False
        if self.spreadEligible:
            self.spreadSource = None
            self.spread = 0.0
    
    def completeGame(self, margin):
        self.gamePlayed = True

        self.margin = margin
        if self.margin < 0:
            self.winner = self.teamA
        elif self.margin > 0:
            self.winner = self.teamB
        else:
            self.winner = "TIE"

        if self.spreadEligible:
            self.marginAts = margin + self.spread
            if self.marginAts < 0:
                self.winnerAts = self.teamA
            elif self.marginAts > 0:
                self.winnerAts = self.teamB
            else:
                self.winnerAts = "PUSH"

class Schedule:

    def __init__(self, season):
        config = configparser.ConfigParser()
        defaults = config["DEFAULT"]
        schedSrc = pdFromExcel(defaults["MASTER_SCHED_SRC"], defaults["MASTER_SCHED_SHEET"])

        self.season = season
        self.master = []
        for rowIndex, row in schedSrc.iterrows():
            self.master.append(Matchup(*row))

class Prediction:

    def __init__(self, matchup):
        self.matchup = matchup
        self.stats = self.__getStatMinList()
        self.statDiffs = []
        self.predictionsA = []
        self.predictionsB = []

        for stat, vals in self.stats.items():
            importance, scale = 10, 10 # TODO: set these somewhere
            self.statDiffs.append(StatDiff(vals[1] - vals[0], importance, scale))
            self.predictionsA.append()

    def __getStatMinList(self):
        statsA = self.matchup.teamA.stats
        statsB = self.matchup.teamB.stats
        statNamesB = [s.name for s in statsB]

        stats = {}
        for i in range(len(statsA)):
            try:
                statBIndex = statNamesB.index(statsA[i].name)
                stats[statsA[i].name] = [statsA[i], statsB[statBIndex]]
            except ValueError as err:
                pass

        return stats
