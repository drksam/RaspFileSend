import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import configparser
import os
import sys
import subprocess
from pathlib import Path
import threading
import base64
import hashlib

class RaspFileSendConfig:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("RaspFileSend Configuration")
        self.root.geometry("550x650")  # Even taller to ensure all content fits
        self.root.resizable(True, True)
        
        # Configuration file path
        self.config_file = Path.home() / ".raspfilesend_config.ini"
        self.config = configparser.ConfigParser()
        self.load_config()
        
        self.setup_ui()
        self.load_saved_settings()
        
    def setup_ui(self):
        # Main frame with scrollbar capability
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # SSH Connection Settings
        ssh_frame = ttk.LabelFrame(main_frame, text="SSH Connection Settings", padding="15")
        ssh_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create grid layout for SSH settings
        ttk.Label(ssh_frame, text="Raspberry Pi IP:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.ip_var = tk.StringVar()
        ttk.Entry(ssh_frame, textvariable=self.ip_var, width=35).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(15, 0))
        
        ttk.Label(ssh_frame, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.username_var = tk.StringVar()
        ttk.Entry(ssh_frame, textvariable=self.username_var, width=35).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(15, 0))
        
        ttk.Label(ssh_frame, text="Port:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.port_var = tk.StringVar(value="22")
        ttk.Entry(ssh_frame, textvariable=self.port_var, width=35).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=(15, 0))
        
        ttk.Label(ssh_frame, text="Authentication:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.auth_var = tk.StringVar(value="password")
        auth_frame = ttk.Frame(ssh_frame)
        auth_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=8, padx=(15, 0))
        ttk.Radiobutton(auth_frame, text="Password", variable=self.auth_var, value="password").pack(side=tk.LEFT)
        ttk.Radiobutton(auth_frame, text="SSH Key", variable=self.auth_var, value="key").pack(side=tk.LEFT, padx=(15, 0))
        
        ttk.Label(ssh_frame, text="SSH Key Path:").grid(row=4, column=0, sticky=tk.W, pady=8)
        key_frame = ttk.Frame(ssh_frame)
        key_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=8, padx=(15, 0))
        self.key_path_var = tk.StringVar()
        self.key_entry = ttk.Entry(key_frame, textvariable=self.key_path_var, width=28)
        self.key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(key_frame, text="Browse", command=self.browse_key_file).pack(side=tk.RIGHT, padx=(8, 0))
        
        # Password saving option
        ttk.Label(ssh_frame, text="Save Password:").grid(row=5, column=0, sticky=tk.W, pady=8)
        password_frame = ttk.Frame(ssh_frame)
        password_frame.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=8, padx=(15, 0))
        
        self.save_password_var = tk.BooleanVar()
        self.save_password_check = ttk.Checkbutton(password_frame, text="Remember password (encrypted)", 
                                                  variable=self.save_password_var, command=self.on_save_password_changed)
        self.save_password_check.pack(side=tk.LEFT)
        
        # Password entry (only shown when save password is enabled)
        ttk.Label(ssh_frame, text="Password:").grid(row=6, column=0, sticky=tk.W, pady=8)
        password_entry_frame = ttk.Frame(ssh_frame)
        password_entry_frame.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=8, padx=(15, 0))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_entry_frame, textvariable=self.password_var, show="*", width=28)
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.show_password_var = tk.BooleanVar()
        self.show_password_check = ttk.Checkbutton(password_entry_frame, text="Show", 
                                                  variable=self.show_password_var, command=self.toggle_password_visibility)
        self.show_password_check.pack(side=tk.LEFT, padx=(8, 0))
        
        # Initially hide password fields
        self.password_entry.config(state='disabled')
        self.show_password_check.config(state='disabled')
        
        ssh_frame.columnconfigure(1, weight=1)
        
        # Target Directory Settings
        target_frame = ttk.LabelFrame(main_frame, text="Target Directory Settings", padding="15")
        target_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(target_frame, text="Default Target Directory:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.target_dir_var = tk.StringVar(value="/home/pi/uploads")
        ttk.Entry(target_frame, textvariable=self.target_dir_var, width=45).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(15, 0))
        target_frame.columnconfigure(1, weight=1)
        
        # Test Connection
        test_frame = ttk.LabelFrame(main_frame, text="Connection Test", padding="15")
        test_frame.pack(fill=tk.X, pady=(0, 15))
        
        test_button_frame = ttk.Frame(test_frame)
        test_button_frame.pack(fill=tk.X)
        
        ttk.Button(test_button_frame, text="Test Connection", command=self.test_connection).pack(side=tk.LEFT)
        self.test_status_var = tk.StringVar()
        status_label = ttk.Label(test_button_frame, textvariable=self.test_status_var, foreground="blue")
        status_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Installation Section
        install_frame = ttk.LabelFrame(main_frame, text="Send To Menu Installation", padding="15")
        install_frame.pack(fill=tk.X, pady=(0, 15))
        
        install_button_frame = ttk.Frame(install_frame)
        install_button_frame.pack(fill=tk.X)
        
        ttk.Button(install_button_frame, text="Install Send To Menu", command=self.install_sendto_menu).pack(side=tk.LEFT)
        ttk.Button(install_button_frame, text="Uninstall Send To Menu", command=self.uninstall_sendto_menu).pack(side=tk.LEFT, padx=(15, 0))
        
        # SAVE BUTTONS - Make them very prominent
        button_frame = ttk.LabelFrame(main_frame, text="💾 SAVE SETTINGS", padding="20")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        button_container = ttk.Frame(button_frame)
        button_container.pack(fill=tk.X)
        
        # Make save button prominent
        save_button = ttk.Button(button_container, text="💾 Save Settings", command=self.save_config)
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        save_button.configure(style="Accent.TButton")  # Try to make it stand out
        
        ttk.Button(button_container, text="Save & Exit", command=self.save_and_exit).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_container, text="Exit", command=self.root.quit).pack(side=tk.LEFT)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Auto-save on any change
        self.ip_var.trace('w', self.auto_save)
        self.username_var.trace('w', self.auto_save)
        self.port_var.trace('w', self.auto_save)
        self.auth_var.trace('w', self.auto_save)
        self.key_path_var.trace('w', self.auto_save)
        self.target_dir_var.trace('w', self.auto_save)
        self.save_password_var.trace('w', self.auto_save)
        self.password_var.trace('w', self.auto_save)
        
    def _get_encryption_key(self):
        """Generate a machine-specific encryption key"""
        try:
            # Use machine-specific information to generate key
            import platform
            machine_info = f"{platform.node()}-{platform.machine()}-{platform.processor()}"
            key = hashlib.sha256(machine_info.encode()).digest()
            return base64.urlsafe_b64encode(key)
        except:
            # Fallback key if platform info fails
            fallback = "RaspFileSend-Default-Key-2024"
            key = hashlib.sha256(fallback.encode()).digest()
            return base64.urlsafe_b64encode(key)
    
    def _encrypt_password(self, password):
        """Encrypt password using machine-specific key"""
        if not password:
            return ""
        
        try:
            from cryptography.fernet import Fernet
            key = self._get_encryption_key()
            fernet = Fernet(key)
            encrypted = fernet.encrypt(password.encode())
            return base64.b64encode(encrypted).decode()
        except ImportError:
            # Fallback to base64 if cryptography not available
            messagebox.showwarning("Security Warning", 
                                 "Cryptography library not found. Password will be stored with basic encoding only.\n\n"
                                 "For better security, install with: pip install cryptography")
            return base64.b64encode(password.encode()).decode()
        except Exception as e:
            messagebox.showerror("Encryption Error", f"Failed to encrypt password: {e}")
            return ""
    
    def _decrypt_password(self, encrypted_password):
        """Decrypt password using machine-specific key"""
        if not encrypted_password:
            return ""
        
        try:
            from cryptography.fernet import Fernet
            key = self._get_encryption_key()
            fernet = Fernet(key)
            encrypted_bytes = base64.b64decode(encrypted_password.encode())
            decrypted = fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except ImportError:
            # Fallback from base64
            try:
                return base64.b64decode(encrypted_password.encode()).decode()
            except:
                return ""
        except Exception:
            # If decryption fails, return empty (password changed or corrupted)
            return ""
    
    def on_save_password_changed(self):
        """Handle save password checkbox change"""
        if self.save_password_var.get():
            # Enable password fields
            self.password_entry.config(state='normal')
            self.show_password_check.config(state='normal')
            # Show warning about password storage
            response = messagebox.askyesno("Password Storage", 
                                         "Do you want to save your password?\n\n"
                                         "• Password will be encrypted and stored locally\n"
                                         "• Only works on this computer\n"
                                         "• More convenient but less secure than SSH keys\n\n"
                                         "Continue?", parent=self.root)
            if not response:
                self.save_password_var.set(False)
                self.password_entry.config(state='disabled')
                self.show_password_check.config(state='disabled')
        else:
            # Disable password fields and clear password
            self.password_var.set("")
            self.password_entry.config(state='disabled')
            self.show_password_check.config(state='disabled')
            self.show_password_var.set(False)
            self.password_entry.config(show="*")
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")
    
    def browse_key_file(self):
        filename = filedialog.askopenfilename(
            title="Select SSH Private Key",
            filetypes=[("All files", "*.*"), ("PEM files", "*.pem"), ("Key files", "*.key")]
        )
        if filename:
            self.key_path_var.set(filename)
    
    def load_config(self):
        if self.config_file.exists():
            self.config.read(self.config_file)
        else:
            # Create default configuration
            self.config['SSH'] = {
                'ip': '',
                'username': 'pi',
                'port': '22',
                'auth_method': 'password',
                'key_path': '',
                'save_password': 'false',
                'encrypted_password': ''
            }
            self.config['TARGET'] = {
                'default_directory': '/home/pi/uploads'
            }
    
    def load_saved_settings(self):
        try:
            self.ip_var.set(self.config.get('SSH', 'ip', fallback=''))
            self.username_var.set(self.config.get('SSH', 'username', fallback='pi'))
            self.port_var.set(self.config.get('SSH', 'port', fallback='22'))
            self.auth_var.set(self.config.get('SSH', 'auth_method', fallback='password'))
            self.key_path_var.set(self.config.get('SSH', 'key_path', fallback=''))
            self.target_dir_var.set(self.config.get('TARGET', 'default_directory', fallback='/home/pi/uploads'))
            
            # Load password settings
            save_password = self.config.get('SSH', 'save_password', fallback='false').lower() == 'true'
            self.save_password_var.set(save_password)
            
            if save_password:
                # Enable password fields
                self.password_entry.config(state='normal')
                self.show_password_check.config(state='normal')
                # Load and decrypt password
                encrypted_password = self.config.get('SSH', 'encrypted_password', fallback='')
                if encrypted_password:
                    decrypted_password = self._decrypt_password(encrypted_password)
                    self.password_var.set(decrypted_password)
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def auto_save(self, *args):
        """Auto-save configuration when any field changes"""
        try:
            if hasattr(self, 'config'):  # Only save if config is initialized
                self.save_config_silent()
        except Exception as e:
            pass  # Ignore errors during auto-save
    
    def save_config_silent(self):
        """Save configuration without showing success message"""
        try:
            if not self.config.has_section('SSH'):
                self.config.add_section('SSH')
            if not self.config.has_section('TARGET'):
                self.config.add_section('TARGET')
                
            self.config['SSH']['ip'] = self.ip_var.get()
            self.config['SSH']['username'] = self.username_var.get()
            self.config['SSH']['port'] = self.port_var.get()
            self.config['SSH']['auth_method'] = self.auth_var.get()
            self.config['SSH']['key_path'] = self.key_path_var.get()
            self.config['SSH']['save_password'] = str(self.save_password_var.get()).lower()
            self.config['TARGET']['default_directory'] = self.target_dir_var.get()
            
            # Handle password saving
            if self.save_password_var.get() and self.password_var.get():
                encrypted_password = self._encrypt_password(self.password_var.get())
                self.config['SSH']['encrypted_password'] = encrypted_password
            else:
                # Remove password if not saving or empty
                if self.config.has_option('SSH', 'encrypted_password'):
                    self.config.remove_option('SSH', 'encrypted_password')
            
            # Ensure the directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            
            return True
        except Exception as e:
            return False
            
            return True
        except Exception as e:
            return False
    
    def save_and_exit(self):
        """Save settings and exit application"""
        if self.save_config():
            self.root.quit()
    
    def save_config(self):
        try:
            if not self.config.has_section('SSH'):
                self.config.add_section('SSH')
            if not self.config.has_section('TARGET'):
                self.config.add_section('TARGET')
                
            self.config['SSH']['ip'] = self.ip_var.get()
            self.config['SSH']['username'] = self.username_var.get()
            self.config['SSH']['port'] = self.port_var.get()
            self.config['SSH']['auth_method'] = self.auth_var.get()
            self.config['SSH']['key_path'] = self.key_path_var.get()
            self.config['SSH']['save_password'] = str(self.save_password_var.get()).lower()
            self.config['TARGET']['default_directory'] = self.target_dir_var.get()
            
            # Handle password saving
            if self.save_password_var.get() and self.password_var.get():
                encrypted_password = self._encrypt_password(self.password_var.get())
                self.config['SSH']['encrypted_password'] = encrypted_password
            else:
                # Remove password if not saving or empty
                if self.config.has_option('SSH', 'encrypted_password'):
                    self.config.remove_option('SSH', 'encrypted_password')
            
            # Ensure the directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            print(f"Configuration saved to: {self.config_file}")  # Debug output
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            return False
            
            with open(self.config_file, 'w') as f:
                self.config.write(f)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            print(f"Configuration saved to: {self.config_file}")  # Debug output
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            return False
    
    def test_connection(self):
        try:
            self.test_status_var.set("Testing...")
            self.root.update()
            
            # Validate inputs first
            if not self.ip_var.get().strip():
                self.test_status_var.set("✗ Please enter Raspberry Pi IP")
                return
            
            if not self.username_var.get().strip():
                self.test_status_var.set("✗ Please enter username")
                return
            
            # Import here to avoid issues if paramiko is not installed
            try:
                import paramiko
            except ImportError:
                self.test_status_var.set("✗ paramiko not installed. Run: pip install paramiko")
                return
            
            # Get password if needed (on main thread)
            password = None
            if self.auth_var.get() == "password":
                # Check if we have a saved password
                if self.save_password_var.get() and self.password_var.get():
                    password = self.password_var.get()
                else:
                    password = simpledialog.askstring("Password", "Enter SSH password:", show='*', parent=self.root)
                    if not password:
                        self.test_status_var.set("Test cancelled")
                        return
            
            # Run connection test in background thread
            def test():
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    
                    if self.auth_var.get() == "password":
                        ssh.connect(
                            hostname=self.ip_var.get().strip(),
                            username=self.username_var.get().strip(),
                            password=password,
                            port=int(self.port_var.get()),
                            timeout=10
                        )
                    else:
                        if not self.key_path_var.get().strip():
                            self.root.after(0, lambda: self.test_status_var.set("✗ Please specify SSH key path"))
                            return
                        ssh.connect(
                            hostname=self.ip_var.get().strip(),
                            username=self.username_var.get().strip(),
                            key_filename=self.key_path_var.get().strip(),
                            port=int(self.port_var.get()),
                            timeout=10
                        )
                    
                    # Test if target directory exists, create if not
                    stdin, stdout, stderr = ssh.exec_command(f"mkdir -p {self.target_dir_var.get()}")
                    ssh.close()
                    
                    # Update UI on main thread
                    self.root.after(0, lambda: self.test_status_var.set("✓ Connection successful!"))
                    
                except Exception as e:
                    error_msg = str(e)
                    if "Authentication failed" in error_msg:
                        error_msg = "Authentication failed - check credentials"
                    elif "Connection refused" in error_msg:
                        error_msg = "Connection refused - check IP and SSH service"
                    elif "timeout" in error_msg.lower():
                        error_msg = "Connection timeout - check IP and network"
                    else:
                        error_msg = f"Connection failed: {error_msg[:50]}..."
                    
                    # Update UI on main thread
                    self.root.after(0, lambda: self.test_status_var.set(f"✗ {error_msg}"))
            
            threading.Thread(target=test, daemon=True).start()
            
        except ValueError:
            self.test_status_var.set("✗ Invalid port number")
        except Exception as e:
            self.test_status_var.set(f"✗ Error: {str(e)[:50]}...")
    
    def install_sendto_menu(self):
        try:
            # Get the path to the current script directory
            script_dir = Path(__file__).parent.absolute()
            
            # Create the batch file that will be called from Send To menu
            sendto_batch = script_dir / "raspfilesend_sendto.bat"
            python_script = script_dir / "raspfilesend_transfer.py"
            
            batch_content = f'''@echo off
cd /d "{script_dir}"
python "{python_script}" %*
if errorlevel 1 (
    echo.
    echo Error occurred. Please check the configuration.
    timeout /t 5
)
pause
'''
            
            with open(sendto_batch, 'w') as f:
                f.write(batch_content)
            
            # Get the Windows Send To folder
            sendto_folder = Path(os.path.expandvars(r"%APPDATA%\Microsoft\Windows\SendTo"))
            sendto_link = sendto_folder / "Send to Raspberry Pi.bat"
            
            # Copy the batch file to Send To folder
            import shutil
            shutil.copy2(sendto_batch, sendto_link)
            
            messagebox.showinfo("Success", f"Send To menu installed successfully!\n\nYou can now right-click on files and select\n'Send to' → 'Send to Raspberry Pi'")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install Send To menu: {e}")
    
    def uninstall_sendto_menu(self):
        try:
            sendto_folder = Path(os.path.expandvars(r"%APPDATA%\Microsoft\Windows\SendTo"))
            sendto_link = sendto_folder / "Send to Raspberry Pi.bat"
            
            if sendto_link.exists():
                sendto_link.unlink()
                messagebox.showinfo("Success", "Send To menu uninstalled successfully!")
            else:
                messagebox.showwarning("Warning", "Send To menu entry not found.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to uninstall Send To menu: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = RaspFileSendConfig()
    app.run()
