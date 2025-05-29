#muito lento, crasha
import numpy as np
import vedo
from scipy.spatial import cKDTree
import time

# Load Brain Mesh
brain_mesh = vedo.load("brain.obj").c("gray")

# Define EEG 10-10 system approximate positions
electrode_labels = ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2", "T7", "T8", "Fz", "Cz", "Pz", "Oz"]
theta_phi_positions = [(45, -45), (45, 45), (60, -30), (60, 30), (90, -30), (90, 30), (120, -30), (120, 30), 
                       (135, -45), (135, 45), (90, -90), (90, 90), (45, 0), (90, 0), (120, 0), (150, 0)]

# Convert spherical coordinates to Cartesian (positions of the electrodes)
electrodes = []
for (theta, phi), label in zip(theta_phi_positions, electrode_labels):
    x = np.sin(np.radians(theta)) * np.cos(np.radians(phi))
    y = np.sin(np.radians(theta)) * np.sin(np.radians(phi))
    z = np.cos(np.radians(theta))
    electrodes.append((x, y, z, label))

# Get the brain's center and radius
brain_center = brain_mesh.center_of_mass()
brain_radius = brain_mesh.diagonal_size() / 3

# Adjust electrode positions and scale by brain radius
electrode_positions = [np.array([y, x, z]) * brain_radius + brain_center for x, y, z, _ in electrodes]

# Simulate EEG time series data (you can replace this with actual EEG data)
# Example: 16 electrodes, 1000 time points
num_time_steps = 1000
eeg_data = np.random.rand(len(electrodes), num_time_steps)  # EEG data for each electrode over time

# Create a KDTree for fast spatial search (for interpolation purposes)
tree = cKDTree(electrode_positions)

# Interpolate EEG data onto the brain mesh for each time step
brain_points = brain_mesh.points  # All vertices of the brain mesh
distances, indices = tree.query(brain_points)  # Find closest electrodes

# Set up for animation of EEG data over time
plotter = vedo.Plotter()

# Create a list of actors for each time step
actors = []

# Loop through each time step (assuming the data has dimensions [num_electrodes, num_time_steps])
for t in range(num_time_steps):
    # Interpolate EEG values to the mesh vertices for the current time step
    interpolated_eeg = eeg_data[:, t][indices]  # Interpolated EEG data at time step t

    # Map the interpolated EEG data to the brain mesh (coloring based on activity)
    brain_mesh.pointdata["eeg"] = interpolated_eeg
    
    # Normalize EEG values for consistent color scaling
    eeg_min = np.min(interpolated_eeg)
    eeg_max = np.max(interpolated_eeg)
    normalized_eeg = (interpolated_eeg - eeg_min) / (eeg_max - eeg_min)

    # Apply the colormap using the normalized EEG data
    brain_mesh.c("coolwarm")  # Apply the color map

    # Create an actor for the current time step (used for animation)
    actors.append(brain_mesh.clone().c("coolwarm"))

# Animate the brain mesh (update the colors per time step)
plotter += actors[0]  # Initialize with the first frame
plotter.show(interactive=False)

# Run the animation loop
for i in range(1, len(actors)):
    plotter.render()
    plotter += actors[i]
    time.sleep(0.05)  # Sleep to control the speed of the animation

plotter.show()
print("Done")