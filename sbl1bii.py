import pandas as pd
from collections import defaultdict, Counter
import itertools

# function to load data from the file
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' : ')
            senders = list(map(int, parts[0].split()))
            receivers = list(map(int, parts[1].split()))
            data.append((senders, receivers))
    return data

# recursive function to find minimal hitting sets
def exact_hs(observations, m, C=set()):
    if not observations:  # base case: no more observations
        return [C]
    if m < 1:  # base case: invalid m
        return []
    
    B = observations[0]
    H = []
    for r in B:
        # create new observations excluding r
        new_obs = [obs for obs in observations if r not in obs]
        # add r to the current set
        new_C = C | {r}
        # recurse with updated observations and set
        H += exact_hs(new_obs, m - 1, new_C)
    
    return H

# function to calculate minimal hitting sets for a specific sender
def calculate_exact_hs(data, sender):
    # filter observations for the given sender
    sender_observations = [set(receivers) for senders, receivers in data if sender in senders]
    m = 1
    hitting_sets = []
    while not hitting_sets:  # increment m until hitting sets are found
        hitting_sets = exact_hs(sender_observations, m)
        m += 1
    return hitting_sets

# function to display a single hitting set
def display_hitting_set(hitting_sets):
    if hitting_sets:
        print(f"Hitting Set: {sorted(hitting_sets[0])}")

# main function to load data and compute hitting sets for each sender
def main():
    file_path = r"C:\Users\manue\Downloads\observation_mix.txt"
    data = load_data(file_path)
    
    for sender in range(1, 11):
        print(f"\nSender {sender} minimal hitting set:")
        hitting_sets = calculate_exact_hs(data, sender)
        display_hitting_set(hitting_sets)

if __name__ == "__main__":
    main()
