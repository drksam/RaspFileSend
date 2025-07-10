#!/usr/bin/env python3
"""
Test script for password encryption/decryption functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from raspfilesend_config import RaspFileSendConfig

def test_password_encryption():
    print("🔐 Testing Password Encryption/Decryption")
    print("=" * 50)
    
    # Create a config instance (without GUI)
    config = RaspFileSendConfig.__new__(RaspFileSendConfig)
    
    # Test passwords
    test_passwords = [
        "simplepassword",
        "complex!P@ssw0rd#123",
        "with spaces and symbols !@#$%",
        "unicode_test_αβγδε",
        ""
    ]
    
    for i, original_password in enumerate(test_passwords, 1):
        print(f"\n🧪 Test {i}: {'(empty)' if not original_password else original_password[:10] + '...' if len(original_password) > 10 else original_password}")
        
        try:
            # Encrypt the password
            encrypted = config._encrypt_password(original_password)
            print(f"   🔒 Encrypted: {encrypted[:20]}...{encrypted[-10:] if len(encrypted) > 30 else encrypted}")
            
            # Decrypt the password
            decrypted = config._decrypt_password(encrypted)
            print(f"   🔓 Decrypted: {'(empty)' if not decrypted else decrypted}")
            
            # Verify they match
            if original_password == decrypted:
                print("   ✅ PASS: Encryption/Decryption successful")
            else:
                print("   ❌ FAIL: Passwords don't match")
                print(f"      Original: '{original_password}'")
                print(f"      Decrypted: '{decrypted}'")
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Password encryption test completed!")

if __name__ == "__main__":
    test_password_encryption()
    input("\nPress Enter to exit...")
