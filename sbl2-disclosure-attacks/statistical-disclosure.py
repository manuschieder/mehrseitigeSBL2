# Mehrseitige Sicherheit SS 24 - SBL 2
# Manuel Schieder, 2143783
# Gina Kastner, 2090593
# Python 3.9
from typing import List

import numpy

from observation import Observation
from operator import itemgetter
import numpy as np


# Loads observations from file as list of observation objects
def load_observations(file_path):
    observations = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' : ')
            senders = list(map(int, parts[0].split()))
            receivers = list(map(int, parts[1].split()))
            observations.append(Observation(senders, receivers))
    return observations

# Counts frequencies and returns them as a list of tuples (A, freq_A) where
# A is the total number of observations with sender A and
# freq_A is a list of frequencies for each receiver across all observations with sender A
def count_frequencies(observations: list[Observation], num_participants) -> list[tuple[int, list[int]]]:
    sender_array = np.array([observation.senders for observation in observations])
    receiver_array = np.array([observation.receivers for observation in observations])
    frequencies = []

    for sender in range(1, num_participants + 1):
        # Filter relevant rows for currently observed sender (e.g. all rows that contain the value 1)
        sender_occurrence = np.any(sender_array == sender, axis=1)  # boolean array
        potential_receivers = receiver_array[sender_occurrence]  # int array

        num_observations_with_sender = len(potential_receivers)

        # Flatten 2D array, count number of occurrences for each value in [0, 10] and save result for indices [1, 10]
        # (dropping index 0 as there is no receiver "0" and as such bincount is always 0)
        list_occurrences_receivers = numpy.bincount(potential_receivers.flatten()).tolist()[1:]

        frequencies.append((num_observations_with_sender, list_occurrences_receivers))

    return frequencies


# Calculate statistical disclosure attack matrix assuming a uniform distribution
def calc_sda(batch_size: int, frequencies: list[tuple[int, list[int]]]) -> list[list[float]]:
    num_participants = len(frequencies[0][1])

    # values of vector R same for all indices => simpler calculation as constant subtrahend than with vector
    subtrahend = (batch_size - 1) * 1. / num_participants

    freq_array = np.array([freq_tuple[1] for freq_tuple in frequencies])  # transfer receiver frequency lists to array
    freq_div = np.array([freq_array[i].astype(float) / frequencies[i][0] for i in
                         range(0, len(freq_array))])  # apply calculation (freq_A / A) to each value

    sda_lists = np.array([(freq_div[i] - subtrahend) for i in range(0, len(freq_array))]).tolist()
    return sda_lists


# Returns a list of the most likely contacts
def get_most_likely_contacts(sda_lists: list[list[float]], num: int) -> list[list[float]]:
    most_likely_contacts = []
    for sender in sda_lists:
        most_likely_contacts.append(list(sorted(enumerate(sender, start=1), key=itemgetter(1)))[
                                    :-(num + 1):-1])  # -1 for reverse order (most likely contact listed first)
    return most_likely_contacts


# Print method for list of frequency tuples (see count_frequencies)
def print_frequencies(frequencies: list[tuple[int, list[int]]]) -> None:
    print("Frequency matrix:")
    print(f"{'':33s}Receiver")
    heading = f"{'':10s} Total {1:3d}"
    for i in range(2, len(frequencies) + 1):
        heading += f"{i:6d}"
    print(heading)
    for i in range(1, len(frequencies) + 1):
        print(f"Sender {i:2d} {frequencies[i - 1][0]:6d} {frequencies[i - 1][1]}")
    print()


# Print method for list of frequency tuples (see count_frequencies)
def print_sda_results(sda_list: list[list[float]], most_likely_contacts: list[list[float]]) -> None:
    print("Statistical disclosure attack results:")
    print(f"{'':33s}Receiver")
    heading = f"{'':10s} {1:6d}"
    for i in range(2, len(sda_list) + 1):
        heading += f"{i:12d}"
    print(heading + f"{' ':12s}" + "Contacts")
    for i in range(1, len(sda_list) + 1):
        print(f"Sender {i:2d} "
              f"{[format(x, '+.5f') for x in sda_list[i - 1]]} "
              f"{' ':5s} "
              f"{[idx for idx, value in most_likely_contacts[i - 1]]}")
    print()


#####################

file_path = "observation_mix.txt"
observations = load_observations(file_path)
batch_size = len(observations[0].senders)
num_participants = 10

print("Example observation:")
print(observations[0])
print()

frequencies = count_frequencies(observations, num_participants)
print_frequencies(frequencies)

sda_lists = calc_sda(batch_size, frequencies)

n_contacts = 2
most_likely_contacts = get_most_likely_contacts(sda_lists, n_contacts)

# Prints results, last column are most likely contacts for each sender
print_sda_results(sda_lists, most_likely_contacts)
