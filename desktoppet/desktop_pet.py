import tkinter as tk
from PIL import Image, ImageTk
import itertools, os

class DesktopPet:
    def __init__(self, gif_path):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # No title bar
        self.root.wm_attributes("-topmost", True)  # Always on top
        self.root.wm_attributes("-transparentcolor", "white")  # Transparency
        self.root.config(bg='white')

        # Load GIF frames
        self.original_frames = []
        img = Image.open(gif_path)
        try:
            while True:
                frame = ImageTk.PhotoImage(img.copy().convert("RGBA"))
                self.original_frames.append(frame)
                img.seek(len(self.original_frames))
        except EOFError:
            pass

        self.frames = list(self.original_frames)
        self.frame_cycle = itertools.cycle(self.frames)

        # Create label to display the GIF
        self.label = tk.Label(self.root, bg="white", bd=0)
        self.label.pack()

        # Bind movement (left-click drag)
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

        # Bind resizing (right-click drag)
        self.label.bind("<Button-3>", self.start_resize)
        self.label.bind("<B3-Motion>", self.do_resize)

        # Double-click to disappear
        self.label.bind("<Double-Button-1>", self.fade_and_close)

        # Animation
        self.update_animation()
        self.root.geometry("+200+200")

        # Resize tracking
        self.resize_start_x = 0
        self.resize_start_y = 0
        self.resize_width = None
        self.resize_height = None

        self.root.mainloop()

    def update_animation(self):
        frame = next(self.frame_cycle)
        self.label.configure(image=frame)
        self.root.after(100, self.update_animation)

    # Dragging
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{x}+{y}")

    # Resizing
    def start_resize(self, event):
        self.resize_start_x = event.x_root
        self.resize_start_y = event.y_root
        self.resize_width = self.frames[0].width()
        self.resize_height = self.frames[0].height()

    def do_resize(self, event):
        dx = event.x_root - self.resize_start_x
        dy = event.y_root - self.resize_start_y
        new_width = max(20, self.resize_width + dx)
        new_height = max(20, self.resize_height + dy)
        self.resize_pet(new_width, new_height)

    def resize_pet(self, width, height):
        resized_frames = []
        for f in self.original_frames:
            img = ImageTk.getimage(f)
            resized = img.resize((int(width), int(height)), Image.LANCZOS)
            resized_frames.append(ImageTk.PhotoImage(resized))
        self.frames = resized_frames
        self.frame_cycle = itertools.cycle(self.frames)
        self.label.configure(image=self.frames[0])

    # Fade out and close
    def fade_and_close(self, event=None):
        self.fade_step(1.0)

    def fade_step(self, alpha):
        if alpha <= 0:
            self.root.destroy()
            return
        self.root.attributes("-alpha", alpha)
        self.root.after(50, self.fade_step, alpha - 0.1)

if __name__ == "__main__":
    DesktopPet(os.path.join(os.path.dirname(__file__), "pet.gif"))
