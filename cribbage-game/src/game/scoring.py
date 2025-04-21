def count_pairs(hand):
    counts = {}
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    return sum(count * (count - 1) // 2 for count in counts.values())

def count_runs(hand):
    sorted_hand = sorted(hand)
    runs = 0
    current_run_length = 1

    for i in range(1, len(sorted_hand)):
        if sorted_hand[i] == sorted_hand[i - 1] + 1:
            current_run_length += 1
        elif sorted_hand[i] != sorted_hand[i - 1]:
            if current_run_length >= 3:
                runs += current_run_length
            current_run_length = 1

    if current_run_length >= 3:
        runs += current_run_length

    return runs

def count_fifteens(hand):
    from itertools import combinations
    count = 0
    for r in range(2, len(hand) + 1):
        for combo in combinations(hand, r):
            if sum(combo) == 15:
                count += 1
    return count

def calculate_score(hand):
    return count_pairs(hand) + count_runs(hand) + count_fifteens(hand)