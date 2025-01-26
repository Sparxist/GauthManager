# Gauth Manager
![image](https://github.com/user-attachments/assets/03f3643b-87bf-46cd-83ef-0626ed3e68da)

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
