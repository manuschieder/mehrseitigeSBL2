import pandas as pd
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' : ')
            senders = list(map(int, parts[0].split()))
            receivers = list(map(int, parts[1].split()))
            data.append(senders + receivers)
    return pd.DataFrame(data, columns=["S1", "S2", "S3", "S4", "R1", "R2", "R3", "R4"])

def calculate_sda(df):
    total_batches = len(df)
    sender_receiver_counts = defaultdict(lambda: Counter())
    total_sender_appearances = Counter()
    
    for _, row in df.iterrows():
        senders = set(row[:4])
        receivers = set(row[4:])
        for sender in senders:
            sender_receiver_counts[sender].update(receivers)
            total_sender_appearances[sender] += 1
    
    sda_scores = defaultdict(dict)
    num_possible_receivers = 10  # Assuming there are 10 potential receivers
    for sender in range(1, 11):
        for receiver in range(1, 11):
            observed_freq = sender_receiver_counts[sender][receiver]
            expected_freq = total_sender_appearances[sender] / num_possible_receivers
            sda_score = (observed_freq - expected_freq) / total_batches
            sda_scores[sender][receiver] = sda_score

    return sda_scores

def display_and_plot_scores(sda_scores):
    for sender in sorted(sda_scores):
        print(f"Sender {sender} communication probabilities:")
        sorted_receivers = sorted(sda_scores[sender].items(), key=lambda item: item[1], reverse=True)
        receivers, scores = zip(*sorted_receivers)
        plt.figure(figsize=(10, 5))
        plt.bar(receivers, scores, color='skyblue')
        plt.xlabel('Receiver')
        plt.ylabel('SDA Score')
        plt.title(f'SDA Communication Probabilities for Sender {sender}')
        plt.ylim(-0.25, 1)  # Set y-axis limits to be consistent across all plots
        plt.show()
        for receiver, score in sorted_receivers:
            print(f"  Receiver {receiver}: {score:.4f}")
        print("")

def main():
    file_path = r"C:\Users\manue\Downloads\observation_mix.txt"
    df = load_data(file_path)
    sda_scores = calculate_sda(df)
    display_and_plot_scores(sda_scores)

if __name__ == "__main__":
    main()

