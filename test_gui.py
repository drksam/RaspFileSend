import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the current directory to Python path so we can import the main module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_gui():
    """Simple test to verify GUI layout"""
    root = tk.Tk()
    root.title("RaspFileSend GUI Test")
    root.geometry("500x600")
    
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Test frame 1
    frame1 = ttk.LabelFrame(main_frame, text="Frame 1", padding="10")
    frame1.pack(fill=tk.X, pady=(0, 10))
    ttk.Label(frame1, text="This is frame 1").pack()
    
    # Test frame 2
    frame2 = ttk.LabelFrame(main_frame, text="Frame 2", padding="10")
    frame2.pack(fill=tk.X, pady=(0, 10))
    ttk.Label(frame2, text="This is frame 2").pack()
    
    # Test frame 3
    frame3 = ttk.LabelFrame(main_frame, text="Frame 3", padding="10")
    frame3.pack(fill=tk.X, pady=(0, 10))
    ttk.Label(frame3, text="This is frame 3").pack()
    
    # Test frame 4
    frame4 = ttk.LabelFrame(main_frame, text="Frame 4", padding="10")
    frame4.pack(fill=tk.X, pady=(0, 10))
    ttk.Label(frame4, text="This is frame 4").pack()
    
    # BUTTONS FRAME
    button_frame = ttk.LabelFrame(main_frame, text="BUTTONS", padding="10")
    button_frame.pack(fill=tk.X, pady=(10, 0))
    
    ttk.Button(button_frame, text="Save Settings", command=lambda: messagebox.showinfo("Test", "Save clicked!")).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(button_frame, text="Save and Exit", command=lambda: messagebox.showinfo("Test", "Save and Exit clicked!")).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(button_frame, text="Exit", command=root.quit).pack(side=tk.LEFT)
    
    root.mainloop()

if __name__ == "__main__":
    test_gui()
