# Quick Start Guide

## 1. Setup (One-time only)

**Run the setup script:**
```
setup.bat
```

This will:
- Check if Python is installed
- Install required packages
- Open the configuration tool

**Or manually:**
```powershell
pip install -r requirements.txt
python raspfilesend_config.py
```

## 2. Configure Your Raspberry Pi Connection

In the configuration window:

1. **SSH Connection Settings:**
   - Enter your Raspberry Pi's IP address
   - Set username (usually 'pi')
   - Choose port (usually 22)
   - Select authentication method:
     - **Password**: You'll be prompted each time
     - **SSH Key**: Browse to your private key file

2. **Target Directory:**
   - Set where files should be uploaded (e.g., `/home/pi/uploads`)
   - This directory will be created automatically if it doesn't exist

3. **Test Connection:**
   - Click "Test Connection" to verify settings
   - Enter password if prompted

4. **Install Send To Menu:**
   - Click "Install Send To Menu"
   - This adds the option to your Windows right-click menu

5. **Save Settings:**
   - Click "Save Settings" to store your configuration

## 3. Using the Application

**To send files:**
1. Right-click on any file(s) in Windows Explorer
2. Select "Send to" → "Send to Raspberry Pi"
3. Review the files and target directory
4. Click "Send Files"
5. Enter password if prompted
6. Monitor transfer progress
7. **If files exist:** Choose from these options:
   - **Yes**: Overwrite this file only
   - **No**: Skip this file only  
   - **Yes to All**: Overwrite this and all remaining files without asking
   - **No to All**: Skip this and all remaining files without asking
   - **Cancel**: Stop the entire transfer

**To change target directory:**
- Click "Change" button during transfer, or
- Re-run the configuration tool

## 4. SSH Key Setup (Recommended)

For password-free transfers, set up SSH keys:

**On Windows:**
```powershell
# Generate key pair (if you don't have one)
ssh-keygen -t rsa -b 4096

# Copy public key to Raspberry Pi
type %USERPROFILE%\.ssh\id_rsa.pub | ssh pi@YOUR_PI_IP "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**In the configuration:**
- Select "SSH Key" authentication
- Browse to your private key (usually `%USERPROFILE%\.ssh\id_rsa`)

## 5. Troubleshooting

**Common Issues:**

- **"paramiko not found"**: Run `pip install paramiko`
- **Connection refused**: Enable SSH on Pi with `sudo systemctl enable ssh`
- **Permission denied**: Check target directory permissions
- **Send To menu missing**: Run config tool as administrator

**Enable SSH on Raspberry Pi:**
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

**Create upload directory:**
```bash
mkdir -p /home/pi/uploads
chmod 755 /home/pi/uploads
```

## 6. Features

- ✅ Multiple file support
- ✅ Persistent target directory
- ✅ Password and SSH key authentication
- ✅ Progress monitoring
- ✅ File overwrite protection with bulk options (Yes to All, No to All)
- ✅ Native Windows integration
- ✅ Automatic directory creation
- ✅ Secure password storage (optional)
- ✅ Auto-closing terminal when GUI is closed

---

**Need help?** Check the full README.md for detailed information.
