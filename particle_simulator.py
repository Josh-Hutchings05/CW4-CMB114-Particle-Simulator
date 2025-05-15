import tkinter as tk
import random
import math

R = 0.0821  # Ideal gas constant (L·atm/mol·K)
MOLECULE_RADIUS = 5
MAX_MOLECULES = 30

def speed_to_color(speed, max_speed):
    ratio = min(speed / max_speed, 1.0)
    red = int(255 * ratio)
    blue = int(255 * (1 - ratio))
    return f"#{red:02x}00{blue:02x}"

class Molecule:
    def __init__(self, canvas, x, y, vx, vy):
        self.canvas = canvas
        self.vx = vx
        self.vy = vy
        self.x = x
        self.y = y
        self.id = canvas.create_oval(
            x, y, x + MOLECULE_RADIUS * 2, y + MOLECULE_RADIUS * 2,
            fill="blue", outline=""
        )

    def speed(self):
        return math.hypot(self.vx, self.vy)

    def update_color(self, max_speed):
        color = speed_to_color(self.speed(), max_speed)
        self.canvas.itemconfig(self.id, fill=color)

    def move(self, width, height):
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
        min_dist = MOLECULE_RADIUS * 2

        if distance < min_dist and distance > 0:
            overlap = min_dist - distance
            nx = dx / distance
            ny = dy / distance

            self.x -= nx * overlap / 2
            self.y -= ny * overlap / 2
            other.x += nx * overlap / 2
            other.y += ny * overlap / 2

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
        self.root.title("Gas Simulation with Energy Visualization")

        control_frame = tk.Frame(root)
        control_frame.pack()

        self.volume_slider = tk.Scale(control_frame, from_=10, to=100, label="Volume (L)", orient=tk.HORIZONTAL)
        self.temp_slider = tk.Scale(control_frame, from_=100, to=1000, label="Temperature (K)", orient=tk.HORIZONTAL)
        self.pressure_slider = tk.Scale(control_frame, from_=0.5, to=5.0, resolution=0.1, label="Pressure (atm)", orient=tk.HORIZONTAL)

        self.volume_slider.set(50)
        self.temp_slider.set(300)
        self.pressure_slider.set(1.0)

        self.volume_slider.grid(row=0, column=0, padx=10, pady=5)
        self.temp_slider.grid(row=1, column=0, padx=10, pady=5)
        self.pressure_slider.grid(row=2, column=0, padx=10, pady=5)

        self.start_button = tk.Button(control_frame, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=3, column=0, pady=5)

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.info_label = tk.Label(root, text="Temperature (avg KE): 0.00")
        self.info_label.pack()

        self.molecules = []
        self.running = False

    def start_simulation(self):
        self.canvas.delete("all")
        self.molecules = []

        volume = self.volume_slider.get()
        temperature = self.temp_slider.get()
        pressure = self.pressure_slider.get()

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

        width, height = 400, 400

        for i, m1 in enumerate(self.molecules):
            for m2 in self.molecules[i + 1:]:
                m1.check_collision(m2)

        total_energy = 0
        max_speed = max((mol.speed() for mol in self.molecules), default=1)

        for mol in self.molecules:
            mol.move(width, height)
            mol.update_color(max_speed)
            total_energy += mol.vx**2 + mol.vy**2  # KE proxy: v²

        avg_ke = total_energy / max(len(self.molecules), 1)
        self.info_label.config(text=f"Temperature (avg KE): {avg_ke:.2f}")

        self.root.after(20, self.animate)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = GasSimulationApp(root)
    root.mainloop()