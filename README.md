# Gauth Manager
![image](https://github.com/user-attachments/assets/d6d4c60f-35a1-420a-8075-786a219608d2)

This program simplifies the task of using Gauth Math to screenshot questions by opening a new Incognito tab if the user runs into a paywall. It is a solid alternative to using Gauth on your phone.

# Setup
> [!IMPORTANT]
> This will only work for Windows devices because of the nature of this program. (This will likely not change in the future, sorry!)
## Option 1 - Quick `.exe` file
- Go to the Releases page and download the latest `.exe` file. Then simply run it.
###### (It goes without me saying that you can check for yourself that this is not malware. The Python code is built into an exe with [PyInstaller](https://pypi.org/project/pyinstaller/) and with `--onefile --noconsole --windowed` flags. Test it for yourself.)
## Option 2 - Python file
- Go to the Releases page and download the latest `.py` file.
- In your command line of choice, run `pip install pygetwindow pyautogui Pillow pywin32`.
- Run the python file.

# Why not just clear your cookies?
From my testing, it is very hard to reliably go through every possible browser's setting page without knowing other factors like screen resolution and pre-prepared cookie clear settings. It is much more consistent to use purely keyboard-based inputs without much dependance on browser.
