import pygetwindow as gw
import pyautogui
from PIL import ImageGrab
import win32clipboard
import tkinter as tk
from tkinter import messagebox
import time
from io import BytesIO
import configparser
import os
# Config Handling
def load_config():
    """Load or create configuration file with default values"""
    config = configparser.ConfigParser()
    config['Colors'] = {
        'bg_color': '#45008a',
        'button_color': '#6000b0',
        'text_color': '#ffffff',
        'entry_bg': '#200040'
    }
    config['Padding'] = {
        'top': '200',
        'bottom': '50',
        'left': '50',
        'right': '50'
    }
    config['Settings'] = {
        'delay': '1.0'
    }
    config['Titles'] = {
        'screenshot': 'Sparx Maths',
        'incognito': 'Incognito',
        'gauth': 'Gauth',
        'shortcut': 'ctrl+shift+n'
    }
    if not os.path.exists('config.ini'):
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    else:
        config.read('config.ini')
    return config
# Utility Functions
def find_window(title):
    """Find the first window containing the specified title"""
    for window in gw.getWindowsWithTitle(title):
        return window
    return None
def show_error(message):
    """Display an error message dialog"""
    messagebox.showerror("Error", message)
def sleep_scaled(delay, multiplier=1.0):
    """Sleep for delay * multiplier seconds"""
    time.sleep(delay * multiplier)
