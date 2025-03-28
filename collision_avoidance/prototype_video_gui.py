import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")
        
        # Open in a new separate window with a default maximized state
        self.root.state("zoomed")  # Maximized window
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        self.frame = tk.Frame(root, bg="white")  # Set background to white
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        self.label = tk.Label(self.frame, bg="white")  # Set background to white
        self.label.pack(expand=True, fill=tk.BOTH)
        
        # Center the button in the middle of the screen
        self.btn_open = tk.Button(root, text="Open Video", command=self.open_video)
        self.btn_open.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.cap = None
        
    def open_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", ".mp4;.avi;.mov;.mkv")])
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            self.btn_open.place_forget()  # Hide button when video starts playing
            
            # Get video resolution
            video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            if video_width and video_height:
                # Scale only if the video is larger than the screen
                if video_width > self.screen_width or video_height > self.screen_height:
                    scale_factor = min(self.screen_width / video_width, self.screen_height / video_height)
                    video_width = int(video_width * scale_factor)
                    video_height = int(video_height * scale_factor)
                
                # Set window size dynamically based on video resolution
                self.root.geometry(f"{video_width}x{video_height}")
                self.label.config(width=video_width, height=video_height)
            
            self.play_video()
        
    def play_video(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame)
                
                # Maintain aspect ratio without stretching
                video_width = self.label.winfo_width()
                video_height = self.label.winfo_height()
                frame.thumbnail((video_width, video_height), Image.LANCZOS)
                
                frame = ImageTk.PhotoImage(frame)
                
                self.label.config(image=frame)
                self.label.image = frame
                
                self.root.after(25, self.play_video)  # Adjust delay as needed
            else:
                self.cap.release()
                self.cap = None
                self.label.config(image="", bg="white")  # Clear the video and set background to white
                self.btn_open.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Show button again when video ends
        
if __name__ == "__main__":
    root = tk.Tk()
    root.state("zoomed")  # Open the window in maximized state by default
    player = VideoPlayer(root)
    root.mainloop()