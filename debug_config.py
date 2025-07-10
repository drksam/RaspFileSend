#!/usr/bin/env python3
"""
Debug script to check RaspFileSend configuration
"""

import configparser
from pathlib import Path
import os

def debug_config():
    print("🔍 RaspFileSend Configuration Debug")
    print("=" * 50)
    
    # Check config file location
    config_file = Path.home() / ".raspfilesend_config.ini"
    print(f"📍 Config file path: {config_file}")
    print(f"🏠 Home directory: {Path.home()}")
    
    if config_file.exists():
        print("✅ Configuration file exists")
        print(f"📊 File size: {config_file.stat().st_size} bytes")
        
        # Read and display configuration
        config = configparser.ConfigParser()
        try:
            config.read(config_file)
            print("\n📋 Configuration contents:")
            print("-" * 30)
            
            for section in config.sections():
                print(f"\n[{section}]")
                for key, value in config.items(section):
                    # Mask password-like values
                    if 'password' in key.lower() or 'key' in key.lower():
                        display_value = "*" * len(value) if value else "(empty)"
                    else:
                        display_value = value if value else "(empty)"
                    print(f"  {key} = {display_value}")
            
            # Check required fields
            print("\n🔍 Required fields check:")
            print("-" * 30)
            
            required_checks = [
                ('SSH', 'ip', 'IP Address'),
                ('SSH', 'username', 'Username'),
                ('SSH', 'port', 'Port'),
                ('TARGET', 'default_directory', 'Target Directory')
            ]
            
            all_good = True
            for section, key, description in required_checks:
                try:
                    value = config.get(section, key)
                    if value.strip():
                        print(f"  ✅ {description}: {value}")
                    else:
                        print(f"  ❌ {description}: (empty)")
                        all_good = False
                except:
                    print(f"  ❌ {description}: (missing)")
                    all_good = False
            
            if all_good:
                print("\n🎉 All required configuration fields are present!")
            else:
                print("\n⚠️  Some required fields are missing or empty.")
                
        except Exception as e:
            print(f"❌ Error reading configuration: {e}")
            
    else:
        print("❌ Configuration file does not exist")
        print("\n💡 To create configuration:")
        print("   1. Run: python raspfilesend_config.py")
        print("   2. Fill in your settings")
        print("   3. Click 'Save Settings'")
    
    print("\n" + "=" * 50)
    input("Press Enter to exit...")

if __name__ == "__main__":
    debug_config()