def average_color(hex1, hex2):
    rgb1 = tuple(int(hex1[i:i+2], 16) for i in (1, 3, 5))
    rgb2 = tuple(int(hex2[i:i+2], 16) for i in (1, 3, 5))
    
    rgb_average = tuple((c1 + c2) // 2 for c1, c2 in zip(rgb1, rgb2))
    return f'#{rgb_average[0]:02x}{rgb_average[1]:02x}{rgb_average[2]:02x}'
# Window Management
def focus_and_resize(window, x, y, width, height, delay):
    """Activate and resize/move a window"""
    if not window:
        return
    window.activate()
    sleep_scaled(delay, 0.3)
    window.resizeTo(width, height)
    window.moveTo(x, y)
def close_windows_by_titles(titles, delay):
    """Close windows containing any of the specified titles"""
    for win in gw.getAllWindows():
        if any(title in win.title for title in titles):
            try:
                win.activate()
                sleep_scaled(delay, 0.5)
                pyautogui.hotkey('alt', 'f4')
            except Exception as e:
                show_error(f"Error closing {win.title}: {str(e)}")
#  Screenshot Handling
def capture_window_area(window, padding, delay):
    """Capture screenshot of specified window area with padding"""
    if not window:
        show_error("Target window not found")
        return None
    top_pad, bottom_pad, left_pad, right_pad = padding
    sleep_scaled(delay, 0.1)
    
    return ImageGrab.grab(bbox=(
        window.left + left_pad,
        window.top + top_pad,
        window.left + window.width - right_pad,
        window.top + window.height - bottom_pad
    ))
def copy_to_clipboard(image, show_image=False):
    """Copy image to clipboard or display it"""
    if show_image:
        image.show()
        return
    with BytesIO() as output:
        image.save(output, format="BMP")
        data = output.getvalue()[14:]          
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
# Core Operations
def initialize_workspace(screenshot_title, delay):
    """Set up Screenshot window on left half of screen"""
    screenshot_window = find_window(screenshot_title)
    if not screenshot_window:
        show_error("Screenshot window not found")
        return
    screen_width, screen_height = pyautogui.size()
    focus_and_resize(screenshot_window, 0, 0, screen_width//2, screen_height, delay)
def create_incognito_session(incognito_title, shortcut, delay):
    """Create and position new incognito window"""
    pyautogui.hotkey(*shortcut.split("+"))
    sleep_scaled(delay, 0.1)
    
    incognito_window = find_window(incognito_title)
    if not incognito_window:
        show_error("Incognito window not found")
        return
    screen_width, screen_height = pyautogui.size()
    focus_and_resize(incognito_window, 
                    screen_width//2, 0, 
                    screen_width//2, screen_height, 
                    delay)
    
    pyautogui.typewrite("gauthmath.com\n")
    sleep_scaled(delay, 2)
def normal_transfer(source_title, target_title, padding, delay, pre_paste_steps=None):
    """Core screenshot transfer logic"""
    source_window = find_window(source_title)
    target_window = find_window(target_title)
    
    if not source_window or not target_window:
        show_error("Required windows not found")
        return
    screenshot = capture_window_area(source_window, padding, delay)
    if not screenshot:
        return
        
    copy_to_clipboard(screenshot)
    
    
    target_window.activate()
    sleep_scaled(delay, 0.1)
    
    if pre_paste_steps:
        pre_paste_steps()
    
    pyautogui.hotkey("ctrl", "v")
def quick_transfer(screenshot_title, gauth_title, padding, delay):
    """Basic screenshot transfer without extra steps"""
    normal_transfer(screenshot_title, gauth_title, padding, delay)
def forced_transfer(screenshot_title, gauth_title, padding, delay):
    """Transfer with tab reset"""
    def reset_tab():
        pyautogui.hotkey("ctrl", "t")
        sleep_scaled(delay, 0.1)
        pyautogui.hotkey("ctrl", "1")
        pyautogui.hotkey("ctrl", "w")
        pyautogui.typewrite("gauthmath.com\n")
        sleep_scaled(delay, 1.5)
    
    normal_transfer(screenshot_title, gauth_title, padding, delay, reset_tab)
def restart_session(screenshot_title, incognito_title, gauth_title, delay, shortcut):
    """Full session restart"""
    close_windows_by_titles([incognito_title, gauth_title], delay)
    initialize_workspace(screenshot_title, delay)
    create_incognito_session(incognito_title, shortcut, delay)
# GUI Implementation
def create_gui():
    root = tk.Tk()
    root.title("G\u0430uth Manager v0.2b")  # Cyrillic 'a' for process safety
    root.overrideredirect(True)  
    root.resizable(False, False)
    root.attributes("-topmost", True)
    
    config = load_config()
    
    
    BG_COLOR = config.get('Colors', 'bg_color', fallback='#45008a')
    BUTTON_COLOR = config.get('Colors', 'button_color', fallback='#6000b0')
    TEXT_COLOR = config.get('Colors', 'text_color', fallback='#ffffff')
    ENTRY_BG = config.get('Colors', 'entry_bg', fallback='#200040')
    TITLE_BG = average_color(BG_COLOR, "#000000")
    root.configure(bg=BG_COLOR)
    
    # Custom Title Bar
    
    title_bar = tk.Frame(root, bg=TITLE_BG, height=25)
    title_bar.pack(fill='x', side='top')
    
    title_label = tk.Label(title_bar, 
                         text='Gauth Manager v0.3b', 
                         fg='white', 
                         bg=TITLE_BG,
                         font=('Arial', 10, 'bold'))
    title_label.pack(side='left', padx=10)
    
    close_button = tk.Button(title_bar,
                           text='\uff38', # Fullwidth X
                           fg='white',
                           bg=TITLE_BG,
                           activeforeground='white',
                           activebackground=average_color(BG_COLOR, "#ff0000"),
                           bd=0,
                           command=root.destroy,
                           font=('Arial', 12))
    close_button.pack(side='right', padx=10, pady=2)
    
    def start_move(event):
        root.x = event.x
        root.y = event.y
    def stop_move(event):
        root.x = None
        root.y = None
    def do_move(event):
        dx = event.x - root.x
        dy = event.y - root.y
        x = root.winfo_x() + dx
        y = root.winfo_y() + dy
        root.geometry(f"+{x}+{y}")

    title_bar.bind("<ButtonPress-1>", start_move)
    title_bar.bind("<B1-Motion>", do_move)
    title_bar.bind("<ButtonRelease-1>", stop_move)

    title_label.bind("<ButtonPress-1>", start_move)
    title_label.bind("<B1-Motion>", do_move)
    title_label.bind("<ButtonRelease-1>", stop_move)
    
    
    
    style = {"bg": BG_COLOR, "fg": TEXT_COLOR}
    entry_style = {"bg": ENTRY_BG, "fg": TEXT_COLOR, "insertbackground": TEXT_COLOR}
    
    default_screenshot = config.get('Titles', 'screenshot', fallback='Sparx Maths')
    default_incognito = config.get('Titles', 'incognito', fallback='Incognito')
    default_gauth = config.get('Titles', 'gauth', fallback='Gauth')
    default_shortcut = config.get('Titles', 'shortcut', fallback='ctrl+shift+n')
    
    default_padding = (
        config.getint('Padding', 'top', fallback=200),
        config.getint('Padding', 'bottom', fallback=50),
        config.getint('Padding', 'left', fallback=50),
        config.getint('Padding', 'right', fallback=50)
    )
    
    default_delay = config.getfloat('Settings', 'delay', fallback=1.0)
    
    def create_padding_frame(parent):
        frame = tk.Frame(parent, bg=BG_COLOR)
        
        entries = {}
        labels = [
            ("Padding Top:", "top_pad", default_padding[0]),
            ("Padding Bottom:", "bottom_pad", default_padding[1]),
            ("Padding Left:", "left_pad", default_padding[2]),
            ("Padding Right:", "right_pad", default_padding[3]),
        ]
        for text, key, default in labels:
            tk.Label(frame, text=text, **style).pack(anchor="w")
            entry = tk.Entry(frame, width=10, **entry_style)
            entry.insert(0, str(default))
            entry.pack(anchor="w")
            entries[key] = entry
        tk.Label(frame, text="Delay (s):", **style).pack(anchor="w")
        delay_entry = tk.Entry(frame, width=10, **entry_style)
        delay_entry.insert(0, str(default_delay))
        delay_entry.pack(anchor="w")
        
        return frame, entries, delay_entry
    def create_title_frame(parent):
        frame = tk.Frame(parent, bg=BG_COLOR)
        
        titles = [
            ("Screenshot Window Title:", "screenshot", default_screenshot),
            ("Incognito Window Title:", "incognito", default_incognito),
            ("Gauth Window Title:", "gauth", default_gauth),
            ("Incognito Shortcut:", "shortcut", default_shortcut),
        ]
        entries = {}
        for text, key, default in titles:
            tk.Label(frame, text=text, **style).pack(pady=2)
            entry = tk.Entry(frame, width=25, **entry_style)
            entry.insert(0, default)
            entry.pack(pady=2)
            entries[key] = entry
            
        return frame, entries
    
    def create_control_buttons(parent, entries, padding_entries, delay_entry):
        def get_padding():
            try:
                return (
                    int(padding_entries["top_pad"].get()),
                    int(padding_entries["bottom_pad"].get()),
                    int(padding_entries["left_pad"].get()),
                    int(padding_entries["right_pad"].get()),
                )
            except ValueError:
                show_error("Invalid padding values")
                return default_padding
        def get_delay():
            try:
                return float(delay_entry.get())
            except ValueError:
                show_error("Invalid delay value")
                return default_delay
        button_data = [
            ("Send Question", lambda: normal_transfer(
                entries["screenshot"].get(),
                entries["gauth"].get(),
                get_padding(),
                get_delay(),
                lambda: (pyautogui.hotkey("tab", "enter"), sleep_scaled(get_delay(), 1))
            ), (2, 20)),
            ("Force Send", lambda: forced_transfer(
                entries["screenshot"].get(),
                entries["gauth"].get(),
                get_padding(),
                get_delay()
            ), (1, 20)),
            ("Restart & Send", lambda: (
                restart_session(
                    entries["screenshot"].get(),
                    entries["incognito"].get(),
                    entries["gauth"].get(),
                    get_delay(),
                    entries["shortcut"].get()
                ),
                sleep_scaled(get_delay(), 1),
                quick_transfer(
                    entries["screenshot"].get(),
                    entries["gauth"].get(),
                    get_padding(),
                    get_delay()
                )
            ), (2, 20)),
            ("Restart Gauth", lambda: restart_session(
                entries["screenshot"].get(),
                entries["incognito"].get(),
                entries["gauth"].get(),
                get_delay(),
                entries["shortcut"].get()
            ), (1, 20)),
            ("View Screenshot", lambda: (
                copy_to_clipboard(
                    capture_window_area(
                        find_window(entries["screenshot"].get()),
                        get_padding(),
                        get_delay()
                    ),
                    show_image=True
                )
            ), (1, 20))
        ]
        frame = tk.Frame(parent, bg=BG_COLOR)
        for text, command, (height, width) in button_data:
            btn = tk.Button(
                frame,
                text=text,
                command=command,
                bg=BUTTON_COLOR,
                fg=TEXT_COLOR,
                activebackground="#9932CC",
                height=height,
                width=width
            )
            btn.pack(pady=5)
            
        return frame
    
    padding_frame, padding_entries, delay_entry = create_padding_frame(root)
    padding_frame.pack(side=tk.LEFT, padx=10, pady=10)
    title_frame, title_entries = create_title_frame(root)
    title_frame.pack(side=tk.LEFT, padx=10, pady=10)
    
    HELP_TEXT = """Inputs & Buttons:
Padding: Area to crop from window edges (left, top, right, bottom)
Delay: Execution speed control (lower = faster, might cause issues)
Window Titles: Partial window titles to identify applications
Incognito Shortcut: Keyboard shortcut to open private browsing
Send Question: Screenshot transfer to Gauth
Force Send: More reliable screenshot transfer
Restart & Send: Full reset then transfer
Restart Gauth: Reset incognito session
View Screenshot: Preview captured area (w/ padding)

Setup Guide:
1. Prepare the browser window (make sure it's not fullscreen)
2. Configure window titles
3. Position Gauth Manager away from content
4. Close existing incognito windows
5. Click 'Restart and Send'

Customization:
You can customize the colors of this program by going into the config.ini file in the same directory and changing the hex colors under the 'Colors' header.

Program made by Gallium-Gonzollium // Sparxist
"""
    help_btn = tk.Button(
        title_frame,
        text="Help",
        command=lambda: messagebox.showinfo("Help (Gauth Manager v0.3b)", HELP_TEXT),
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground="#9932CC",
        height=1,
        width=20
    )   
    help_btn.pack(pady=10)
    
    button_frame = create_control_buttons(root, title_entries, padding_entries, delay_entry)
    button_frame.pack(side=tk.RIGHT, padx=10, pady=10)
    
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")
    
    def on_closing():
        """Save current settings to config file"""
        EXEMPT_SECTIONS = {'Colors'}  
        
        current_config = configparser.ConfigParser()
        current_config.read('config.ini')
        
        for section in current_config.sections():
            if section in EXEMPT_SECTIONS:
                continue  
            
            if section == 'Padding':
                current_config[section]['left'] = padding_entries['left_pad'].get()
                current_config[section]['top'] = padding_entries['top_pad'].get()
                current_config[section]['right'] = padding_entries['right_pad'].get()
                current_config[section]['bottom'] = padding_entries['bottom_pad'].get()
            elif section == 'Settings':
                current_config[section]['delay'] = delay_entry.get()
            elif section == 'Titles':
                current_config[section]['screenshot'] = title_entries['screenshot'].get()
                current_config[section]['incognito'] = title_entries['incognito'].get()
                current_config[section]['gauth'] = title_entries['gauth'].get()
                current_config[section]['shortcut'] = title_entries['shortcut'].get()
        
        with open('config.ini', 'w') as configfile:
            current_config.write(configfile)
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
if __name__ == "__main__":
    create_gui()