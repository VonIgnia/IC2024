from pyedflib import highlevel
import pyedflib as plib

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm

path = "1.Dados_Anteriores\Raw Empirical EEG Data\EEG_Cat_Study4_Resting_S1.bdf" 
signals, signal_headers, header = highlevel.read_edf(path)

n = len(signals)

fig = plt.figure()
ax = plt.axes()

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

for i in np.arange(n):
    print(signal_headers[i]["label"])
    if signal_headers[i]["label"] != "Status":
        color = cmap(norm_ranks[i])  # Get color based on normalized average
        ax.plot(signals[i], label=signal_headers[i]["label"], color=color)

plt.xlabel("Tempo (ms)")
plt.ylabel("Amplitude(uV)")
plt.xlim(0, 4e4)
plt.ylim(-3.05e4, 2e3)
#plt.figlegend(bbox_to_anchor = (1, 0.5), loc = "right", ncol = 3)
plt.show()