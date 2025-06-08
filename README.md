# 📡 Discord Webhook Sender (Text & File)

A simple Python tool to send messages or files to a Discord webhook.

---

## 📸 Preview

Easily send text or upload files directly to your Discord channel via webhook.

---

## ⚙️ Features

- ✅ **Send text messages** to a Discord webhook
- 📁 **Upload and send files** (any type)
- 💡 **Simple terminal interface** for quick usage
- 🔒 **Secure**: Your webhook URL is not stored
- 📝 **Customizable**: Edit the script to fit your needs
- 🖥️ **Cross-platform**: Works on Windows, macOS, and Linux

---

## 🧪 Installation

Make sure you have **Python 3.8+** installed.

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/webhook-sender.git
cd webhook-sender
pip install -r requirements.txt  # If needed
```

---
## 🤑 Or just use this code

```bash
pip install -r requirements.txt  # If needed

import requests
import tkinter as tk
from tkinter import filedialog

# Hide the root Tkinter window
root = tk.Tk()
root.withdraw()

webhook_url = input("Enter webhook URL: ")

input_type = input("Select send type (1: Message, 2: File): ")

if input_type == "1":
    while True:
        message = input("Enter message to send (or type 'exit' to quit): ")
        if message.lower() == "exit":
            break

        data = {
            "content": message
        }

        response = requests.post(webhook_url, json=data)

        if response.status_code == 204:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {response.status_code}")

elif input_type == "2":
    while True:
        print("Select an image or file to send (press Cancel to exit)...")
        file_path = filedialog.askopenfilename()

        if not file_path:
            print("Goodbye!")
            break

        try:
            with open(file_path, 'rb') as f:
                files = {
                    "file": f
                }
                response = requests.post(webhook_url, files=files)

            if response.status_code in [200, 204]:
                print("File sent successfully!")
            else:
                print(f"Failed to send file: {response.status_code}")
        except Exception as e:
            print(f"Could not open file: {e}")

```

---

## ▶️ Usage

Run the script from your terminal:

```bash
python webhook_sender.py
```

Then follow the prompts:

1. **Paste your webhook URL**
2. **Choose to send text or file**
3. **Done!** ✅

---

## 🛠 Requirements

- **Python 3.8+**
- **requests** (install with `pip install requests`)

---

## 💬 Support

For issues or feature requests, open an issue on [GitHub](https://github.com/yourusername/webhook-sender/issues), Def no issue here lol.

---

## 📄 License

No License lol – do whatever, just don't be evil 😎
