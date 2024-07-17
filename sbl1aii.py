import pandas as pd
from collections import defaultdict, Counter
import itertools

def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' : ')
            senders = list(map(int, parts[0].split()))
            receivers = list(map(int, parts[1].split()))
            data.append((senders, receivers))
    return data

def exact_hs(observations, m, C=set()):
    if not observations:
        return [C]
    if m < 1:
        return []
    
    B = observations[0]
    H = []
    for r in B:
        new_obs = [obs for obs in observations if r not in obs]
        new_C = C | {r}
        H += exact_hs(new_obs, m - 1, new_C)
    
    return H

def calculate_exact_hs(data, sender):
    sender_observations = [set(receivers) for senders, receivers in data if sender in senders]
    m = 1
    hitting_sets = []
    while not hitting_sets:
        hitting_sets = exact_hs(sender_observations, m)
        m += 1
    return hitting_sets

def display_hitting_sets(hitting_sets):
    for hs in hitting_sets:
        print(f"Hitting Set: {sorted(hs)}")

def main():
    file_path = r"C:\Users\manue\Downloads\observation_mix.txt"
    data = load_data(file_path)
    
    for sender in range(1, 11):
        print(f"\nSender {sender} minimal hitting sets:")
        hitting_sets = calculate_exact_hs(data, sender)
        display_hitting_sets(hitting_sets)

if __name__ == "__main__":
    main()
