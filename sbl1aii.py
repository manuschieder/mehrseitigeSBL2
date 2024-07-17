import pandas as pd
from collections import defaultdict

def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' : ')
            senders = list(map(int, parts[0].split()))
            receivers = list(map(int, parts[1].split()))
            data.append(senders + receivers)
    return pd.DataFrame(data, columns=["S1", "S2", "S3", "S4", "R1", "R2", "R3", "R4"])

def minimal_hitting_set(df):
    sender_batches = defaultdict(list)

    for _, row in df.iterrows():
        senders = set(row[:4])
        receivers = set(row[4:])
        for sender in senders:
            sender_batches[sender].append(receivers)

    minimal_hits = {}
    for sender, batches in sender_batches.items():
        print(f"Sender {sender} batches: {batches}")  # Debugging output
        # Attempt to find a minimal hitting set
        if batches:
            union_set = set.union(*batches)
            intersection_set = set.intersection(*batches)
            minimal_hits[sender] = (union_set, intersection_set)
        else:
            minimal_hits[sender] = (set(), set())

    return minimal_hits

def display_results(minimal_hits):
    for sender, (union, intersection) in minimal_hits.items():
        print(f"Sender {sender}: Union of receivers {sorted(union)}, Intersection of receivers {sorted(intersection)}")

def main():
    file_path = r"C:\Users\manue\Downloads\observation_mix.txt"
    df = load_data(file_path)
    minimal_hits = minimal_hitting_set(df)
    display_results(minimal_hits)

if __name__ == "__main__":
    main()
