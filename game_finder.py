"""
Given the following inputs:
- <game_data> is a list of dictionaries, with each dictionary representing a player's shot attempts in a game. The list can be empty, but any dictionary in the list will include the following keys: gameID, playerID, gameDate, fieldGoal2Attempted, fieldGoal2Made, fieldGoal3Attempted, fieldGoal3Made, freeThrowAttempted, freeThrowMade. All values in this dictionary are ints, except for gameDate which is of type str in the format 'MM/DD/YYYY'
- <true_shooting_cutoff> is the minimum True Shooting percentage value for a player to qualify in a game. It will be an int value >= 0.
- <player_count> is the number of players that need to meet the <true_shooting_cutoff> in order for a gameID to qualify. It will be an int value >= 0.

Implement find_qualified_games to return a list of unique qualified gameIDs in which at least <player_count> players have a True Shooting percentage >= <true_shooting_cutoff>, ordered from most to least recent game.
"""

def calculate_ts_percentage(player_stats):
    points = (2 * player_stats['fieldGoal2Made'] + 
              3 * player_stats['fieldGoal3Made'] + 
              player_stats['freeThrowMade'])
    
    # field goal attempts and free throw attempts
    fga = player_stats['fieldGoal2Attempted'] + player_stats['fieldGoal3Attempted']
    fta = player_stats['freeThrowAttempted']
    
    # Total attempts
    total_attempts = fga + 0.44 * fta
    
    if total_attempts == 0: 
        return 0
    
    # True Shooting Percentage
    ts_percentage = (points / (2 * total_attempts)) * 100
    return ts_percentage

def find_qualified_games(game_data: list[dict], true_shooting_cutoff: int, player_count: int) -> list[int]:
    # Number of qualified players
    game_qualified_players = {}

    for player in game_data:
        game_id = player['gameID']
        ts_percentage = calculate_ts_percentage(player)
        
        if ts_percentage >= true_shooting_cutoff:
            if game_id not in game_qualified_players:
                game_qualified_players[game_id] = {'gameDate': player['gameDate'], 'qualified_count': 0}
            game_qualified_players[game_id]['qualified_count'] += 1

    # Players meet the requirement
    qualified_games = [
        (game_id, game_info['gameDate']) 
        for game_id, game_info in game_qualified_players.items()
        if game_info['qualified_count'] >= player_count
    ]

    # Most recent first
    qualified_games.sort(key=lambda x: x[1], reverse=True)

    return [game_id for game_id, _ in qualified_games]

def test_case_1():
    game_data = []
    qualified_games = find_qualified_games(game_data, 57, 1)
    assert qualified_games == []

def test_case_2():
    game_data = [
        {'gameID': 1, 'playerID': 5, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 2, 'fieldGoal3Attempted': 7, 'fieldGoal3Made': 2, 'freeThrowAttempted': 3, 'freeThrowMade': 3},
        {'gameID': 2, 'playerID': 5, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 8, 'fieldGoal2Made': 5, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 1, 'freeThrowAttempted': 2, 'freeThrowMade': 2},
    ]
    qualified_games = find_qualified_games(game_data, 53, 1)
    assert qualified_games == [2]

def test_case_3():
    game_data = [
        {'gameID': 9, 'playerID': 42, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 2, 'freeThrowAttempted': 4, 'freeThrowMade': 3},
        {'gameID': 10, 'playerID': 34, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 8, 'fieldGoal2Made': 7, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 2, 'freeThrowMade': 1},
    ]
    qualified_games = find_qualified_games(game_data, 0, 1)
    assert qualified_games == [10, 9]

