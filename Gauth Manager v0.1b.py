import pygetwindow as gw
import pyautogui
from PIL import ImageGrab
import win32clipboard
import tkinter as tk
from tkinter import messagebox
import time
from io import BytesIO

def find_window(title):
    for window in gw.getWindowsWithTitle(title):
        return window
    return None

def show_error(message):
    messagebox.showerror("Error", message)

def focus_and_resize(window, x, y, width, height, delay):
    if window:
        window.activate()
        time.sleep(0.3 * delay)
        window.resizeTo(width, height)
        window.moveTo(x, y)

def copy_window_screenshot_to_clipboard(window, padding=(200, 50, 50, 50), delay=1, show=False):
    if not window:
        show_error("Screenshot window not found.")
        return

    left_pad, top_pad, right_pad, bottom_pad = padding
    time.sleep(0.1 * delay)
    screenshot = ImageGrab.grab(bbox=(
        window.left + left_pad, 
        window.top + top_pad, 
        window.left + window.width - right_pad, 
        window.top + window.height - bottom_pad
    ))

    if show:
        screenshot.show()
    else:
        output = BytesIO()
        screenshot.save(output, format="BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

def send_screenshot_to_window(screenshot_window, target_window, padding, delay, additional_steps=None):
    if not screenshot_window:
        show_error("Screenshot window not found.")
        return

    if not target_window:
        show_error("Gauth window not found.")
        return

    copy_window_screenshot_to_clipboard(screenshot_window, padding, delay)

    target_window.activate()
    time.sleep(0.1 * delay)
    if additional_steps: additional_steps()
    pyautogui.hotkey("ctrl", "v")

def initial_setup(sparx_title, delay):
    sparx_window = find_window(sparx_title)
    if sparx_window:
        screen_width, screen_height = pyautogui.size()
        focus_and_resize(sparx_window, 0, 0, screen_width // 2, screen_height, delay)
    else:
        show_error(f"Screenshot window not found.")

def new_incognito(incognito_title, delay):
    pyautogui.hotkey("ctrl", "shift", "n")
    time.sleep(0.1 * delay)
    incognito_window = find_window(incognito_title)
    if incognito_window:
        screen_width, screen_height = pyautogui.size()
        focus_and_resize(incognito_window, screen_width // 2, 0, screen_width // 2, screen_height, delay)
        pyautogui.typewrite("gauthmath.com\n")
        time.sleep(2 * delay)
    else:
        show_error(f"Incognito window not found.")

def send_gauth_fast(sparx_title, gauth_title, delay, padding):
    sparx_window = find_window(sparx_title)
    gauth_window = find_window(gauth_title)
    send_screenshot_to_window(sparx_window, gauth_window, padding, delay)

def send_gauth(sparx_title, gauth_title, delay, padding):
    sparx_window = find_window(sparx_title)
    gauth_window = find_window(gauth_title)
    send_screenshot_to_window(sparx_window, gauth_window, padding, delay, additional_steps=lambda: (
        pyautogui.hotkey("tab", "enter"),
        time.sleep(delay)
    ))

def send_gauth_force(sparx_title, gauth_title, delay, padding):
    sparx_window = find_window(sparx_title)
    gauth_window = find_window(gauth_title)
    send_screenshot_to_window(sparx_window, gauth_window, padding, delay, additional_steps=lambda: (
        pyautogui.hotkey("ctrl", "t"),
        time.sleep(0.1 * delay),
        pyautogui.hotkey("ctrl", "1"),
        pyautogui.hotkey("ctrl", "w"),
        pyautogui.typewrite("gauthmath.com\n"),
        time.sleep(1.5 * delay),
    ))

def del_gauth(incognito_title, gauth_title, delay):
    windows = gw.getAllWindows()
    gauth_windows = [win for win in windows if (incognito_title in win.title or gauth_title in win.title)]

    for win in gauth_windows:
        try:
            win.activate()
            time.sleep(0.5 * delay)
            pyautogui.hotkey('alt', 'f4')
        except Exception as e:
            show_error(f"Could not close window '{win.title}': {e}")

def restart(sparx_title, incognito_title, gauth_title, delay):
    del_gauth(incognito_title, gauth_title, delay)
    initial_setup(sparx_title, delay)
    new_incognito(incognito_title, delay)

def restart_and_send(sparx_title, incognito_title, gauth_title, delay, padding):
    restart(sparx_title, incognito_title, gauth_title, delay)
    time.sleep(delay)
    send_gauth_fast(sparx_title, gauth_title, delay, padding)

def create_gui():
    root = tk.Tk()
    root.title("G\u0430uth Manager v0.1b")  # \u0430 is Cyrillic A, avoids the program self-killing when restarting Gauth
    root.geometry("500x250")
    root.attributes("-topmost", True)
    root.configure(bg="#45008a")

    label_style = {"bg": "#45008a", "fg": "#FFFFFF"}
    entry_bg = "#200040"
    entry_fg = "#FFFFFF"

    padding_frame = tk.Frame(root, bg="#45008a")
    padding_frame.pack(side=tk.LEFT, padx=10, pady=10)

    tk.Label(padding_frame, text="Padding Top:", **label_style).pack(anchor="w")
    top_padding = tk.Entry(padding_frame, bg=entry_bg, fg=entry_fg, insertbackground="#FFFFFF", width=10)
    top_padding.pack(anchor="w")
    top_padding.insert(0, "200")

    tk.Label(padding_frame, text="Padding Left:", **label_style).pack(anchor="w")
    left_padding = tk.Entry(padding_frame, bg=entry_bg, fg=entry_fg, insertbackground="#FFFFFF", width=10)
    left_padding.pack(anchor="w")
    left_padding.insert(0, "50")

    tk.Label(padding_frame, text="Padding Bottom:", **label_style).pack(anchor="w")
    bottom_padding = tk.Entry(padding_frame, bg=entry_bg, fg=entry_fg, insertbackground="#FFFFFF", width=10)
    bottom_padding.pack(anchor="w")
    bottom_padding.insert(0, "50")

    tk.Label(padding_frame, text="Padding Right:", **label_style).pack(anchor="w")
    right_padding = tk.Entry(padding_frame, bg=entry_bg, fg=entry_fg, insertbackground="#FFFFFF", width=10)
    right_padding.pack(anchor="w")
    right_padding.insert(0, "50")

    tk.Label(padding_frame, text="Delay (s):", **label_style).pack(anchor="w")
    delay_entry = tk.Entry(padding_frame, bg=entry_bg, fg=entry_fg, insertbackground="#FFFFFF", width=10)
    delay_entry.pack(anchor="w")
    delay_entry.insert(0, "1")

    title_frame = tk.Frame(root, bg="#45008a")
    title_frame.pack(side=tk.LEFT, padx=10, pady=10)

    sparx_label = tk.Label(title_frame, text="Screenshot Window Title:", **label_style)
    sparx_label.pack(pady=2)
    sparx_entry = tk.Entry(title_frame, bg=entry_bg, fg=entry_fg, insertbackground="#FFFFFF", width=25)
    sparx_entry.pack(pady=2)
    sparx_entry.insert(0, "Sparx Maths")

    incognito_label = tk.Label(title_frame, text="Incognito Window Title:", **label_style)
    incognito_label.pack(pady=2)
    incognito_entry = tk.Entry(title_frame, bg=entry_bg, fg=entry_fg, insertbackground="#FFFFFF", width=25)
    incognito_entry.pack(pady=2)
    incognito_entry.insert(0, "Incognito")

    gauth_label = tk.Label(title_frame, text="Gauth Window Title:", **label_style)
    gauth_label.pack(pady=2)
    gauth_entry = tk.Entry(title_frame, bg=entry_bg, fg=entry_fg, insertbackground="#FFFFFF", width=25)
    gauth_entry.pack(pady=2)
    gauth_entry.insert(0, "Gauth")

    # Function to display help message
    def show_help():
        messagebox.showinfo(
            "Help (Gauth Manager v0.1b)", 
            "Inputs & Buttons:\n\n" +
            "  Padding:  Describes the area inside your screenshot window that will get chopped off.\n" +
            "  Delay:  Changes how fast the program will run (less delay might make the program miss inputs)\n" +
            "  Windows:  The titles of the windows you wish be detected and used. (Note that it looks for if the window contains the text.)\n\n" +
            "  Send Question:  Screenshots & copies the Screenshot Window and pastes it into the Gauth window\n" +
            "  Force Send Question:  Send Question, but it resets the tab (Useful if Send Question doesn't work properly)\n" +
            "  Restart and Send:  Restarts the Gauth session and does Send Question. Use this if you hit a paywall in Gauth.\n" +
            "  Restart Gauth:  Restarts the Gauth session without doing Send Question.\n" +
            "  View Screenshot:  Views the screenshot window with padding in place.\n\n" +
            "Setup:\n\n" +
            "  - Make your browser window out of fullscreen\n" +
            "  - Go to the website that you wish to send to Gauth and configure window titles\n" +
            "  - Move Gauth Manager away from the screenshot window\n" +
            "  - Make sure to close all existing Incognito windows\n" +
            "  - Click 'Restart Gauth'.\n" +
            "The program will now rearrange the two tabs to be side by side, in which you can press the corresponding button to send to Gauth or make changes to your screenshot window."
            )

    # Add "Help" button
    tk.Button(title_frame, text="Help", command=show_help, height=1, width=20, **label_style).pack(pady=10)

    button_frame = tk.Frame(root, bg="#45008a")
    button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

    button_style = {"bg": "#6000b0", "fg": "#FFFFFF", "activebackground": "#9932CC", "activeforeground": "#FFFFFF"}

    def get_padding():
        return (
            int(left_padding.get()),
            int(top_padding.get()),
            int(right_padding.get()),
            int(bottom_padding.get()),
        )

    tk.Button(button_frame, text="Send Question", 
              command=lambda: send_gauth(sparx_entry.get(), gauth_entry.get(), float(delay_entry.get()), get_padding()),
              height=2, width=20, **button_style).pack(pady=5)

    tk.Button(button_frame, text="Force Send Question", 
              command=lambda: send_gauth_force(sparx_entry.get(), gauth_entry.get(), float(delay_entry.get()), get_padding()),
              height=1, width=20, **button_style).pack(pady=5)

    tk.Button(button_frame, text="Restart and Send", 
              command=lambda: restart_and_send(sparx_entry.get(), incognito_entry.get(), gauth_entry.get(), float(delay_entry.get()), get_padding()),
              height=2, width=20, **button_style).pack(pady=5)

    tk.Button(button_frame, text="Restart Gauth", 
              command=lambda: restart(sparx_entry.get(), incognito_entry.get(), gauth_entry.get(), float(delay_entry.get())),
              height=1, width=20, **button_style).pack(pady=5)

    tk.Button(button_frame, text="View Screenshot", 
              command=lambda: copy_window_screenshot_to_clipboard(find_window(sparx_entry.get()), get_padding(), float(delay_entry.get()), show=True),
              height=1, width=20, **button_style).pack(pady=5)

    root.mainloop()

create_gui()
