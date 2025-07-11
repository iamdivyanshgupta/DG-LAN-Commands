import os
import shutil
import subprocess
import sys
import time

APPDATA = os.getenv("APPDATA")
CLIENT_FOLDER = os.path.join(APPDATA, "SystemMonitor")
STARTUP_FOLDER = os.path.join(APPDATA, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
STARTUP_SCRIPT = os.path.join(STARTUP_FOLDER, "SystemMonitor.bat")

def kill_client():
    try:
        subprocess.call("taskkill /f /im client.exe", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ client.exe killed.")
    except Exception as e:
        print(f"❌ Couldn't kill client.exe: {e}")

def delete_folder():
    if os.path.exists(CLIENT_FOLDER):
        try:
            shutil.rmtree(CLIENT_FOLDER)
            print(f"✅ Deleted {CLIENT_FOLDER}")
        except Exception as e:
            print(f"❌ Failed to delete {CLIENT_FOLDER}: {e}")
    else:
        print("ℹ️  No client folder found.")

def delete_startup():
    if os.path.exists(STARTUP_SCRIPT):
        try:
            os.remove(STARTUP_SCRIPT)
            print("✅ Removed startup script.")
        except Exception as e:
            print(f"❌ Failed to remove startup script: {e}")
    else:
        print("ℹ️  No startup script found.")

def self_delete():
    # Write a batch file to delete this .exe after 3 seconds
    bat_path = os.path.join(os.getcwd(), "remove_self.bat")
    with open(bat_path, "w") as f:
        f.write(f"""
@echo off
timeout /t 3 > nul
del "{sys.argv[0]}"
del "%~f0"
""")
    os.startfile(bat_path)

if __name__ == "__main__":
    print("🔧 Uninstalling Remote Client...")
    kill_client()
    time.sleep(1)
    delete_folder()
    delete_startup()
    print("✅ Uninstallation complete.")
    self_delete()
