import numpy as np
import vedo
from scipy.spatial import cKDTree
from scipy.interpolate import griddata
import time

# Load Brain Mesh (Change 'brain.stl' to your model file)
brain_mesh = vedo.load("brain.obj").c("gray")  # Load & color it gray

# Define EEG 10-10 system approximate positions (relative to a sphere)
electrode_labels = ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2", "T7", "T8", "Fz", "Cz", "Pz", "Oz"]
theta_phi_positions = [  # (theta, phi) in spherical coordinates
    (45, -45), (45, 45),  # Fp1, Fp2
    (60, -30), (60, 30),  # F3, F4
    (90, -30), (90, 30),  # C3, C4
    (120, -30), (120, 30),  # P3, P4
    (135, -45), (135, 45),  # O1, O2
    (90, -90), (90, 90),  # T7, T8
    (45, 0), (90, 0), (120, 0), (150, 0)  # Fz, Cz, Pz, Oz (midline)
]

# Convert spherical coordinates to Cartesian (assuming unit sphere)
electrodes = []
for (theta, phi), label in zip(theta_phi_positions, electrode_labels):
    x = np.sin(np.radians(theta)) * np.cos(np.radians(phi))
    y = np.sin(np.radians(theta)) * np.sin(np.radians(phi))
    z = np.cos(np.radians(theta))
    electrodes.append((x, y, z, label))

# Scale & project electrodes onto the brain mesh
brain_center = brain_mesh.center_of_mass()
brain_radius = brain_mesh.diagonal_size() / 3
electrode_points = [vedo.Point(np.array([y, x, z]) * brain_radius + brain_center, r=10, c="red") for x, y, z, _ in electrodes]
electrode_labels = [vedo.Text3D(label, np.array([y, x, z]) * brain_radius + brain_center, s=.4, c="black") for x, y, z, label in electrodes]

# Display the brain mesh with electrodes
vedo.show(brain_mesh, *electrode_points, *electrode_labels, axes=1, title="EEG Electrode Positions")
