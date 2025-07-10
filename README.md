This Works its not 100% but it works great for sending files to raspberry pi when you need to send several files many times.
#. RaspFileSend

A Windows application that allows you to easily send files to a Raspberry Pi over SSH using the right-click "Send to" context menu.

## Features

- **Easy Setup**: Configure your Raspberry Pi connection settings through a user-friendly GUI
- **Send To Integration**: Right-click on any file(s) and select "Send to Raspberry Pi" from the context menu
- **Multiple Authentication Methods**: Support for both password and SSH key authentication
- **Persistent Target Directory**: The target directory is remembered and can be easily changed
- **Multiple File Support**: Send multiple files at once
- **Progress Tracking**: Real-time transfer progress and status updates
- **File Overwrite Protection**: Prompts before overwriting existing files

## Installation

1. **Clone or download this repository**
   ```powershell
   git clone https://github.com/yourusername/RaspFileSend.git
   cd RaspFileSend
   ```

2. **Install Python dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the configuration tool**
   ```powershell
   python raspfilesend_config.py
   ```

4. **Configure your Raspberry Pi connection**:
   - Enter your Raspberry Pi's IP address
   - Set the username (default: pi)
   - Choose authentication method (password or SSH key)
   - Set the default target directory on your Pi
   - Test the connection to ensure everything works

5. **Install the Send To menu integration**:
   - Click "Install Send To Menu" in the configuration tool
   - This will add "Send to Raspberry Pi" to your Windows right-click context menu

## Usage

### First Time Setup
1. Run `python raspfilesend_config.py`
2. Fill in your Raspberry Pi connection details
3. Test the connection
4. Click "Install Send To Menu"
5. Save your settings

### Sending Files
1. Right-click on any file or group of files in Windows Explorer
2. Select "Send to" → "Send to Raspberry Pi"
3. A window will open showing the files to be transferred
4. Verify or change the target directory if needed
5. Click "Send Files"
6. Enter your password if prompted (for password authentication)
7. Monitor the transfer progress

### Changing Settings
- Run `python raspfilesend_config.py` again to modify connection settings
- The target directory can be changed during file transfer or in the configuration

## Configuration

The application stores its configuration in `%USERPROFILE%\.raspfilesend_config.ini`. This includes:

- SSH connection details (IP, username, port)
- Authentication method and key path
- Default target directory

## Requirements

- Windows 10/11
- Python 3.7+
- Required Python packages (installed via requirements.txt):
  - paramiko (for SSH/SFTP)
  - tkinter (usually included with Python)
  - configparser (usually included with Python)
  - pathlib (usually included with Python)

## Security Notes

- Passwords are not stored - you'll be prompted each time for password authentication
- SSH keys are recommended for better security and convenience
- The application uses paramiko with AutoAddPolicy for host key verification

## Troubleshooting

### "paramiko not found" error
```powershell
pip install paramiko
```

### Connection timeout or refused
- Verify your Raspberry Pi's IP address
- Ensure SSH is enabled on your Raspberry Pi: `sudo systemctl enable ssh`
- Check firewall settings
- Verify the username and authentication method

### Permission denied errors
- Ensure the target directory exists and is writable by your user
- Check file permissions on the Raspberry Pi

### Send To menu not appearing
- Run the configuration tool as administrator and try installing again
- Manually check if the file exists in `%APPDATA%\Microsoft\Windows\SendTo\`

## Uninstalling

1. Run `python raspfilesend_config.py`
2. Click "Uninstall Send To Menu"
3. Delete the application folder
4. Optionally remove `%USERPROFILE%\.raspfilesend_config.ini`

## File Structure

```
RaspFileSend/
├── raspfilesend_config.py      # Configuration GUI application
├── raspfilesend_transfer.py    # File transfer application
├── raspfilesend_sendto.bat    # Batch file for Send To menu
├── requirements.txt           # Python dependencies
├── README.md                 # This file
└── sendtoinfo.txt           # Additional notes
```

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

## License

This project is open source and available under the MIT License.
