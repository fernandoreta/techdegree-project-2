import sys
import csv
import random

# Fernando Uriel Wertt reta
# List of each player.
# List of each team
# 2 spaces between functions as a good practice
# DATAFILE as constant


DATAFILE = 'soccer_players.csv'
PRACTICE_TIME = {
    'Dragons': "April 22, 2019 @ 5:00PM",
    'Sharks': "April 23, 2019 @ 7:00PM",
    'Raptors': "April 24, 2019 @ 9:00PM",
}
TEAM_NAMES = ['Dragons', 'Sharks', 'Raptors']


def get_players_from_file(filename=DATAFILE):
    with open(filename, newline='') as csvfile:
        player_reader = csv.DictReader(csvfile)
        players = list(player_reader)
        return players


def generate_team(name):
    return {'name': name, 'avg_height': 0, 'players': []}


def get_team_avg_height(team):
    num_players = len(team['players'])
    if num_players == 0:
        # No players return 0
        return 0
    total_height = 0
    for player in team['players']:
        total_height += int(player['Height (inches)'])
    return total_height / num_players


def partition_players(players, league):
    while players:
        league.sort(key=lambda team: team['avg_height'])
        for team in league:
            team['players'].append(players.pop(0))
            team['avg_height'] = get_team_avg_height(team)


def gen_player_letters(team):
    for player in team['players']:
        # split on space
        player_name = player['Name'].split()
        # gen file name from player name (rejoin with '_')
        filename = "player_" + "_".join(player_name).lower() + ".txt"
        with open(filename, 'w') as file:
            # write header
            file.write("\n\n\t\t\tSoccer League -- Team {}\n\n"
                       "".format(team['name']))
            # salutation
            file.write("Dear {},\n\n".format(player['Guardian Name(s)']))
            # body
            file.write("We would like to welcome you and {} to the Soccer "
                       "League.\n".format(player['Name']))
            file.write("This year, {} will be playing on Team {}.\nThe first "
                       "".format(player_name[0], team['name']))
            file.write("practice will be on {} at BBVA Bancomer.\n"
                       "".format(PRACTICE_TIME[team['name']]))
            # closing
            file.write("\n\nWe look forward to another great year!"
                       "\n\nRegards, Coach Kicks.\n")


def gen_team_roster(team):
    filename = team['name'].lower() + "_roster.txt"
    with open(filename, 'w') as file:
        # write header
        file.write("\n\n\t\t\tSoccer League -- Team {} Roster\n\n"
                   "".format(team['name']))
        # write practice time
        file.write("\tFirst Practice:\t{}\n\n"
                   "".format(PRACTICE_TIME[team['name']]))
        # write stats
        file.write("\tStats:\t\tNumber of players: {}, "
                   "Average Height (inches): {:0.2f}\n\n"
                   "".format(len(team['players']), team['avg_height']))
        # write roster of players
        file.write("\tPlayers:\n")
        for player in team['players']:
            file.write("\t\tName: {}\n".format(player['Name']))
            file.write("\t\t\tExperienced: {}, Height: {}, Guardian(s): {}\n"
                       "".format(player['Soccer Experience'],
                                 player['Height (inches)'],
                                 player['Guardian Name(s)']))


def output_stats(league):
    for team in league:
        print("Team {}: Avg Height {}".format(
            team['name'], team['avg_height']))


def main():
    entire_league = []
    for name in TEAM_NAMES:
        entire_league.append(generate_team(name))

    players = get_players_from_file()

    exp_players = []
    new_players = []
    for player in players:
        if player['Soccer Experience'] == 'YES':
            exp_players.append(player)
        else:
            new_players.append(player)
    exp_players.sort(key=lambda player: player['Height (inches)'],
                     reverse=True)
    new_players.sort(key=lambda player: player['Height (inches)'],
                     reverse=True)

    partition_players(exp_players, entire_league)

    partition_players(new_players, entire_league)

    for team in entire_league:
        gen_player_letters(team)
        gen_team_roster(team)

    output_stats(entire_league)

if __name__ == '__main__':
    main()