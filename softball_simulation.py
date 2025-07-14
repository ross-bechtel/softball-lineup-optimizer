#!/usr/bin/env python3
import random
import itertools
import time

players = {
    "Ross": 0.65,      # Average bases per at-bat
    "Brendon": 0.9,
    "Lindsey": 0.3,
    "Aidan": 1.25,
    "Robbie": 0.65,
    "Kaitlin": 0.45,
    "Kate": 0.2,
    "Thomas": 0.5,
    "Jake": 0.6,
    "Josh": 0.6,
    "Srishti": 0.1,
    "Allison": 0.2
}

# Define which players are women (the rest are men)
women = {"Lindsey", "Kate", "Kaitlin", "Srishti", "Allison"}
men = set(players.keys()) - women

def is_legal_lineup(lineup):
    """Check if a lineup is legal (at most 3 men in a row, including wraparound)."""
    n = len(lineup)
    # Check normal sequence
    consecutive_men = 0
    for player in lineup:
        if player in men:
            consecutive_men += 1
            if consecutive_men > 3:
                return False
        else:
            consecutive_men = 0
    # Check wraparound: concatenate up to 3 from start to end
    max_wrap = 3
    wrap_lineup = list(lineup) + list(lineup)[:max_wrap]
    consecutive_men = 0
    for player in wrap_lineup:
        if player in men:
            consecutive_men += 1
            if consecutive_men > 3:
                return False
        else:
            consecutive_men = 0
    return True

def generate_legal_lineups(all_players):
    """Generate all legal lineups that satisfy the 3-men-in-a-row rule."""
    all_lineups = list(itertools.permutations(all_players))
    legal_lineups = [lineup for lineup in all_lineups if is_legal_lineup(lineup)]
    return legal_lineups

def simulate_at_bat(player_name):
    """Simulate a single at-bat for a player, returning whole bases (0-4)."""
    if player_name not in players:
        return 0
    
    avg_bases = players[player_name]
    
    # Convert average bases to whole base outcomes
    # For example: 1.3 avg bases means 70% chance of 1 base, 30% chance of 2 bases
    decimal_part = avg_bases - int(avg_bases)
    
    if random.random() < decimal_part:
        return min(int(avg_bases) + 1, 4)  # Cap at 4 bases (home run)
    else:
        return min(int(avg_bases), 4)

def simulate_inning(player_list):
    """Simulate one inning, returning runs scored."""
    bases = [None, None, None, None]  # 1st, 2nd, 3rd, home
    runs = 0
    outs = 0
    player_index = 0
    
    while outs < 3 and runs < 6:  # Cap at 6 runs per inning
        if not player_list:
            break
            
        player = player_list[player_index % len(player_list)]
        bases_gained = simulate_at_bat(player)
        
        if bases_gained == 0:
            outs += 1
        else:
            # Move runners and add new runner
            for i in range(3, -1, -1):
                if bases[i] is not None:
                    new_position = i + bases_gained
                    if new_position >= 4:
                        runs += 1
                        bases[i] = None
                    else:
                        bases[new_position] = bases[i]
                        bases[i] = None
            
            # Place new runner
            if bases_gained >= 4:
                runs += 1
            else:
                bases[bases_gained - 1] = player
        
        player_index += 1
    
    return runs

def simulate_multiple_games(player_list, num_games=10):
    """Simulate multiple games with the same lineup and return average runs."""
    total_runs = 0
    game_results = []
    
    for game in range(num_games):
        runs = simulate(player_list, verbose=False)
        total_runs += runs
        game_results.append(runs)
    
    avg_runs = total_runs / num_games
    return avg_runs, game_results

def find_best_lineup(all_players, num_games_per_lineup=10, max_lineups_to_test=None):
    """Find the best batting order by testing different permutations."""
    start_time = time.time()
    
    print(f"Testing lineups with {len(all_players)} players...")
    print(f"Each lineup will play {num_games_per_lineup} games")
    print(f"Women: {', '.join(women)}")
    print(f"Men: {', '.join(men)}")
    print(f"Rule: At most 3 men in a row")
    
    # Generate all legal lineups
    all_lineups = generate_legal_lineups(all_players)
    print(f"Found {len(all_lineups):,} legal lineups out of {len(list(itertools.permutations(all_players))):,} total possible")
    
    if max_lineups_to_test and len(all_lineups) > max_lineups_to_test:
        print(f"Testing {max_lineups_to_test:,} random legal lineups")
        # Randomly sample lineups to test
        random.shuffle(all_lineups)
        all_lineups = all_lineups[:max_lineups_to_test]
    else:
        print(f"Testing all {len(all_lineups):,} legal lineups")
    
    best_lineup = None
    best_avg_runs = 0
    best_game_results = []
    
    lineup_results = []
    
    for i, lineup in enumerate(all_lineups):
        avg_runs, game_results = simulate_multiple_games(list(lineup), num_games_per_lineup)
        lineup_results.append((list(lineup), avg_runs, game_results))
        
        if avg_runs > best_avg_runs:
            best_avg_runs = avg_runs
            best_lineup = list(lineup)
            best_game_results = game_results
        
        if (i + 1) % 10000 == 0:
            elapsed = time.time() - start_time
            print(f"Tested {i + 1:,}/{len(all_lineups):,} lineups... ({elapsed:.1f}s elapsed)")
    
    total_time = time.time() - start_time
    return best_lineup, best_avg_runs, best_game_results, lineup_results, total_time

def simulate(player_list, verbose=True):
    """Simulate a 6-inning game, returning total runs scored."""
    total_runs = 0
    
    for inning in range(6):
        inning_runs = simulate_inning(player_list)
        total_runs += inning_runs
        if verbose:
            print(f"Inning {inning + 1}: {inning_runs} runs")
    
    return total_runs

if __name__ == "__main__":
    print("Softball Game Simulation")
    print("=" * 30)
    
    # Get all players
    all_players = list(players.keys())
    
    # Find the best lineup
    print("Finding optimal batting order...")
    print()
    
    best_lineup, best_avg_runs, best_game_results, all_results, total_time = find_best_lineup(
        all_players, 
        num_games_per_lineup=10
    )
    
    print(f"\n🏆 BEST LINEUP FOUND:")
    print("=" * 40)
    if best_lineup:
        for i, player in enumerate(best_lineup, 1):
            avg_bases = players[player]
            print(f"{i}. {player:<10} (avg: {avg_bases:.2f} bases)")
    
    print(f"\nAverage runs per game: {best_avg_runs:.2f}")
    print(f"Game results: {best_game_results}")
    print(f"Range: {min(best_game_results)} - {max(best_game_results)} runs")
    
    # Show top 5 lineups
    print(f"\n📊 TOP 5 LINEUPS:")
    print("=" * 40)
    sorted_results = sorted(all_results, key=lambda x: x[1], reverse=True)
    for i, (lineup, avg_runs, game_results) in enumerate(sorted_results[:5], 1):
        print(f"{i}. {avg_runs:.2f} avg runs")
        print(f"   Lineup: {' → '.join(lineup)}")
        print()
    
    print(f"⏱️  Total time: {total_time:.2f} seconds")
    print(f"📈 Tested {len(all_results)} lineups")
