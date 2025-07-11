📄 README.md
md
Copy
Edit
# 🔗 LAN Sharing Tool

A lightweight and easy-to-use Python-based tool to **send and receive files over a Local Area Network (LAN)**. The project consists of a server-side app and a client-side app (which can be compiled into an `.exe` for easy sharing).

---

## 🚀 Features

- 📤 Send files to any connected client over LAN
- 📥 Receive files from clients without internet
- 🖥️ Minimal terminal interface
- 📦 Client can be bundled as a portable `.exe` file (via PyInstaller)
- 🔒 Secure file handling with confirmation messages
- 💡 Easy to set up and use on any Windows machine

---

## 🧠 How It Works

The server listens on a specific port for incoming file transfer requests. The client connects to the server using the server's IP address and sends the selected file. The server receives and stores the file in the defined folder.

---

## 🛠️ Requirements

- Python 3.8 or higher
- For `.exe` build: [PyInstaller](https://pyinstaller.org/)

---

## 📂 Folder Structure

LAN-Sharing-Project/
├── client/
│ ├── lanClient.py
│ └── shared/
├── server/
│ └── server.py
├── .gitignore
├── README.md

yaml
Copy
Edit

---

## ⚙️ How to Use

### ✅ Server (Receiver)

1. Navigate to the `server` folder:
   ```bash
   cd server
Run the server script:

bash
Copy
Edit
python server.py
The server will listen for connections and show file receive progress.

✅ Client (Sender)
Option 1: Run from Python (for testing)
Navigate to the client folder:
cd client

Run:
python server.py

Option 2: Build .exe file (for easy use)
Install PyInstaller:
pip install pyinstaller

Build the .exe:
pyinstaller --onefile --noconsole --add-data "shared;shared" lanClient.py --name client
Share dist/client.exe with others on the same LAN.

🧪 Example Use Case
Start the server on your PC (Receiver).

Share your IP address with someone on the same Wi-Fi.

They run the client and send files to your machine.

💻 Commands Summary
Shutdown Windows (bonus):
shutdown /s /f /t 0

Popup Message (Windows):
powershell -Command "Add-Type -AssemblyName PresentationFramework; [System.Windows.MessageBox]::Show('Hello from LAN Sharing Tool!','Popup')"

🙋‍♂️ Author
Divyansh Gupta
Contact: LinkedIn | Portfolio | GitHub

📃 License
This project is licensed under the MIT License.

🌐 Disclaimer
This tool is intended for educational and personal use only. Make sure all users are aware of file transfers on your network.