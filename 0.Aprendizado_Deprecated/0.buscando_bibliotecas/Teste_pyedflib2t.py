from pyedflib import highlevel
import pyedflib as plib

import numpy as np

import matplotlib.pyplot as plt
import matplotlib

path = "1.Dados_Anteriores\Raw Empirical EEG Data\EEG_Cat_Study4_Resting_S1.bdf" 
signals, signal_headers, header = highlevel.read_edf(path)

# Sample data setup (replace this with your actual signals and signal_headers)
#fs = 256 # Sampling frequency (Hz)
fs = 2048
T = 1.0 / fs  # Sampling period

def compute_fft(signal, fs):
    n = len(signal)
    fft_result = np.fft.fft(signal)
    fft_freq = np.fft.fftfreq(n, T)
    return fft_freq, np.abs(fft_result) # Only take positive frequencies
    #return fft_freq[:n // 2], np.abs(fft_result)[:n // 2]  # Only take positive frequencies

n = len(signals)
n = 2 # only for easier observation


#print(header)
#print(signal_headers)

# Define colormap
cmap = matplotlib.colormaps["gist_rainbow"]  # Use"gist_rainbow"

# Compute average y-values for each signal
avg_values = np.array([np.mean(sig) for sig in signals])

# Get the ranking of average values (argsort sorts in ascending order)
ranked_indices = np.argsort(avg_values)  # Get sorted indices
ranks = np.argsort(ranked_indices)  # Get rank positions (0 = lowest, n-1 = highest)

# Normalize ranks to range [0, 1]
norm_ranks = ranks / (n - 1)

# plota todos individualmente
plt.title("Plot Reduzido")
for i in np.arange(n):
    plt.subplot(n,1,i+1) #n colunas, 1linha, seguindo o índice
    print(signal_headers[i]["label"])

    if signal_headers[i]["label"] != "Status":
        color = cmap(i / (n - 1))  # Get color based on normalized average
        plt.plot(signals[i], label=signal_headers[i]["label"], color=color)
        plt.legend(signal_headers[i]["label"], loc="upper right")
        plt.xlabel("Tempo (ms)")
        plt.ylabel("Amplitude(uV)") 

plt.subplots_adjust(hspace=1, wspace=0.3)
plt.show()

plt.title("Plot Reduzido Frequency")

for i in np.arange(n):
    plt.subplot(n,1,i+1) #n colunas, 1linha, seguindo o índice
    print(signal_headers[i]["label"])

    if signal_headers[i]["label"] != "Status":
        fft_freq, fft_magnitude = compute_fft(signals[i], fs)
        color = cmap(i / (n - 1))  # Get color based on normalized average
        plt.plot(fft_freq, fft_magnitude, label=signal_headers[i]["label"], color=color)
        plt.legend(signal_headers[i]["label"], loc="upper right")
        plt.xlabel("Frequencia(Hz)")
        plt.ylabel("Magnitude") 

plt.subplots_adjust(hspace=1, wspace=0.3)
plt.show()