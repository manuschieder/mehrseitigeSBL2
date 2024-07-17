import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

def load_data(file_path):
    # Read the data from the file
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' : ')
            senders = list(map(int, parts[0].split()))
            receivers = list(map(int, parts[1].split()))
            data.append(senders + receivers)
    
    # Create DataFrame
    return pd.DataFrame(data, columns=["S1", "S2", "S3", "S4", "R1", "R2", "R3", "R4"])

def calculate_probabilities(df):
    # Initialize dictionaries to count frequencies of each sender and receiver appearance
    sender_counts = defaultdict(int)
    pair_counts = defaultdict(lambda: defaultdict(int))
    
    # Count occurrences
    for index, row in df.iterrows():
        senders = set(row[:4])  # Unique senders in this batch
        receivers = set(row[4:])  # Unique receivers in this batch
        
        for sender in senders:
            sender_counts[sender] += 1
            for receiver in receivers:
                pair_counts[sender][receiver] += 1
    
    # Calculate probabilities
    probabilities = defaultdict(lambda: defaultdict(float))
    for sender, receivers in pair_counts.items():
        for receiver, count in receivers.items():
            probabilities[sender][receiver] = count / sender_counts[sender]
    
    return probabilities

def plot_probabilities(probabilities):
    # Prepare data for plotting
    for sender in sorted(probabilities):
        receivers = probabilities[sender]
        receiver_labels = list(receivers.keys())
        probs = list(receivers.values())
        
        # Create a bar plot for each sender
        plt.figure(figsize=(10, 4))
        plt.bar(receiver_labels, probs, color='skyblue')
        plt.xlabel('Receiver')
        plt.ylabel('Probability')
        plt.title(f'Communication Probability from Sender {sender}')
        plt.ylim(0, 1)  # Ensure y-axis starts at 0 and ends at 1 for probability
        plt.show()

def main():
    # Specify the file path
    file_path = r"C:\Users\manue\Downloads\observation_mix.txt"  # Adjust the file path using a raw string
    
    # Load the data
    df = load_data(file_path)
    
    # Calculate communication probabilities
    probabilities = calculate_probabilities(df)
    
    # Plot the probabilities
    plot_probabilities(probabilities)

if __name__ == "__main__":
    main()
