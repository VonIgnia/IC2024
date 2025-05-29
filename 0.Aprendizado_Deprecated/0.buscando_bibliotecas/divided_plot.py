import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from pyedflib import highlevel

# Example data structure
path = "1.Dados_Anteriores\Raw Empirical EEG Data\EEG_Cat_Study4_Resting_S1.bdf" 
signals, signal_headers, header = highlevel.read_edf(path)
n = len(signal_headers)  # Number of signals

# Dictionaries to hold signals organized by region and side
regions = {
    'Pre-frontal': {'left': [], 'right': [], 'middle': []},
    'Frontal': {'left': [], 'right': [], 'middle': []},
    'Temporal': {'left': [], 'right': [], 'middle': []},
    'Parietal': {'left': [], 'right': [], 'middle': []},
    'Occipital': {'left': [], 'right': [], 'middle': []},
    'Central': {'left': [], 'right': [], 'middle': []},
    'Mixed': {'left': [], 'right': [], 'middle': []},
}

# Define a function to classify each signal label
def classify_signal(label):
    # Check the region based on the start of the label
    if label.startswith("Fp"):
        region = "Pre-frontal"
    elif label.startswith("F"):
        region = "Frontal"
    elif label.startswith("T"):
        region = "Temporal"
    elif label.startswith("P"):
        region = "Parietal"
    elif label.startswith("O"):
        region = "Occipital"
    elif label.startswith("C"):
        region = "Central"
    elif label.startswith("AF") or label.startswith("FT"):
        region = "Mixed"
    else:
        return None, None  # Invalid label, to be printed and removed

    # Determine the side based on the last character of the label
    if label[-1] == "Z":
        side = "middle"
    elif label[-1].isdigit():
        side = "right" if int(label[-1]) % 2 == 0 else "left"
    else:
        return None, None  # Invalid label, to be printed and removed

    return region, side

# Process and classify each signal
filtered_signals = []
for i in range(n):
    label = signal_headers[i]["label"]
    region, side = classify_signal(label)
    
    if region is not None and side is not None:
        # Append signal to appropriate region and side
        regions[region][side].append((label, signals[i]))
        filtered_signals.append(signals[i])
    else:
        print(f"Invalid label removed: {label}")

# Plotting
fig, axs = plt.subplots(3, 3, figsize=(15, 15))  # Adjust the grid for more regions as needed
fig.suptitle("Brain Region Signals")

for idx, (region, sides) in enumerate(regions.items()):
    for side, data in sides.items():
        # Select subplot axis based on region and side
        row = idx // 3
        col = idx % 3
        ax = axs[row, col]
        
        for label, signal in data:
            ax.plot(signal, label=label)
        ax.set_title(f"{region} ({side})")
        ax.legend(loc="upper right")

plt.tight_layout()
plt.show()