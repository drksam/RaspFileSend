#!/usr/bin/env python3
"""
Simple SSH connection test script for RaspFileSend
This helps debug connection issues without the GUI complexity
"""

import sys
import configparser
from pathlib import Path

def test_ssh_connection():
    # Load configuration
    config_file = Path.home() / ".raspfilesend_config.ini"
    if not config_file.exists():
        print("❌ Configuration file not found. Please run raspfilesend_config.py first.")
        return False
    
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # Get connection details
    ip = config.get('SSH', 'ip', fallback='')
    username = config.get('SSH', 'username', fallback='')
    port = config.get('SSH', 'port', fallback='22')
    auth_method = config.get('SSH', 'auth_method', fallback='password')
    key_path = config.get('SSH', 'key_path', fallback='')
    
    print(f"🔧 Testing connection to {username}@{ip}:{port}")
    print(f"🔐 Authentication method: {auth_method}")
    
    if not ip or not username:
        print("❌ IP address or username not configured")
        return False
    
    try:
        import paramiko
        print("✅ paramiko library found")
    except ImportError:
        print("❌ paramiko library not found. Install with: pip install paramiko")
        return False
    
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print("🔌 Attempting to connect...")
        
        if auth_method == "password":
            import getpass
            password = getpass.getpass(f"Enter password for {username}@{ip}: ")
            ssh.connect(
                hostname=ip,
                username=username,
                password=password,
                port=int(port),
                timeout=15
            )
        else:
            if not key_path:
                print("❌ SSH key path not specified")
                return False
            if not Path(key_path).exists():
                print(f"❌ SSH key file not found: {key_path}")
                return False
            
            ssh.connect(
                hostname=ip,
                username=username,
                key_filename=key_path,
                port=int(port),
                timeout=15
            )
        
        print("✅ SSH connection successful!")
        
        # Test command execution
        print("🧪 Testing command execution...")
        stdin, stdout, stderr = ssh.exec_command("echo 'Hello from RaspFileSend!'")
        output = stdout.read().decode().strip()
        print(f"📤 Command output: {output}")
        
        # Test target directory
        target_dir = config.get('TARGET', 'default_directory', fallback='/home/pi/uploads')
        print(f"📁 Testing target directory: {target_dir}")
        stdin, stdout, stderr = ssh.exec_command(f"mkdir -p {target_dir} && ls -ld {target_dir}")
        output = stdout.read().decode().strip()
        if output:
            print(f"✅ Target directory accessible: {output}")
        else:
            error = stderr.read().decode().strip()
            print(f"⚠️  Target directory warning: {error}")
        
        ssh.close()
        print("🎉 All tests passed! Your RaspFileSend should work correctly.")
        return True
        
    except paramiko.AuthenticationException:
        print("❌ Authentication failed - check your username/password or SSH key")
        return False
    except paramiko.SSHException as e:
        print(f"❌ SSH connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 RaspFileSend Connection Test")
    print("=" * 40)
    
    success = test_ssh_connection()
    
    print("\n" + "=" * 40)
    if success:
        print("🎯 Test completed successfully!")
    else:
        print("💥 Test failed. Please check the errors above.")
        
    input("\nPress Enter to exit...")