def test_case_4():
    game_data = [
        {'gameID': 9, 'playerID': 24, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 14, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 2, 'freeThrowAttempted': 4, 'freeThrowMade': 3},
        {'gameID': 9, 'playerID': 35, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 2, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 1, 'freeThrowAttempted': 4, 'freeThrowMade': 2},
        {'gameID': 9, 'playerID': 34, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 8, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 3, 'freeThrowMade': 1},
        {'gameID': 9, 'playerID': 42, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 2, 'freeThrowAttempted': 4, 'freeThrowMade': 0},
        {'gameID': 10, 'playerID': 24, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 8, 'fieldGoal2Made': 7, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 8, 'freeThrowMade': 1},
        {'gameID': 10, 'playerID': 42, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 8, 'fieldGoal2Made': 7, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 1, 'freeThrowAttempted': 2, 'freeThrowMade': 1},
        {'gameID': 10, 'playerID': 25, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 2, 'freeThrowAttempted': 4, 'freeThrowMade': 3},
        {'gameID': 10, 'playerID': 33, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 6, 'fieldGoal2Made': 2, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 2, 'freeThrowMade': 1},
        {'gameID': 6, 'playerID': 34, 'gameDate': '02/11/2023', 'fieldGoal2Attempted': 12, 'fieldGoal2Made': 6, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 1, 'freeThrowAttempted': 6, 'freeThrowMade': 6},
        {'gameID': 6, 'playerID': 25, 'gameDate': '02/11/2023', 'fieldGoal2Attempted': 9, 'fieldGoal2Made': 2, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 2, 'freeThrowAttempted': 2, 'freeThrowMade': 0},
        {'gameID': 5, 'playerID': 42, 'gameDate': '01/06/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 2, 'freeThrowAttempted': 3, 'freeThrowMade': 3},
        {'gameID': 4, 'playerID': 34, 'gameDate': '01/22/2023', 'fieldGoal2Attempted': 18, 'fieldGoal2Made': 5, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 3, 'freeThrowAttempted': 2, 'freeThrowMade': 1},
    ]
    qualified_games = find_qualified_games(game_data, 52, 1)
    assert qualified_games == [6, 10, 5]

def test_case_5():
    game_data = [
        {'gameID': 6, 'playerID': 34, 'gameDate': '02/11/2023', 'fieldGoal2Attempted': 12, 'fieldGoal2Made': 6, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 1, 'freeThrowAttempted': 6, 'freeThrowMade': 6},
        {'gameID': 6, 'playerID': 25, 'gameDate': '02/11/2023', 'fieldGoal2Attempted': 9, 'fieldGoal2Made': 2, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 2, 'freeThrowAttempted': 2, 'freeThrowMade': 0},
        {'gameID': 9, 'playerID': 24, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 14, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 3, 'freeThrowAttempted': 4, 'freeThrowMade': 4},
        {'gameID': 9, 'playerID': 35, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 2, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 1, 'freeThrowAttempted': 4, 'freeThrowMade': 2},
        {'gameID': 9, 'playerID': 34, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 8, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 3, 'freeThrowMade': 1},
        {'gameID': 9, 'playerID': 42, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 2, 'freeThrowAttempted': 4, 'freeThrowMade': 0},
        {'gameID': 10, 'playerID': 24, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 8, 'fieldGoal2Made': 7, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 5, 'freeThrowMade': 4},
        {'gameID': 10, 'playerID': 42, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 8, 'fieldGoal2Made': 6, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 1, 'freeThrowAttempted': 2, 'freeThrowMade': 1},
        {'gameID': 10, 'playerID': 25, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 2, 'freeThrowAttempted': 4, 'freeThrowMade': 3},
        {'gameID': 10, 'playerID': 33, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 7, 'fieldGoal2Made': 2, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 2, 'freeThrowMade': 1},
        {'gameID': 5, 'playerID': 42, 'gameDate': '01/06/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 2, 'freeThrowAttempted': 3, 'freeThrowMade': 3},
        {'gameID': 4, 'playerID': 34, 'gameDate': '01/22/2023', 'fieldGoal2Attempted': 18, 'fieldGoal2Made': 5, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 3, 'freeThrowAttempted': 2, 'freeThrowMade': 1},
    ]
    qualified_games = find_qualified_games(game_data, 46, 3)
    assert qualified_games == [10]

def test_case_6():
    game_data = [
        {'gameID': 6, 'playerID': 34, 'gameDate': '02/11/2023', 'fieldGoal2Attempted': 12, 'fieldGoal2Made': 0, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 6, 'freeThrowMade': 6},
        {'gameID': 9, 'playerID': 35, 'gameDate': '01/02/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 2, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 1, 'freeThrowAttempted': 4, 'freeThrowMade': 2},
        {'gameID': 10, 'playerID': 24, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 8, 'fieldGoal2Made': 7, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 5, 'freeThrowMade': 4},
        {'gameID': 10, 'playerID': 42, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 8, 'fieldGoal2Made': 6, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 1, 'freeThrowAttempted': 2, 'freeThrowMade': 1},
        {'gameID': 10, 'playerID': 25, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 2, 'freeThrowAttempted': 4, 'freeThrowMade': 3},
        {'gameID': 10, 'playerID': 33, 'gameDate': '01/09/2023', 'fieldGoal2Attempted': 7, 'fieldGoal2Made': 2, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 2, 'freeThrowMade': 1},
        {'gameID': 5, 'playerID': 42, 'gameDate': '01/06/2023', 'fieldGoal2Attempted': 4, 'fieldGoal2Made': 3, 'fieldGoal3Attempted': 6, 'fieldGoal3Made': 2, 'freeThrowAttempted': 3, 'freeThrowMade': 3},
        {'gameID': 4, 'playerID': 34, 'gameDate': '01/22/2023', 'fieldGoal2Attempted': 3, 'fieldGoal2Made': 0, 'fieldGoal3Attempted': 5, 'fieldGoal3Made': 0, 'freeThrowAttempted': 2, 'freeThrowMade': 0},
    ]
    qualified_games = find_qualified_games(game_data, 1, 1)
    # print(qualified_games)
    assert qualified_games == [6, 10, 5, 9]

test_case_1()
test_case_2()
test_case_3()
test_case_4()
test_case_5()
test_case_6()
print("All test cases passed")