import tkinter as tk
from tkinter import ttk

def create_test_window():
    """Test window to debug button visibility"""
    root = tk.Tk()
    root.title("Transfer Window Test")
    root.geometry("650x600")
    root.configure(bg="lightblue")  # Background color to see window boundaries
    
    # Main frame
    main_frame = tk.Frame(root, padx=20, pady=20, bg="lightgreen")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Test sections
    frame1 = tk.LabelFrame(main_frame, text="Files (Height=100)", height=100, bg="yellow")
    frame1.pack(fill=tk.X, pady=(0, 10))
    frame1.pack_propagate(False)  # Keep fixed height
    
    frame2 = tk.LabelFrame(main_frame, text="Target (Height=60)", height=60, bg="orange")
    frame2.pack(fill=tk.X, pady=(0, 10))
    frame2.pack_propagate(False)  # Keep fixed height
    
    frame3 = tk.LabelFrame(main_frame, text="Progress (Height=100)", height=100, bg="pink")
    frame3.pack(fill=tk.X, pady=(0, 10))
    frame3.pack_propagate(False)  # Keep fixed height
    
    # BUTTONS - This should always be visible
    button_frame = tk.LabelFrame(main_frame, text="🚀 BUTTONS - ALWAYS VISIBLE", 
                               padx=20, pady=20, bg="red", fg="white",
                               relief=tk.RIDGE, borderwidth=5)
    button_frame.pack(fill=tk.X, pady=(10, 0), side=tk.BOTTOM)
    
    # Big buttons
    send_btn = tk.Button(button_frame, text="🚀 SEND FILES", 
                        bg="green", fg="white", font=("Arial", 16, "bold"),
                        height=3, width=20)
    send_btn.pack(side=tk.LEFT, padx=10)
    
    cancel_btn = tk.Button(button_frame, text="❌ CANCEL", 
                          bg="darkred", fg="white", font=("Arial", 14, "bold"),
                          height=3, width=15)
    cancel_btn.pack(side=tk.RIGHT, padx=10)
    
    # Info label
    info_label = tk.Label(button_frame, text="If you can see this, the buttons should work!", 
                         bg="red", fg="white", font=("Arial", 12))
    info_label.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_test_window()
