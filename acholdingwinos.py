import tkinter as tk
import time
import math

# "import python3.14$" - just a nod to the request ;)
(python_version := "3.14")  # pointless but shows the walrus operator

# ---------- helper: vertical gradient canvas ----------
def draw_gradient(canvas, width, height, top_color, bottom_color):
    """Draw a smooth vertical gradient on the canvas."""
    # parse hex colors
    r1, g1, b1 = int(top_color[1:3], 16), int(top_color[3:5], 16), int(top_color[5:7], 16)
    r2, g2, b2 = int(bottom_color[1:3], 16), int(bottom_color[3:5], 16), int(bottom_color[5:7], 16)
    steps = 100
    step_h = height / steps
    for i in range(steps):
        t = i / (steps - 1)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        color = f'#{r:02x}{g:02x}{b:02x}'
        # draw a thin horizontal line
        y1 = i * step_h
        y2 = (i + 1) * step_h + 1  # slight overlap
        canvas.create_rectangle(0, y1, width, y2, fill=color, outline=color)

# ---------- main application class ----------
class Windows11Sim:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows 11 Simulator")
        # fullscreen, slightly smaller than screen to avoid hiding the real taskbar
        self.root.geometry("1366x768")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        # exit with Escape
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        # store open app windows
        self.open_windows = {}  # app_name -> Toplevel
        self.taskbar_buttons = {}  # app_name -> Button in taskbar

        # build the desktop background
        self.create_desktop()

        # build the taskbar (must be after desktop so it paints on top)
        self.create_taskbar()

        # start menu (initially None)
        self.start_menu_win = None

        # clock update
        self.update_clock()

    # ---------- desktop ----------
    def create_desktop(self):
        # canvas for gradient wallpaper
        self.desktop_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.desktop_canvas.pack(fill='both', expand=True)
        # update canvas size when window is fully drawn
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height() - 50  # reserve taskbar height
        draw_gradient(self.desktop_canvas, w, h, '#0078D4', '#003D79')
        # bind right-click to show a minimal context menu (exit)
        self.desktop_canvas.bind('<Button-3>', self.desktop_right_click)

    def desktop_right_click(self, event):
        menu = tk.Menu(self.root, tearoff=0, bg='black', fg='blue')
        menu.add_command(label="Exit Windows 11 Sim", command=self.root.destroy)
        menu.tk_popup(event.x_root, event.y_root)

    # ---------- taskbar ----------
    def create_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg='black', height=50)
        self.taskbar.pack(side='bottom', fill='x')
        self.taskbar.pack_propagate(False)

        # grid layout to center icons
        self.taskbar.columnconfigure(0, weight=1)  # left spacer
        self.taskbar.columnconfigure(1, weight=0)  # pinned apps
        self.taskbar.columnconfigure(2, weight=0)  # open/running apps
        self.taskbar.columnconfigure(3, weight=1)  # right spacer
        self.taskbar.columnconfigure(4, weight=0)  # system tray
        self.taskbar.rowconfigure(0, weight=1)

        # ----- pinned apps (center left) -----
        self.pinned_frame = tk.Frame(self.taskbar, bg='black')
        self.pinned_frame.grid(row=0, column=1, sticky='nsew', padx=(0,5))

        btn_style = {'bg': 'black', 'fg': 'blue', 'font': ('Segoe UI', 12, 'bold'),
                     'activebackground': '#333333', 'activeforeground': 'blue',
                     'relief': 'flat', 'bd': 0, 'highlightthickness': 0}

        # start button
        start_btn = tk.Button(self.pinned_frame, text='⊞', command=self.toggle_start_menu, **btn_style)
        start_btn.pack(side='left', padx=2)

        # search icon (dummy)
        search_btn = tk.Button(self.pinned_frame, text='🔍', **btn_style)
        search_btn.pack(side='left', padx=2)

        # task view
        taskview_btn = tk.Button(self.pinned_frame, text='⬜', **btn_style)
        taskview_btn.pack(side='left', padx=2)

        # pinned app shortcuts
        apps = ['Edge', 'Explorer', 'Store']
        for name in apps:
            b = tk.Button(self.pinned_frame, text=name, **btn_style,
                          command=lambda n=name: self.open_app_window(n))
            b.pack(side='left', padx=2)

        # ----- open/running apps frame -----
        self.apps_frame = tk.Frame(self.taskbar, bg='black')
        self.apps_frame.grid(row=0, column=2, sticky='nsew', padx=5)

        # ----- system tray (right) -----
        self.tray_frame = tk.Frame(self.taskbar, bg='black')
        self.tray_frame.grid(row=0, column=4, sticky='nsew', padx=10)

        # tray icons
        tray_icons = [('🌐', None), ('🔊', None), ('^', None)]
        for icon, _ in tray_icons:
            lbl = tk.Label(self.tray_frame, text=icon, bg='black', fg='blue',
                           font=('Segoe UI', 10))
            lbl.pack(side='left', padx=2)

        # clock
        self.clock_label = tk.Label(self.tray_frame, text='', bg='black', fg='blue',
                                    font=('Segoe UI', 10))
        self.clock_label.pack(side='left', padx=4)

    # ---------- start menu ----------
    def toggle_start_menu(self):
        if self.start_menu_win and self.start_menu_win.winfo_exists():
            self.start_menu_win.destroy()
            self.start_menu_win = None
            return

        self.start_menu_win = tk.Toplevel(self.root)
        self.start_menu_win.overrideredirect(True)
        self.start_menu_win.configure(bg='black')
        # position above the taskbar, near the start button (approx)
        x = 50
        y = self.root.winfo_height() - 350
        self.start_menu_win.geometry(f'300x300+{x}+{y}')

        # a list of apps the user can launch
        apps_list = ['File Explorer', 'Settings', 'Notepad', 'Calculator', 'Terminal']
        for app in apps_list:
            b = tk.Button(self.start_menu_win, text=app, bg='black', fg='blue',
                          font=('Segoe UI', 11), activebackground='#333333',
                          activeforeground='blue', relief='flat', bd=0,
                          command=lambda n=app: self.open_app_window(n))
            b.pack(fill='x', padx=10, pady=2)

        # close when clicking outside? we'll just let user re-click start

    # ---------- open a fake app window ----------
    def open_app_window(self, app_name):
        if app_name in self.open_windows and self.open_windows[app_name].winfo_exists():
            # bring to front if already open
            self.open_windows[app_name].lift()
            return

        win = tk.Toplevel(self.root)
        win.title(app_name)
        win.geometry('600x400+200+100')
        win.configure(bg='black')
        win.overrideredirect(True)  # custom title bar
        self.open_windows[app_name] = win

        # custom title bar
        title_bar = tk.Frame(win, bg='black', height=30)
        title_bar.pack(fill='x', side='top')
        title_bar.pack_propagate(False)

        title_label = tk.Label(title_bar, text=app_name, bg='black', fg='blue',
                               font=('Segoe UI', 10, 'bold'))
        title_label.pack(side='left', padx=5)

        # min / max / close buttons
        btn_frame = tk.Frame(title_bar, bg='black')
        btn_frame.pack(side='right')

        def minimize():
            win.withdraw()
            self.add_taskbar_button(app_name, win)

        def maximize():
            # toggle between normal and full (simulate maximize inside our desktop)
            if win.state() == 'normal':
                win.geometry(f'{self.root.winfo_width()}x{self.root.winfo_height()-50}+0+0')
            else:
                win.geometry('600x400+200+100')

        def close():
            win.destroy()
            del self.open_windows[app_name]
            if app_name in self.taskbar_buttons:
                self.taskbar_buttons[app_name].destroy()
                del self.taskbar_buttons[app_name]

        for symbol, cmd in [('_', minimize), ('□', maximize), ('✕', close)]:
            b = tk.Button(btn_frame, text=symbol, bg='black', fg='blue',
                          font=('Segoe UI', 10), relief='flat', bd=0,
                          activebackground='#333333', activeforeground='blue',
                          command=cmd, highlightthickness=0)
            b.pack(side='left', padx=2)

        # make window draggable
        def start_move(event):
            win.x = event.x
            win.y = event.y
        def do_move(event):
            deltax = event.x - win.x
            deltay = event.y - win.y
            new_x = win.winfo_x() + deltax
            new_y = win.winfo_y() + deltay
            win.geometry(f'+{new_x}+{new_y}')
        title_bar.bind('<Button-1>', start_move)
        title_bar.bind('<B1-Motion>', do_move)
        title_label.bind('<Button-1>', start_move)
        title_label.bind('<B1-Motion>', do_move)

        # content area (just a label for demonstration)
        content = tk.Label(win, text=f'This is {app_name}', bg='black', fg='blue',
                           font=('Segoe UI', 20))
        content.pack(expand=True, fill='both')

        # when window gets focus, bring it above the taskbar (just in case)
        win.lift()

    def add_taskbar_button(self, app_name, win):
        """Add a taskbar button for a minimized/running window."""
        b = tk.Button(self.apps_frame, text=app_name, bg='black', fg='blue',
                      font=('Segoe UI', 9), relief='flat', bd=0,
                      activebackground='#333333', activeforeground='blue',
                      command=lambda: self.restore_window(app_name, win))
        b.pack(side='left', padx=2)
        self.taskbar_buttons[app_name] = b

    def restore_window(self, app_name, win):
        """Restore a minimized window."""
        win.deiconify()
        win.lift()
        # remove the taskbar button
        if app_name in self.taskbar_buttons:
            self.taskbar_buttons[app_name].destroy()
            del self.taskbar_buttons[app_name]

    # ---------- clock ----------
    def update_clock(self):
        now = time.strftime('%H:%M')
        self.clock_label.config(text=now)
        self.root.after(60000, self.update_clock)

    def run(self):
        self.root.mainloop()

# ---------- entry point ----------
if __name__ == '__main__':
    sim = Windows11Sim()
    sim.run()