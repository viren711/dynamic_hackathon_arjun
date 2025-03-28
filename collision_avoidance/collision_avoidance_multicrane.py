import tkinter as tk
from tkinter import filedialog
import math
from PIL import Image, ImageTk

# Constants
CANVAS_SIZE = 500
CRANE_RADIUS = 50
JIB_LENGTH = 100
MIN_JIB_LENGTH = CRANE_RADIUS + 10  
MAX_JIB_LENGTH = CANVAS_SIZE // 2 - 10  
WARNING_DISTANCE = 100  

class CraneSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Crane Simulator")
        
        self.canvas = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas.pack()
        
        self.image_path = filedialog.askopenfilename(title="Select an Image")
        self.tk_image = None
        if self.image_path:
            self.load_image()
        
        self.cranes = [
            {"x": CANVAS_SIZE // 3, "y": CANVAS_SIZE // 2, "angle": 0, "jib_length": JIB_LENGTH, "color": "blue"},
            {"x": 2 * CANVAS_SIZE // 3, "y": CANVAS_SIZE // 2, "angle": 0, "jib_length": JIB_LENGTH, "color": "green"}
        ]
        
        self.restricted_polygons = []
        self.temp_polygon = []
        self.polygon_filled = False 
        
        self.canvas.bind("<Button-1>", self.add_polygon_point)
        self.root.bind("<KeyPress>", self.control_cranes)
        
        self.save_button = tk.Button(root, text="Save Polygon", command=self.save_polygon)
        self.save_button.pack()
        
        self.fill_button = tk.Button(root, text="Fill Polygon", command=self.fill_polygon)
        self.fill_button.pack()
        
        self.warning_text = None  # Store warning message reference
        self.draw_scene()
    
    def load_image(self):
        try:
            image = Image.open(self.image_path)
            image = image.resize((CANVAS_SIZE, CANVAS_SIZE))
            self.tk_image = ImageTk.PhotoImage(image)
        except Exception as e:
            print("Error loading image:", e)
    
    def add_polygon_point(self, event):
        x, y = event.x, event.y
        self.temp_polygon.append((x, y))
        self.draw_scene()
    
    def save_polygon(self):
        if len(self.temp_polygon) > 2:
            self.restricted_polygons.append(self.temp_polygon[:])
            self.temp_polygon = []
            self.polygon_filled = False
            self.draw_scene()
    
    def fill_polygon(self):
        if self.restricted_polygons:
            self.polygon_filled = True
            self.draw_scene()
    
    def draw_scene(self):
        self.canvas.delete("all")
        if self.tk_image:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        
        for polygon in self.restricted_polygons:
            if len(polygon) > 2:
                self.canvas.create_polygon(polygon, outline="red", fill="red" if self.polygon_filled else "", width=2)
        
        if len(self.temp_polygon) > 1:
            self.canvas.create_line(self.temp_polygon, fill="red", width=2)
        
        crane_positions = []
        restricted_warning = False  

        for crane in self.cranes:
            jib_x = crane["x"] + crane["jib_length"] * math.cos(math.radians(crane["angle"]))
            jib_y = crane["y"] + crane["jib_length"] * math.sin(math.radians(crane["angle"]))
            
            if self.is_inside_polygon(jib_x, jib_y):
                restricted_warning = True  
            
            crane_positions.append((jib_x, jib_y))
            
            self.canvas.create_oval(
                crane["x"] - CRANE_RADIUS, crane["y"] - CRANE_RADIUS,
                crane["x"] + CRANE_RADIUS, crane["y"] + CRANE_RADIUS,
                outline="black", width=2
            )
            
            self.canvas.create_line(crane["x"], crane["y"], jib_x, jib_y, fill=crane["color"], width=3)
            self.canvas.create_oval(jib_x - 5, jib_y - 5, jib_x + 5, jib_y + 5, fill=crane["color"])
        
        # Show warning for restricted area
        if restricted_warning:
            self.canvas.create_text(CANVAS_SIZE // 2, 50, text="Warning: Crane in Restricted Area!", fill="red", font=("Arial", 15, "bold"))

        # Show warning for crane proximity
        if self.check_crane_proximity(crane_positions):
            self.canvas.create_text(CANVAS_SIZE // 2, 30, text="Warning: Cranes Too Close!", fill="orange", font=("Arial", 15, "bold"))
    
    def check_crane_proximity(self, positions):
        if len(positions) < 2:
            return False
        x1, y1 = positions[0]
        x2, y2 = positions[1]
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance < WARNING_DISTANCE
    
    def is_inside_polygon(self, x, y):
        for polygon in self.restricted_polygons:
            if self.point_in_polygon(x, y, polygon):
                return True
        return False
    
    def point_in_polygon(self, x, y, polygon):
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if min(p1y, p2y) < y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
            p1x, p1y = p2x, p2y
        return inside
    
    def control_cranes(self, event):
        keys = {'w': 0, 's': 0, 'a': 0, 'd': 0, 'Up': 1, 'Down': 1, 'Left': 1, 'Right': 1}
        if event.keysym in keys:
            crane_index = keys[event.keysym]
            crane = self.cranes[crane_index]
            old_angle = crane["angle"]
            old_jib_length = crane["jib_length"]

            if event.keysym in ['w', 'Up']:
                crane["jib_length"] = min(crane["jib_length"] + 5, MAX_JIB_LENGTH)
            elif event.keysym in ['s', 'Down']:
                crane["jib_length"] = max(crane["jib_length"] - 5, MIN_JIB_LENGTH)
            elif event.keysym in ['a', 'Left']:
                crane["angle"] = (crane["angle"] - 5) % 360
            elif event.keysym in ['d', 'Right']:
                crane["angle"] = (crane["angle"] + 5) % 360

            jib_x = crane["x"] + crane["jib_length"] * math.cos(math.radians(crane["angle"]))
            jib_y = crane["y"] + crane["jib_length"] * math.sin(math.radians(crane["angle"]))

            if self.is_inside_polygon(jib_x, jib_y):
                crane["angle"] = old_angle
                crane["jib_length"] = old_jib_length  

            self.draw_scene()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = CraneSimulator(root)
    root.mainloop()
