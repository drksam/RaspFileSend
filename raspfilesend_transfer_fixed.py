import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
import configparser
from pathlib import Path
import threading
import subprocess

class RaspFileSendTransfer:
    def __init__(self, files):
        self.files = files
        self.config_file = Path.home() / ".raspfilesend_config.ini"
        self.config = configparser.ConfigParser()
        self.load_config()
        
        # Create GUI for target directory selection and transfer progress
        self.root = tk.Tk()
        self.root.title("Send Files to Raspberry Pi")
        self.root.geometry("700x650")  # Even bigger
        self.root.resizable(True, True)
        self.root.minsize(650, 600)
        self.setup_ui()
        
    def load_config(self):
        if not self.config_file.exists():
            # Try to find config in current directory as backup
            local_config = Path("raspfilesend_config.ini")
            if local_config.exists():
                self.config_file = local_config
            else:
                messagebox.showerror("Configuration Error", 
                                   f"No configuration found.\n\nExpected location: {self.config_file}\n\nPlease run raspfilesend_config.py first to set up your connection.")
                sys.exit(1)
        
        try:
            self.config.read(self.config_file)
            
            # Verify we have the required sections and keys
            required_sections = ['SSH', 'TARGET']
            for section in required_sections:
                if not self.config.has_section(section):
                    raise configparser.NoSectionError(section)
            
            # Check required SSH settings
            ip = self.config.get('SSH', 'ip', fallback='').strip()
            username = self.config.get('SSH', 'username', fallback='').strip()
            
            if not ip or not username:
                messagebox.showerror("Configuration Error", 
                                   "SSH connection details are incomplete.\n\nPlease run raspfilesend_config.py to configure your connection settings.")
                sys.exit(1)
                
        except Exception as e:
            messagebox.showerror("Configuration Error", 
                               f"Error reading configuration: {e}\n\nPlease run raspfilesend_config.py to reconfigure.")
            sys.exit(1)
        
    def setup_ui(self):
        # Use grid layout for better control
        self.root.grid_rowconfigure(0, weight=1)  # Content area expands
        self.root.grid_rowconfigure(1, weight=0)  # Button area fixed
        self.root.grid_columnconfigure(0, weight=1)
        
        # Content frame (expandable)
        content_frame = tk.Frame(self.root, padx=20, pady=20)
        content_frame.grid(row=0, column=0, sticky="nsew")
        
        # Files to send
        files_frame = tk.LabelFrame(content_frame, text="📁 Files to Send", padx=15, pady=15)
        files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # File list with scrollbar
        file_list_frame = tk.Frame(files_frame)
        file_list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.files_listbox = tk.Listbox(file_list_frame, font=("Arial", 10))
        file_scrollbar = tk.Scrollbar(file_list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=file_scrollbar.set)
        
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        for file_path in self.files:
            self.files_listbox.insert(tk.END, os.path.basename(file_path))
        
        # Target directory
        target_frame = tk.LabelFrame(content_frame, text="🎯 Target Directory", padx=15, pady=15)
        target_frame.pack(fill=tk.X, pady=(0, 15))
        
        target_container = tk.Frame(target_frame)
        target_container.pack(fill=tk.X)
        
        self.target_var = tk.StringVar(value=self.config.get('TARGET', 'default_directory', fallback='/home/pi/uploads'))
        target_entry = tk.Entry(target_container, textvariable=self.target_var, font=("Arial", 11))
        target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        change_btn = tk.Button(target_container, text="Change", command=self.change_target_directory, 
                              font=("Arial", 10))
        change_btn.pack(side=tk.RIGHT)
        
        # Progress frame (fixed height)
        progress_frame = tk.LabelFrame(content_frame, text="📊 Transfer Progress", padx=15, pady=15)
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        progress_container = tk.Frame(progress_frame)
        progress_container.pack(fill=tk.X)
        
        self.progress_text = tk.Text(progress_container, height=4, state=tk.DISABLED, font=("Consolas", 9))
        progress_scrollbar = tk.Scrollbar(progress_container, orient=tk.VERTICAL, command=self.progress_text.yview)
        self.progress_text.configure(yscrollcommand=progress_scrollbar.set)
        
        self.progress_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        progress_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # BUTTON FRAME - Fixed at bottom (row=1)
        button_frame = tk.Frame(self.root, bg="#2E2E2E", padx=20, pady=20)
        button_frame.grid(row=1, column=0, sticky="ew")
        
        # Inner container for buttons
        button_container = tk.Frame(button_frame, bg="#2E2E2E")
        button_container.pack(expand=True)
        
        # Large, prominent Send button
        self.send_button = tk.Button(
            button_container, 
            text="🚀 SEND FILES",
            command=self.start_transfer,
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            relief=tk.RAISED,
            borderwidth=3,
            cursor="hand2"
        )
        self.send_button.pack(side=tk.LEFT, padx=(0, 20))
        
        # Cancel button
        cancel_button = tk.Button(
            button_container,
            text="❌ CANCEL",
            command=self.root.quit,
            font=("Arial", 12, "bold"),
            bg="#F44336",
            fg="white",
            width=12,
            height=2,
            relief=tk.RAISED,
            borderwidth=2,
            cursor="hand2"
        )
        cancel_button.pack(side=tk.RIGHT)
        
        # Status label
        self.status_label = tk.Label(
            button_frame,
            text="✅ Ready to transfer files to Raspberry Pi",
            font=("Arial", 10),
            bg="#2E2E2E",
            fg="white"
        )
        self.status_label.pack(pady=(10, 0))
        
    def log_message(self, message):
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state=tk.DISABLED)
        self.root.update()
        
    def change_target_directory(self):
        current_dir = self.target_var.get()
        new_dir = simpledialog.askstring("Target Directory", 
                                        "Enter target directory path:", 
                                        initialvalue=current_dir,
                                        parent=self.root)
        if new_dir:
            self.target_var.set(new_dir)
            # Update config file with new default
            self.config.set('TARGET', 'default_directory', new_dir)
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            
    def start_transfer(self):
        # Disable button during transfer
        self.send_button.config(state=tk.DISABLED, text="🔄 TRANSFERRING...")
        self.status_label.config(text="🔄 Transfer in progress...")
        
        # Validate inputs first
        if not self.files:
            messagebox.showerror("Error", "No files specified for transfer.", parent=self.root)
            self.send_button.config(state=tk.NORMAL, text="🚀 SEND FILES")
            self.status_label.config(text="✅ Ready to transfer files")
            return
        
        # Get connection details
        ip = self.config.get('SSH', 'ip', fallback='')
        username = self.config.get('SSH', 'username', fallback='')
        
        if not ip.strip() or not username.strip():
            messagebox.showerror("Configuration Error", 
                               "SSH connection details not configured.\nPlease run raspfilesend_config.py first.",
                               parent=self.root)
            self.send_button.config(state=tk.NORMAL, text="🚀 SEND FILES")
            self.status_label.config(text="❌ Configuration error")
            return
        
        # Get password if needed (on main thread)
        password = None
        auth_method = self.config.get('SSH', 'auth_method', fallback='password')
        
        if auth_method == "password":
            password = simpledialog.askstring("Password", 
                                            f"Enter password for {username}@{ip}:", 
                                            show='*', parent=self.root)
            if not password:
                self.log_message("Transfer cancelled - no password provided.")
                self.send_button.config(state=tk.NORMAL, text="🚀 SEND FILES")
                self.status_label.config(text="❌ Transfer cancelled")
                return
        
        def transfer():
            try:
                self.log_message("🔄 Starting file transfer...")
                
                # Import paramiko here to check if it's available
                try:
                    import paramiko
                except ImportError:
                    self.root.after(0, lambda: self.log_message("❌ ERROR: paramiko library not found. Please install it with: pip install paramiko"))
                    self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL, text="🚀 SEND FILES"))
                    self.root.after(0, lambda: self.status_label.config(text="❌ Missing dependency"))
                    return
                
                port = int(self.config.get('SSH', 'port', fallback='22'))
                key_path = self.config.get('SSH', 'key_path', fallback='')
                target_dir = self.target_var.get()
                
                # Establish SSH connection
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                self.root.after(0, lambda: self.log_message(f"🔌 Connecting to {username}@{ip}:{port}..."))
                
                if auth_method == "password":
                    ssh.connect(hostname=ip, username=username, password=password, port=port, timeout=15)
                else:
                    ssh.connect(hostname=ip, username=username, key_filename=key_path, port=port, timeout=15)
                
                self.root.after(0, lambda: self.log_message("✅ Connected successfully!"))
                
                # Create target directory if it doesn't exist
                stdin, stdout, stderr = ssh.exec_command(f"mkdir -p {target_dir}")
                
                # Start SFTP session
                sftp = ssh.open_sftp()
                
                # Transfer each file
                for i, file_path in enumerate(self.files, 1):
                    if not os.path.exists(file_path):
                        self.root.after(0, lambda fp=file_path: self.log_message(f"⚠️ WARNING: File not found: {fp}"))
                        continue
                        
                    filename = os.path.basename(file_path)
                    remote_path = f"{target_dir}/{filename}"
                    
                    self.root.after(0, lambda fn=filename, idx=i, total=len(self.files): 
                                  self.log_message(f"📤 Transferring [{idx}/{total}]: {fn}"))
                    
                    try:
                        # Check if file already exists and ask for confirmation
                        file_exists = False
                        try:
                            sftp.stat(remote_path)
                            file_exists = True
                        except FileNotFoundError:
                            pass  # File doesn't exist, continue with transfer
                        
                        if file_exists:
                            # Ask on main thread
                            response = [None]  # Use list to allow modification in nested function
                            def ask_overwrite():
                                response[0] = messagebox.askyesno("File Exists", 
                                                                f"File '{filename}' already exists on the Raspberry Pi.\n\nOverwrite?",
                                                                parent=self.root)
                            
                            self.root.after(0, ask_overwrite)
                            
                            # Wait for response
                            while response[0] is None:
                                import time
                                time.sleep(0.1)
                            
                            if not response[0]:
                                self.root.after(0, lambda fn=filename: self.log_message(f"⏭️ Skipped: {fn}"))
                                continue
                        
                        # Transfer the file
                        sftp.put(file_path, remote_path)
                        file_size = os.path.getsize(file_path)
                        self.root.after(0, lambda fn=filename, fs=file_size: 
                                      self.log_message(f"✅ Transferred: {fn} ({fs:,} bytes)"))
                        
                    except Exception as e:
                        self.root.after(0, lambda fn=filename, err=str(e): 
                                      self.log_message(f"❌ Failed to transfer {fn}: {err}"))
                
                sftp.close()
                ssh.close()
                
                self.root.after(0, lambda: self.log_message(f"\n🎉 Transfer completed! Files sent to: {target_dir}"))
                self.root.after(0, lambda: self.status_label.config(text="🎉 Transfer completed successfully!"))
                self.root.after(0, lambda: messagebox.showinfo("Transfer Complete", 
                                                              f"Files have been successfully sent to {ip}:{target_dir}",
                                                              parent=self.root))
                
            except Exception as e:
                error_msg = f"Transfer failed: {str(e)}"
                self.root.after(0, lambda: self.log_message(f"❌ ERROR: {error_msg}"))
                self.root.after(0, lambda: self.status_label.config(text="❌ Transfer failed"))
                self.root.after(0, lambda: messagebox.showerror("Transfer Error", error_msg, parent=self.root))
            finally:
                # Re-enable button
                self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL, text="🚀 SEND FILES"))
        
        # Run transfer in separate thread to avoid blocking UI
        threading.Thread(target=transfer, daemon=True).start()
        
    def run(self):
        self.root.mainloop()

def main():
    if len(sys.argv) < 2:
        messagebox.showerror("Error", "No files specified for transfer.")
        return
    
    files = sys.argv[1:]
    app = RaspFileSendTransfer(files)
    app.run()

if __name__ == "__main__":
    main()
