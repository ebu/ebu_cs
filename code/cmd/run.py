#!/usr/bin/env python3
"""
Launcher for the XML Classification Scheme Viewer (Tkinter GUI).
"""

import os
import subprocess
import sys

# === Configuration ===
APP_FILE = "app.py"
CS_DIR = "../../metadata/cs"  # Change this to your XML folder if needed

def check_requirements():
    try:
        import tkinter
    except ImportError:
        print("❌ tkinter is not installed.")
        print("💡 On macOS, use: brew install python-tk")
        print("💡 On Ubuntu/Debian: sudo apt install python3-tk")
        sys.exit(1)

def check_cs_directory():
    if not os.path.exists(CS_DIR):
        print(f"⚠️ The folder `{CS_DIR}/` was not found.")
        print("Creating it now. Add your XML files into this folder.")
        os.makedirs(CS_DIR, exist_ok=True)

def run_app():
    print(f"🚀 Launching the XML Viewer...")
    subprocess.run([sys.executable, APP_FILE, CS_DIR])

if __name__ == "__main__":
    print("🔧 Checking environment...")
    check_requirements()
    check_cs_directory()
    run_app()
