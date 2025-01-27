# 🌟 Gauth Manager 🌟
![image](https://github.com/user-attachments/assets/8f580b59-ae20-451e-9753-35512d79bc3a)

This program simplifies the task of using Gauth Math to screenshot questions by opening a new Incognito tab if the user runs into a paywall. It is a solid alternative to using Gauth on your phone.

# ⭐ Features ⭐
- Customizable color scheme and parameters
- Automated Gauth Screenshot Transfer
- Browser and Resolution Independant
- Fast and Reliable
  
# Setup
> [!IMPORTANT]
> This will only work for Windows devices because of the nature of this program. (This will likely not change in the future, sorry!)
## Option 1 - Quick `.exe` file
- Go to the Releases page and download the latest `.exe` file. Then simply run it.
###### (It goes without me saying that you can check for yourself that this is not malware. The Python code is built into an exe with [PyInstaller](https://pypi.org/project/pyinstaller/) and with `--onefile --noconsole --windowed` flags. Test it for yourself.)
## Option 2 - Python file
1. Go to the Releases page and download the latest `.py` file.
2. In your command line of choice, run `pip install pygetwindow pyautogui Pillow pywin32`.
3. Run the python file.

> [!NOTE]
> Make sure that the "Incognito Window" and "Gauth Window" strings are not contained in any other program, else if you press `Restart Gauth` it will close out those programs.

## Why not just clear your cookies?
From my testing, it is very hard to reliably go through every possible browser's setting page without knowing other factors like screen resolution and pre-prepared cookie clear settings. It is much more consistent to use purely keyboard-based inputs without much dependance on browser.
