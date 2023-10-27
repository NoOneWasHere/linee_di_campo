import numpy as np
import matplotlib.pyplot as plt

# Constants
k = 8.99e9  # Coulomb's constant in Nm^2/C^2

# Initialize empty lists to store charges and positions
charges = []
positions = []

# Function to calculate the electric field at a point
def calculate_electric_field(x, y):
    Ex = np.zeros_like(x)
    Ey = np.zeros_like(y)

    for i in range(len(x)):
        for j in range(len(y)):
            total_electric_field = np.zeros(2)

            for q, pos in zip(charges, positions):
                r = np.array([x[i, j] - pos[0], y[i, j] - pos[1]])
                r_mag = np.linalg.norm(r)
                e_field = (k * q / r_mag**2) * r / r_mag
                total_electric_field += e_field

            Ex[i, j] = total_electric_field[0]
            Ey[i, j] = total_electric_field[1]

    return Ex, Ey

# Interactive charge input
charge_number = 1
while True:
    try:
        q = float(input(f"Inserisci la carica (in Coulomb) per q{charge_number}: "))
        x = float(input(f"Inserisci la coordinata X (in metri) per q{charge_number}: "))
        y = float(input(f"Inserisci la coordinata Y (in metri) for q{charge_number}: "))
        charges.append(q)
        positions.append((x, y))
        
        another_particle = input("Vuoi inserire una nuova particella? (sì/no): ")
        if another_particle.lower() != 'sì' and another_particle.lower() != 'si':
            break
        charge_number += 1
    except ValueError:
        print("Input invalido. Inserisci un valido input numerico.")

# Create a grid of points for electric field calculation
x = np.linspace(min_x - 2, max_x + 2, 20)
y = np.linspace(min_x - 2, max_x + 2, 20)
X, Y = np.meshgrid(x, y)

# Calculate the electric field
Ex, Ey = calculate_electric_field(X, Y)

# Calculate the electric potential at each point
V = np.zeros_like(X)
for i in range(len(x)):
    for j in range(len(y)):
        total_potential = 0
        for q, pos in zip(charges, positions):
            r = np.array([x[i], y[j]]) - np.array(pos)
            r_mag = np.linalg.norm(r)
            potential = k * q / r_mag
            total_potential += potential
        V[j, i] = total_potential  # Reversed indexing for X and Y

# Calculate the vectors connecting the particles to form a polygon
polygon_vectors = np.zeros((len(charges), 2))
for i in range(len(charges)):
    for j in range(len(charges)):
        if i != j:
            r = np.array(positions[j]) - np.array(positions[i])
            r_mag = np.linalg.norm(r)
            if charges[i] * charges[j] < 0:
                polygon_vectors[i] += r / r_mag * abs(charges[j])
            else:
                polygon_vectors[i] -= r / r_mag * abs(charges[i])

# Define colors for charges and vectors
charge_colors = ['red' if q > 0 else 'blue' for q in charges]

# Determine the maximum and minimum coordinates
max_x = max([pos[0] for pos in positions])
min_x = min([pos[0] for pos in positions])
max_y = max([pos[1] for pos in positions])
min_y = min([pos[1] for pos in positions])

# Calculate the shift for charge labels based on the graph size
label_shift_x = (max_x - min_x) * 0.04
label_shift_y = (max_y - min_y) * 0.04

# Plot the electric potential as contours
plt.figure(figsize=(8, 8))
plt.subplot(2, 2, 1)  # Create the upper subplot
plt.contour(X, Y, V, cmap='viridis', levels=20)
for i, (q, pos) in enumerate(zip(charges, positions)):
    plt.scatter(pos[0], pos[1], c=['red' if q > 0 else 'blue'], marker='o', s=200, label=f'q{i+1} = {q} C')
    plt.text(pos[0] + label_shift_x, pos[1] - label_shift_y, f'q{i+1}', fontsize=12, ha='center', va='bottom')
plt.xlabel('X (metri)')
plt.ylabel('Y (metri)')
plt.title('Linee equipotenti')
plt.xlim(min_x - 2, max_x + 2)
plt.ylim(min_y - 2, max_y + 2)
plt.legend()
plt.grid(True)

# Create a separate subplot for the polygon vectors
plt.subplot(2, 2, 2)  # Create the lower subplot
for i in range(len(charges)):
    plt.quiver(positions[i][0], positions[i][1], polygon_vectors[i][0], polygon_vectors[i][1],
               angles='xy', scale_units='xy', scale=1, color='green', width=0.005, headwidth=10, headlength=10)
    plt.scatter(positions[i][0], positions[i][1], c=['red' if q > 0 else 'blue' for q in charges][i], marker='o', s=200, label=f'q{i+1} = {charges[i]} C')
    plt.text(positions[i][0] + label_shift_x, positions[i][1] - label_shift_y, f'q{i+1}', fontsize=12, ha='center', va='bottom')
plt.xlabel('X (metri)')
plt.ylabel('Y (metri)')
plt.title('Vettori')
plt.xlim(min_x - 2, max_x + 2)
plt.ylim(min_y - 2, max_y + 2)
plt.legend()
plt.grid(True)

# Create a separate subplot for electric field lines with arrowheads
plt.subplot(2, 2, 3)  # Create the lower-left subplot
plt.streamplot(X, Y, Ex, Ey, color='green', linewidth=1, density=.5, arrowstyle='->', arrowsize=1.5)
for i, (q, pos) in enumerate(zip(charges, positions)):
    plt.scatter(pos[0], pos[1], c=['red' if q > 0 else 'blue'], marker='o', s=200, label=f'q{i+1} = {q} C')
    plt.text(pos[0] + label_shift_x, pos[1] - label_shift_y, f'q{i+1}', fontsize=12, ha='center', va='bottom')
plt.xlabel('X (metri)')
plt.ylabel('Y (metri)')
plt.title('Linee di campo elettrico')
plt.xlim(min_x - 2, max_x + 2)
plt.ylim(min_y - 2, max_y + 2)
plt.legend(loc='upper right')
plt.grid(True)

plt.tight_layout()  # Ensure the subplots don't overlap
plt.show()
