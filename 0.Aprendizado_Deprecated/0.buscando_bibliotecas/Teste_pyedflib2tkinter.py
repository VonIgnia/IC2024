from pyedflib import highlevel
import pyedflib as plib

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

path = "1.Dados_Anteriores\Raw Empirical EEG Data\EEG_Cat_Study4_Resting_S1.bdf" 
signals, signal_headers, header = highlevel.read_edf(path)

n = len(signals)


#print(header)
#print(signal_headers)

# Define colormap
cmap = cm.get_cmap("gist_rainbow")  # Use "gist_rainbow" or another colormap

# Compute average y-values for each signal
avg_values = np.array([np.mean(sig) for sig in signals])

# Get the ranking of average values (argsort sorts in ascending order)
ranked_indices = np.argsort(avg_values)  # Get sorted indices
ranks = np.argsort(ranked_indices)  # Get rank positions (0 = lowest, n-1 = highest)

# Normalize ranks to range [0, 1]
norm_ranks = ranks / (n - 1)

# Create a Tkinter window
root = tk.Tk()
root.title("Scrollable EEG Plots")
# Create a Matplotlib figure
fig, axes = plt.subplots(n, 1, figsize=(10, n * 2))  # Adjust figure size

# Plot each EEG signal
for i in range(n):
    if signal_headers[i]["label"] != "Status":
        color = cmap(norm_ranks[i])
        axes[i].plot(signals[i], label=signal_headers[i]["label"], color=color)
        axes[i].legend()
        axes[i].set_xlabel("Tempo (ms)")
        axes[i].set_ylabel("Amplitude (uV)")
        axes[i].set_title(signal_headers[i]["label"])


# Adjust spacing
plt.subplots_adjust(hspace=0.5)  

# Embed Matplotlib figure into Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.mainloop()  # Run the Tkinter loop
