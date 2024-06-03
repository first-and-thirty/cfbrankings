from schedule import Schedule

if __name__ == "__main__":
    print("Welcome to docgen!")

    season = 2021
    print("Generating {:} schedule...".format(season))
    schedule = Schedule(season)
    print("The {:} season has {:} games, starting with {:} @ {:} and ending with {:} @ {:}".format(season,
                                                                                                   len(schedule.master),
                                                                                                   schedule.master[0].teamA,
                                                                                                   schedule.master[0].teamB,
                                                                                                   schedule.master[-1].teamA,
                                                                                                   schedule.master[-1].teamB
    ))