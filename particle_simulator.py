import tkinter as tk
import random
import math

# Constants
R = 0.0821  # Ideal gas constant (L·atm/mol·K)
MOLECULE_RADIUS = 3
MAX_MOLECULES = 30

class Molecule:
    def __init__(self, canvas, x, y, vx, vy):
        self.canvas = canvas
        self.vx = vx
        self.vy = vy
        self.id = canvas.create_oval(x, y, x + MOLECULE_RADIUS*2, y + MOLECULE_RADIUS*2, fill="blue")

    def move(self, width, height):
        coords = self.canvas.coords(self.id)
        x1, y1, x2, y2 = coords

        if x1 + self.vx < 0 or x2 + self.vx > width:
            self.vx = -self.vx
        if y1 + self.vy < 0 or y2 + self.vy > height:
            self.vy = -self.vy

        self.canvas.move(self.id, self.vx, self.vy)

class GasSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gas Molecule Simulation")

        # Input frame
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

        # Canvas for drawing
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

        # Ideal Gas Law: PV = nRT => n = PV / RT
        n_moles = (pressure * volume) / (R * temperature)
        num_molecules = min(int(n_moles * 100), MAX_MOLECULES)

        avg_speed = math.sqrt(temperature) * 0.5

        for _ in range(num_molecules):
            x = random.randint(0, 400 - MOLECULE_RADIUS*2)
            y = random.randint(0, 400 - MOLECULE_RADIUS*2)
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

        for mol in self.molecules:
            mol.move(400, 400)

        self.root.after(20, self.animate)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GasSimulationApp(root)
    root.mainloop()

'''    
This is a qualitative visualization, not a precise physical simulation.

The number of molecules is capped to maintain performance.

The molecule speed is based on the square root of temperature, following kinetic theory.
'''