#!/usr/bin/env python3
import itertools

# Player map with names and their average bases
players = {
    "Ross": 0.65,      # Average bases per at-bat
    "Brendon": 0.9,
    "Lindsey": 0.3,
    "Aidan": 1.25,
    "Robbie": 0.65,
    "Kaitlin": 0.45,
    "Kate": 0.2,
    "Thomas": 0.5,
    "Jake": 0.8,
    "Josh": 0.8
}

# Define which players are women (the rest are men)
women = {"Lindsey", "Kate", "Kaitlin"}
men = set(players.keys()) - women

def is_legal_lineup(lineup):
    """Check if a lineup is legal (at most 3 men in a row)."""
    lineup_list = list(lineup)
    
    for i in range(len(lineup_list) - 2):  # Check every group of 3 consecutive players
        consecutive_men = 0
        for j in range(3):
            if i + j < len(lineup_list) and lineup_list[i + j] in men:
                consecutive_men += 1
        if consecutive_men > 3:
            return False
    
    return True

def generate_legal_lineups(all_players):
    """Generate all legal lineups that satisfy the 3-men-in-a-row rule."""
    all_lineups = list(itertools.permutations(all_players))
    legal_lineups = [lineup for lineup in all_lineups if is_legal_lineup(lineup)]
    return legal_lineups

if __name__ == "__main__":
    all_players = list(players.keys())
    
    print("Testing lineup restrictions...")
    print(f"Women: {', '.join(women)}")
    print(f"Men: {', '.join(men)}")
    print(f"Rule: At most 3 men in a row")
    print()
    
    legal_lineups = generate_legal_lineups(all_players)
    total_possible = len(list(itertools.permutations(all_players)))
    
    print(f"Total possible lineups: {total_possible:,}")
    print(f"Legal lineups: {len(legal_lineups):,}")
    print(f"Percentage legal: {len(legal_lineups)/total_possible*100:.1f}%")
    
    # Show a few example legal lineups
    print(f"\nExample legal lineups:")
    for i, lineup in enumerate(legal_lineups[:5]):
        print(f"{i+1}. {' → '.join(lineup)}")
    
    # Show a few example illegal lineups
    print(f"\nExample illegal lineups (4+ men in a row):")
    illegal_count = 0
    for lineup in itertools.permutations(all_players):
        if not is_legal_lineup(lineup):
            print(f"{illegal_count+1}. {' → '.join(lineup)}")
            illegal_count += 1
            if illegal_count >= 5:
                break
    
    # Test with a scenario that should be illegal
    print(f"\nTesting logic with 4 men in a row:")
    test_lineup = ("Ross", "Brendon", "Jake", "Josh", "Lindsey", "Aidan", "Robbie", "Thomas", "Kaitlin", "Kate")
    print(f"Test lineup: {' → '.join(test_lineup)}")
    print(f"Is legal: {is_legal_lineup(test_lineup)}")
    
    # Check if we can find any lineup with 4 men in a row
    print(f"\nSearching for lineups with 4+ men in a row...")
    found_illegal = False
    for lineup in itertools.permutations(all_players):
        if not is_legal_lineup(lineup):
            print(f"Found illegal lineup: {' → '.join(lineup)}")
            found_illegal = True
            break
    
    if not found_illegal:
        print("No illegal lineups found - all lineups are legal!")
        print("This makes sense because with 7 men and 3 women, we can't have 4 men in a row.") 