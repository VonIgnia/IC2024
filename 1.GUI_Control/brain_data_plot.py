import numpy as np
import vedo
import random
import time
#import math
from vedo import *
from scipy.spatial import cKDTree
from scipy.interpolate import griddata

# Load Brain Mesh (Change 'brain.obj' to your model file)
brain = vedo.Mesh("brain.obj").c("white") # Load & color it gray
#brain.c('white').lighting('glossy')

electrode_labels = [
    "Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2",
    "T7", "T8", "F7", "F8", "FC5", "FC6", "CP5", "CP6", "P7", "P8",
    "AF3", "AF4", "F1", "F2", "F5", "F6", "FT7", "FT8", "FC1", "FC2",
    "C1", "C2", "C5", "C6", "TP7", "TP8", "CP1", "CP2", "P1", "P2",
    "P5", "P6", "PO3", "PO4", "PO7", "PO8", "O9", "O10", "Iz",
    "Fz", "FCz", "Cz", "CPz", "Pz", "POz", "Oz",
    "AF7", "AF8", "AFF1h", "AFF2h", "FFC1h", "FFC2h", "FCC1h", "FCC2h",
    "CPP1h", "CPP2h", "PPO1h", "PPO2h", "POO1h", "POO2h",
    "FFT7h", "FFT8h", "FTT9h", "FTT10h", "TTP7h", "TTP8h", "TPP9h", "TPP10h",
    "FT9", "FT10", "TP9", "TP10"
]

# Approximate (theta, phi) positions for each electrode in spherical coordinates
theta_phi_positions = [
    (45, -45), (45, 45),  # Fp1, Fp2
    (60, -30), (60, 30),  # F3, F4
    (90, -30), (90, 30),  # C3, C4
    (120, -30), (120, 30),  # P3, P4
    (135, -45), (135, 45),  # O1, O2
    (90, -90), (90, 90),  # T7, T8
    (60, -60), (60, 60),  # F7, F8
    (75, -45), (75, 45),  # FC5, FC6
    (105, -45), (105, 45),  # CP5, CP6
    (120, -60), (120, 60),  # P7, P8
    (30, -30), (30, 30),  # AF3, AF4
    (45, -15), (45, 15),  # F1, F2
    (60, -15), (60, 15), (60, -45), (60, 45),  # F5, F6
    (75, -60), (75, 60),  # FT7, FT8
    (75, -15), (75, 15),  # FC1, FC2
    (90, -15), (90, 15),  # C1, C2
    (90, -45), (90, 45),  # C5, C6
    (105, -60), (105, 60),  # TP7, TP8
    (105, -15), (105, 15),  # CP1, CP2
    (120, -15), (120, 15),  # P1, P2
    (120, -45), (120, 45),  # P5, P6
    (135, -30), (135, 30),  # PO3, PO4
    (135, -60), (135, 60),  # PO7, PO8
    (150, -45), (150, 45),  # O9, O10
    (165, 0),  # Iz
    (45, 0), (75, 0), (90, 0), (105, 0), (120, 0), (135, 0), (150, 0),  # Fz, FCz, Cz, CPz, Pz, POz, Oz
    (30, -60), (30, 60),  # AF7, AF8
    (30, -15), (30, 15),  # AFF1h, AFF2h
    (45, -10), (45, 10),  # FFC1h, FFC2h
    (75, -10), (75, 10),  # FCC1h, FCC2h
    (105, -10), (105, 10),  # CPP1h, CPP2h
    (135, -10), (135, 10),  # PPO1h, PPO2h
    (150, -10), (150, 10),  # POO1h, POO2h
    (60, -75), (60, 75),  # FFT7h, FFT8h
    (75, -90), (75, 90),  # FTT9h, FTT10h
    (105, -75), (105, 75),  # TTP7h, TTP8h
    (120, -90), (120, 90),  # TPP9h, TPP10h
    (75, -120), (75, 120),  # FT9, FT10
    (105, -120), (105, 120)  # TP9, TP10
]

# Convert spherical coordinates to Cartesian (assuming unit sphere)
electrodes = []
for (theta, phi), label in zip(theta_phi_positions, electrode_labels):
    x = np.sin(np.radians(theta)) * np.cos(np.radians(phi))
    y = np.sin(np.radians(theta)) * np.sin(np.radians(phi))
    z = np.cos(np.radians(theta))
    electrodes.append((x, y, z, label))

# Scale & project electrodes onto the brain mesh
brain_center = brain.center_of_mass()
brain_radius = brain.diagonal_size() * 0.35
electrode_points = [vedo.Point(np.array([y, x, z]) * brain_radius + brain_center, r=10, c="red") for x, y, z, _ in electrodes]
electrode_labels = [vedo.Text3D(label, np.array([y, x, z]) * brain_radius + brain_center, s=.4, c="black") for x, y, z, label in electrodes]

# Interpolate electrode values onto the brain mesh
brain_points = brain.points  # Get the points of the brain mesh
electrode_positions = np.array([np.array([y, x, z]) * brain_radius + brain_center for x, y, z, _ in electrodes])

# Use a KDTree to find the nearest points on the brain mesh
kdtree = cKDTree(electrode_positions)
dist, indices = kdtree.query(brain_points)

frame = 0
#frame_label = [vedo.Text3D(frame, [0,0,0], s=.4, c="black")]

# Setup the scene
#world = Box([0,0,0], size=(1, 1, 1)).wireframe()
plt = Plotter(interactive=False)
plt.show(brain, electrode_points, electrode_labels, __doc__)
#plt.show(brain, electrode_points, electrode_labels, __doc__, viewup="y")

# plot loop update



while True:
#for frame in np.arange(0, 10, 1):
    time.sleep(1)
    #print("loopstart")
    
    # Initialize n empty lists, being n the number of electrodes
    #print("clean list")
    electrode_values = [[] for _ in electrodes]

    #print("random list")
    #Assign random values to each electrode each frame
    for i in range(0, len(electrode_values)):
        electrode_values[i].append(random.uniform(-1, 1))

    #print("interpol")
    # Interpolate the electrode values to the mesh points using griddata
    interpolated_values = griddata(electrode_positions, electrode_values, brain_points, method='linear',fill_value=0)

    #print("map")
    # Map the interpolated values to a coolwarm colormap
    #brain.cmap("coolwarm", interpolated_values, vmin=-1, vmax=1).add_scalarbar(title="Electrode Values", nlabels=5).show()
    brain.cmap("jet", interpolated_values, vmin=-1, vmax=1).add_scalarbar(title="Electrode Values", nlabels=5).show()

    
    plt.render()

plt.interactive()
plt.close()
