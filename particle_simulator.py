import tkinter as tk
import random
import math

# Constants
R = 0.0821  # Ideal gas constant (L·atm/mol·K)
MOLECULE_RADIUS = 5
MAX_MOLECULES = 30

class Molecule:
    def __init__(self, canvas, x, y, vx, vy):
        self.canvas = canvas
        self.vx = vx
        self.vy = vy
        self.x = x
        self.y = y
        self.id = canvas.create_oval(
            x, y, x + MOLECULE_RADIUS * 2, y + MOLECULE_RADIUS * 2, fill="blue"
        )

    def move(self, width, height):
        # Wall collision
        if self.x + self.vx < 0 or self.x + self.vx + MOLECULE_RADIUS * 2 > width:
            self.vx = -self.vx
        if self.y + self.vy < 0 or self.y + self.vy + MOLECULE_RADIUS * 2 > height:
            self.vy = -self.vy

        self.x += self.vx
        self.y += self.vy
        self.canvas.coords(self.id, self.x, self.y,
                           self.x + MOLECULE_RADIUS * 2,
                           self.y + MOLECULE_RADIUS * 2)

    def check_collision(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.hypot(dx, dy)
        if distance < MOLECULE_RADIUS * 2:
            # Simple 2D elastic collision for equal masses
            nx = dx / distance
            ny = dy / distance
            dvx = self.vx - other.vx
            dvy = self.vy - other.vy
            impact_speed = dvx * nx + dvy * ny

            if impact_speed > 0:
                return

            self.vx -= impact_speed * nx
            self.vy -= impact_speed * ny
            other.vx += impact_speed * nx
            other.vy += impact_speed * ny

class GasSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gas Molecule Simulation with Collisions")

        input_frame = tk.Frame(root)
        input_frame.pack()

        tk.Label(input_frame, text="Volume (L):").grid(row=0, column=0)
        tk.Label(input_frame, text="Temperature (K):").grid(row=1, column=0)
        tk.Label(input_frame, text="Pressure (atm):").grid(row=2, column=0)

        self.volume_entry = tk.Entry(input_frame)
        self.temp_entry = tk.Entry(input_frame)
        self.pressure_entry = tk.Entry(input_frame)

        self.volume_entry.grid(row=0, column=1)
        self.temp_entry.grid(row=1, column=1)
        self.pressure_entry.grid(row=2, column=1)

        self.start_button = tk.Button(input_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=3, column=0, columnspan=2)

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.molecules = []
        self.running = False

    def start_simulation(self):
        self.canvas.delete("all")
        self.molecules = []

        try:
            volume = float(self.volume_entry.get())
            temperature = float(self.temp_entry.get())
            pressure = float(self.pressure_entry.get())
        except ValueError:
            print("Invalid input")
            return

        n_moles = (pressure * volume) / (R * temperature)
        num_molecules = min(int(n_moles * 100), MAX_MOLECULES)

        avg_speed = math.sqrt(temperature) * 0.5

        for _ in range(num_molecules):
            x = random.randint(0, 400 - MOLECULE_RADIUS * 2)
            y = random.randint(0, 400 - MOLECULE_RADIUS * 2)
            angle = random.uniform(0, 2 * math.pi)
            vx = avg_speed * math.cos(angle)
            vy = avg_speed * math.sin(angle)
            mol = Molecule(self.canvas, x, y, vx, vy)
            self.molecules.append(mol)

        self.running = True
        self.animate()

    def animate(self):
        if not self.running:
            return

        width = 400
        height = 400

        # Check molecule collisions
        for i, m1 in enumerate(self.molecules):
            for m2 in self.molecules[i+1:]:
                m1.check_collision(m2)

        for mol in self.molecules:
            mol.move(width, height)

        self.root.after(20, self.animate)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GasSimulationApp(root)
    root.mainloop()
    
'''
Molecules are modeled as identical circles with elastic collisions.

Only pairwise collisions are checked each frame; fine for small numbers.

Edge case handling is simple—perfect overlap isn't deeply resolved.
'''