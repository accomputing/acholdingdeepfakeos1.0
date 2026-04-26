import tkinter as tk
import time
import math
import random

# ---------- dummy import for Python 3.14 ----------
try:
    import python314  # This will never work — just a joke
except ImportError:
    pass

# ---------- Gradient helper for desktop wallpaper ----------
def draw_gradient(canvas, width, height, top_color, bottom_color):
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
        canvas.create_rectangle(0, i * step_h, width, (i + 1) * step_h + 1,
                                fill=color, outline=color)

# ---------- Simulated web page generator ----------
FAKE_SITES = {
    "fakebook.com": {
        "title": "Fakebook - Log In or Sign Up",
        "style": "social",
        "content": [
            ("h1", "Welcome to Fakebook"),
            ("p", "Connect with friends and the world around you."),
            ("link", "News Feed", "/newsfeed"),
            ("link", "Messenger", "/messenger"),
            ("link", "Watch", "/watch"),
            ("img", "📷 [Photo: Vacation]"),
            ("p", "Trending: Python 3.14 leaked screenshots!")
        ]
    },
    "zonazon.com": {
        "title": "Zonazon - Everything Store",
        "style": "shopping",
        "content": [
            ("h1", "Today's Deals"),
            ("p", "Up to 70% off on electronics, books, and more."),
            ("link", "Laptops", "/laptops"),
            ("link", "Smart Home", "/smart-home"),
            ("img", "🛒 [Product Image: 4K Monitor]"),
            ("p", "Lightning Deal: Wireless Mouse $12.99")
        ]
    },
    "newsify.net": {
        "title": "Newsify - Breaking News",
        "style": "news",
        "content": [
            ("h1", "Top Stories"),
            ("h2", "AI assistant passes Turing Test, demands vacation"),
            ("p", "In a shocking development, a simulated intelligence..."),
            ("link", "Read more", "/article/1"),
            ("h2", "Python 3.14 to include built-in time travel"),
            ("p", "Developers confirm the rumored 'import antigravity'..."),
            ("link", "Read more", "/article/2"),
        ]
    },
    "catpics.org": {
        "title": "Cat Pictures - The Internet's Purpose",
        "style": "gallery",
        "content": [
            ("h1", "Random Cat Pictures"),
            ("img", "🐱 [Cute cat sleeping]"),
            ("img", "😺 [Cat on a keyboard]"),
            ("p", "You're welcome."),
            ("link", "More cats", "/more")
        ]
    },
    "searchme.com": {
        "title": "SearchMe - Find Anything",
        "style": "search",
        "content": [
            ("h1", "Search the web"),
            ("search", ""),
            ("p", "Popular: Python 3.14, Blue Screen of Death, Cat memes")
        ]
    }
}

def generate_random_page(domain=None):
    """Return (title, html_content_as_text_with_tags) for a random page."""
    if domain and domain in FAKE_SITES:
        site = FAKE_SITES[domain]
    else:
        # pick a random domain (excluding search engine)
        possible = [d for d in FAKE_SITES if d != "searchme.com"]
        if not possible:
            possible = list(FAKE_SITES.keys())
        domain = random.choice(possible)
        site = FAKE_SITES[domain]

    title = site["title"]
    # Build fake HTML-ish text
    lines = []
    for tag, text in site["content"]:
        if tag == "h1":
            lines.append(f"# {text}")
        elif tag == "h2":
            lines.append(f"## {text}")
        elif tag == "p":
            lines.append(text)
        elif tag == "link":
            lines.append(f">>> {text}")  # clickable link representation
        elif tag == "img":
            lines.append(f"[IMG] {text}")
        elif tag == "search":
            # Will be handled separately in the browser
            lines.append("[SEARCHBOX]")
    return title, "\n".join(lines)

# ---------- Main Windows 11 Simulator ----------
class Windows11_25H2:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows 11 25H2 – Tkinter Edition")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='black')
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        # Data stores
        self.open_apps = {}          # app_name -> Toplevel
        self.taskbar_app_buttons = {}  # app_name -> Button
        self.pinned_apps = ['File Explorer', 'Microsoft Edge', 'Microsoft Store',
                            'Settings', 'Notepad', 'Terminal', 'Calculator']

        # Popups / flyouts (None when hidden)
        self.start_menu = None
        self.widgets_panel = None
        self.quick_settings = None
        self.notif_center = None

        # Build layers
        self.create_desktop()
        self.create_taskbar()
        self.update_clock()
        self.root.after(100, self.ensure_size)

    # ---------- Desktop wallaper ----------
    def create_desktop(self):
        self.desktop = tk.Canvas(self.root, highlightthickness=0)
        self.desktop.pack(fill='both', expand=True)
        # Right-click menu
        self.desktop.bind('<Button-3>', self.show_desktop_menu)

    def show_desktop_menu(self, event):
        menu = tk.Menu(self.root, tearoff=0, bg='black', fg='blue')
        menu.add_command(label="Exit Windows 11 Simulation", command=self.root.destroy)
        menu.add_separator()
        menu.add_command(label="Simulate BSOD", command=self.trigger_bsod)  # Special feature
        menu.tk_popup(event.x_root, event.y_root)

    def trigger_bsod(self):
        """Simulated Blue Screen of Death."""
        bsod = tk.Toplevel(self.root)
        bsod.attributes('-fullscreen', True)
        bsod.configure(bg='#0078D4')  # Classic Windows blue
        bsod.overrideredirect(True)
        bsod.lift()

        fg = 'white'
        bg = '#0078D4'
        frame = tk.Frame(bsod, bg=bg)
        frame.place(relx=0.5, rely=0.4, anchor='center')

        sad_face = tk.Label(frame, text=":(", font=('Segoe UI', 72), bg=bg, fg=fg)
        sad_face.pack()

        tk.Label(frame, text="Your PC ran into a problem and needs to restart.",
                 font=('Segoe UI', 14), bg=bg, fg=fg).pack(pady=10)
        tk.Label(frame, text="We're just collecting some error info, and then we'll restart for you.",
                 font=('Segoe UI', 10), bg=bg, fg=fg).pack()
        tk.Label(frame, text="", bg=bg).pack(pady=5)

        progress = tk.Label(frame, text="0% complete", font=('Segoe UI', 9), bg=bg, fg=fg)
        progress.pack()

        qr = tk.Label(frame, text="■■■■■■■■\n■■■■■■■■\n■■■■■■■■\n■■■■■■■■",
                      font=('Courier', 16), bg='white', fg='black', width=10, height=4)
        qr.pack(pady=10)

        info = tk.Label(frame, text="Stop code: IRQL_NOT_LESS_OR_EQUAL",
                        font=('Segoe UI', 10, 'bold'), bg=bg, fg=fg)
        info.pack()

        def update_progress(pct=0):
            if pct <= 100 and bsod.winfo_exists():
                progress.config(text=f"{pct}% complete")
                bsod.after(50, update_progress, pct+1)
            else:
                if bsod.winfo_exists():
                    bsod.destroy()

        bsod.after(100, update_progress)
        bsod.bind('<Button-1>', lambda e: bsod.destroy())
        bsod.bind('<Key>', lambda e: bsod.destroy())
        bsod.focus_set()

    def ensure_size(self):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        if w > 1 and h > 50:
            self.desktop.delete('all')
            draw_gradient(self.desktop, w, h - 48, '#0078D4', '#003D79')
            self.desktop_painted = True

    # ---------- Taskbar ----------
    def create_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg='black', height=48)
        self.taskbar.pack(side='bottom', fill='x')
        self.taskbar.pack_propagate(False)

        # Grid layout: left (widgets trigger), center, right
        self.taskbar.columnconfigure(0, weight=0)   # Widgets button (left)
        self.taskbar.columnconfigure(1, weight=1)   # center spacer
        self.taskbar.columnconfigure(2, weight=0)   # app icons
        self.taskbar.columnconfigure(3, weight=1)   # center spacer
        self.taskbar.columnconfigure(4, weight=0)   # system tray
        self.taskbar.rowconfigure(0, weight=1)

        # Widgets button (left edge)
        self.widgets_btn = tk.Button(self.taskbar, text='☰', bg='black', fg='blue',
                                     font=('Segoe UI', 14), relief='flat',
                                     command=self.toggle_widgets, activebackground='#333')
        self.widgets_btn.grid(row=0, column=0, padx=4, pady=4)

        # Center app area (pinned + running)
        self.apps_area = tk.Frame(self.taskbar, bg='black')
        self.apps_area.grid(row=0, column=2, sticky='nsew')
        # Put pinned apps first
        for app in self.pinned_apps:
            btn = self.make_task_button(app)
            btn.pack(side='left', padx=1)
        # Separator (visual only) – a thin line
        sep = tk.Frame(self.apps_area, bg='#444', width=1)
        sep.pack(side='left', padx=2, fill='y')
        # Running apps (added dynamically)
        self.running_apps_frame = tk.Frame(self.apps_area, bg='black')
        self.running_apps_frame.pack(side='left')

        # System tray (right)
        tray = tk.Frame(self.taskbar, bg='black')
        tray.grid(row=0, column=4, padx=10, sticky='e')
        # Up arrow (show hidden icons)
        tk.Label(tray, text='^', bg='black', fg='blue', font=('Segoe UI', 10)).pack(side='left', padx=2)
        # Network / sound / battery (combined)
        self.qs_btn = tk.Label(tray, text='🌐🔊🔋', bg='black', fg='blue', font=('Segoe UI', 10))
        self.qs_btn.pack(side='left', padx=4)
        self.qs_btn.bind('<Button-1>', lambda e: self.toggle_quick_settings())
        # Clock / date (opens notification center)
        self.clock_label = tk.Label(tray, text='', bg='black', fg='blue', font=('Segoe UI', 10))
        self.clock_label.pack(side='left', padx=4)
        self.clock_label.bind('<Button-1>', lambda e: self.toggle_notif_center())

        # Start button (left of app area)
        self.start_btn = self.make_task_button('⊞')
        self.start_btn.pack(in_=self.apps_area, side='left', before=self.apps_area.winfo_children()[0])

    def make_task_button(self, text):
        return tk.Button(self.taskbar, text=text, bg='black', fg='blue',
                         font=('Segoe UI', 11), relief='flat',
                         activebackground='#333', activeforeground='blue',
                         command=lambda t=text: self.on_task_button(t))

    def on_task_button(self, text):
        if text == '⊞':
            self.toggle_start_menu()
        elif text in self.pinned_apps:
            self.open_app(text)
        # else: running app (handled separately)

    # ---------- Windows management ----------
    def open_app(self, app_name):
        if app_name in self.open_apps and self.open_apps[app_name].winfo_exists():
            self.open_apps[app_name].lift()
            return

        win = tk.Toplevel(self.root)
        win.title(app_name)
        win.geometry(self.random_geometry())
        win.configure(bg='black')
        win.overrideredirect(True)   # custom chrome
        win.attributes('-topmost', False)
        self.open_apps[app_name] = win

        # Taskbar indicator
        btn = tk.Button(self.running_apps_frame, text=app_name, bg='black', fg='blue',
                        font=('Segoe UI', 9), relief='flat', activebackground='#333',
                        activeforeground='blue',
                        command=lambda n=app_name: self.focus_app(n))
        btn.pack(side='left', padx=2)
        self.taskbar_app_buttons[app_name] = btn

        # Title bar
        title_bar = tk.Frame(win, bg='black', height=32, cursor='fleur')
        title_bar.pack(fill='x')
        title_bar.pack_propagate(False)
        title_label = tk.Label(title_bar, text=app_name, bg='black', fg='blue',
                               font=('Segoe UI', 10, 'bold'))
        title_label.pack(side='left', padx=8)
        # Window controls
        btn_frame = tk.Frame(title_bar, bg='black')
        btn_frame.pack(side='right')
        actions = [('_', lambda: win.withdraw() if not win.winfo_ismapped() else None),
                   ('□', lambda: self.maximize_window(win)),
                   ('✕', lambda: self.close_app(app_name))]
        for symbol, cmd in actions:
            b = tk.Button(btn_frame, text=symbol, bg='black', fg='blue',
                          font=('Segoe UI', 10), relief='flat', activebackground='#333',
                          command=cmd)
            b.pack(side='left', padx=2)

        # Make draggable
        def start_move(e):
            win._x = e.x
            win._y = e.y
        def do_move(e):
            x = win.winfo_x() + e.x - win._x
            y = win.winfo_y() + e.y - win._y
            win.geometry(f'+{x}+{y}')
        title_bar.bind('<Button-1>', start_move)
        title_bar.bind('<B1-Motion>', do_move)
        title_label.bind('<Button-1>', start_move)
        title_label.bind('<B1-Motion>', do_move)

        # Window content
        self.build_app_content(win, app_name)

        # Focus binding
        win.bind('<FocusIn>', lambda e, n=app_name: self.highlight_taskbar(n))
        win.protocol('WM_DELETE_WINDOW', lambda n=app_name: self.close_app(n))

    def close_app(self, app_name):
        if app_name in self.open_apps:
            self.open_apps[app_name].destroy()
            del self.open_apps[app_name]
        if app_name in self.taskbar_app_buttons:
            self.taskbar_app_buttons[app_name].destroy()
            del self.taskbar_app_buttons[app_name]

    def focus_app(self, app_name):
        if app_name in self.open_apps and self.open_apps[app_name].winfo_exists():
            win = self.open_apps[app_name]
            if win.winfo_ismapped():
                win.lift()
            else:
                win.deiconify()
                win.lift()

    def highlight_taskbar(self, app_name):
        # Visual feedback is optional
        pass

    def maximize_window(self, win):
        if win.state() == 'normal':
            win.geometry(f'{self.root.winfo_width()}x{self.root.winfo_height()-48}+0+0')
        else:
            win.geometry(self.random_geometry())

    def random_geometry(self):
        w, h = random.randint(500, 800), random.randint(400, 600)
        x = random.randint(50, self.root.winfo_screenwidth()-w-50)
        y = random.randint(50, self.root.winfo_screenheight()-h-100)
        return f'{w}x{h}+{x}+{y}'

    # ---------- App content builders ----------
    def build_app_content(self, win, app_name):
        frame = tk.Frame(win, bg='black')
        frame.pack(fill='both', expand=True)

        if app_name == 'File Explorer':
            # Simple tree + list
            paned = tk.PanedWindow(frame, bg='black', sashwidth=2, sashrelief='flat')
            paned.pack(fill='both', expand=True)
            left = tk.Frame(paned, bg='#111')
            paned.add(left, width=150)
            tk.Label(left, text='Quick access', fg='blue', bg='#111', font=('Segoe UI', 9)).pack(anchor='w', padx=5, pady=2)
            for folder in ['Desktop', 'Downloads', 'Documents', 'Pictures']:
                tk.Label(left, text=f'  📁 {folder}', fg='blue', bg='#111', font=('Segoe UI', 9)).pack(anchor='w', padx=10)
            right = tk.Frame(paned, bg='black')
            paned.add(right)
            tk.Label(right, text='This PC', fg='blue', bg='black', font=('Segoe UI', 12)).pack(anchor='w', padx=10, pady=10)

        elif app_name == 'Settings':
            nb = tk.Frame(frame, bg='black')
            nb.pack(fill='both', expand=True)
            tabs = ['System', 'Bluetooth', 'Network', 'Personalization', 'Apps', 'Accounts', 'Time & Language']
            left_tab = tk.Frame(nb, bg='black', width=150)
            left_tab.pack(side='left', fill='y')
            for tab in tabs:
                tk.Button(left_tab, text=tab, bg='black', fg='blue', relief='flat',
                          font=('Segoe UI', 9), activebackground='#333').pack(fill='x', padx=4, pady=2)
            right_panel = tk.Frame(nb, bg='black')
            right_panel.pack(side='left', fill='both', expand=True)
            tk.Label(right_panel, text='Settings', fg='blue', bg='black', font=('Segoe UI', 16)).pack(pady=20)

        elif app_name == 'Notepad':
            txt = tk.Text(frame, bg='black', fg='blue', insertbackground='blue',
                          font=('Consolas', 12), relief='flat', border=0)
            txt.pack(fill='both', expand=True, padx=2, pady=2)
            txt.insert('1.0', 'Welcome to Notepad\n')

        elif app_name == 'Terminal':
            txt = tk.Text(frame, bg='black', fg='blue', insertbackground='blue',
                          font=('Cascadia Code', 10), relief='flat')
            txt.pack(fill='both', expand=True)
            txt.insert('1.0', 'Windows PowerShell\nCopyright (C) Microsoft Corporation.\n\nPS C:\\Users\\User> ')

        elif app_name == 'Calculator':
            # Simple calculator
            display = tk.Entry(frame, bg='black', fg='blue', font=('Segoe UI', 20),
                               justify='right', relief='flat')
            display.pack(fill='x', padx=10, pady=10)
            buttons = [
                ['%', 'CE', 'C', '⌫'],
                ['1/x', 'x²', '√', '÷'],
                ['7', '8', '9', '×'],
                ['4', '5', '6', '−'],
                ['1', '2', '3', '+'],
                ['±', '0', '.', '=']
            ]
            for row in buttons:
                row_frame = tk.Frame(frame, bg='black')
                row_frame.pack(fill='x', padx=10, pady=2)
                for char in row:
                    tk.Button(row_frame, text=char, bg='black', fg='blue',
                              font=('Segoe UI', 12), relief='flat', activebackground='#333',
                              width=4).pack(side='left', expand=True, fill='x', padx=1)

        elif app_name == 'Microsoft Edge':
            # ---------- Simulated Internet Browser ----------
            # Top bar with address entry
            top_bar = tk.Frame(frame, bg='black')
            top_bar.pack(fill='x', padx=2, pady=2)
            # Navigation buttons
            back_btn = tk.Button(top_bar, text='←', bg='black', fg='blue', font=('Segoe UI', 10),
                                 relief='flat', activebackground='#333')
            back_btn.pack(side='left', padx=2)
            fwd_btn = tk.Button(top_bar, text='→', bg='black', fg='blue', font=('Segoe UI', 10),
                                relief='flat', activebackground='#333')
            fwd_btn.pack(side='left', padx=2)
            refresh_btn = tk.Button(top_bar, text='↻', bg='black', fg='blue', font=('Segoe UI', 10),
                                    relief='flat', activebackground='#333',
                                    command=lambda: self.browser_navigate(win, address_var.get()))
            refresh_btn.pack(side='left', padx=2)

            # Address bar
            address_var = tk.StringVar(value="https://searchme.com")
            address_entry = tk.Entry(top_bar, textvariable=address_var, bg='black', fg='blue',
                                     insertbackground='blue', font=('Segoe UI', 10), relief='flat')
            address_entry.pack(side='left', fill='x', expand=True, padx=2)
            address_entry.bind('<Return>', lambda e: self.browser_navigate(win, address_var.get()))

            go_btn = tk.Button(top_bar, text='Go', bg='black', fg='blue', font=('Segoe UI', 9),
                               relief='flat', activebackground='#333',
                               command=lambda: self.browser_navigate(win, address_var.get()))
            go_btn.pack(side='left', padx=2)

            # Web content display
            content_frame = tk.Frame(frame, bg='black')
            content_frame.pack(fill='both', expand=True, padx=2, pady=2)

            # Use a Text widget to render the fake web page
            self.edge_content = tk.Text(content_frame, bg='black', fg='blue',
                                        insertbackground='blue', font=('Segoe UI', 10),
                                        relief='flat', wrap='word', state='disabled')
            self.edge_content.pack(fill='both', expand=True)
            # Store references for later navigation
            win.edge_address_var = address_var
            win.edge_content_widget = self.edge_content
            win.edge_history = []
            # Load home page
            self.browser_navigate(win, "https://searchme.com")

        else:
            tk.Label(frame, text=f'{app_name}\nApp content placeholder', fg='blue', bg='black',
                     font=('Segoe UI', 14)).pack(expand=True)

    def browser_navigate(self, win, url):
        """Load a new page in the Edge window."""
        # Extract domain from fake URL
        url = url.strip()
        if not url.startswith("https://"):
            url = "https://" + url
        domain = url.replace("https://", "").replace("http://", "").split('/')[0]

        title, page_text = generate_random_page(domain)
        address_var = win.edge_address_var
        address_var.set(url)
        win.title(f"{title} - Microsoft Edge")

        content_widget = win.edge_content_widget
        content_widget.config(state='normal')
        content_widget.delete('1.0', tk.END)

        # Simple rendering: lines with special formatting
        lines = page_text.split('\n')
        for line in lines:
            if line.startswith('# '):
                content_widget.insert(tk.END, line[2:] + '\n', 'h1')
            elif line.startswith('## '):
                content_widget.insert(tk.END, line[3:] + '\n', 'h2')
            elif line.startswith('>>> '):
                # Clickable link representation
                link_text = line[4:]
                start = content_widget.index(tk.END + "-1c")
                content_widget.insert(tk.END, link_text + '\n', 'link')
                end = content_widget.index(tk.END + "-1c")
                # Make it clickable
                content_widget.tag_bind('link', '<Button-1>',
                                        lambda e, u=link_text: self.browser_navigate(win, f"https://{u}"))
            elif line.startswith('[IMG]'):
                content_widget.insert(tk.END, line[5:] + '\n', 'img')
            elif line == '[SEARCHBOX]':
                # already handled by address bar, show a search hint
                content_widget.insert(tk.END, '🔍 Search the simulated web...\n', 'search')
            else:
                content_widget.insert(tk.END, line + '\n')

        # Style tags
        content_widget.tag_config('h1', font=('Segoe UI', 16, 'bold'), foreground='blue')
        content_widget.tag_config('h2', font=('Segoe UI', 13, 'bold'), foreground='blue')
        content_widget.tag_config('link', font=('Segoe UI', 10, 'underline'), foreground='cyan')
        content_widget.tag_config('img', font=('Segoe UI', 10, 'italic'), foreground='#8888ff')
        content_widget.tag_config('search', font=('Segoe UI', 10), foreground='grey')

        content_widget.config(state='disabled')
        # Store history (optional, not fully implemented)
        if not hasattr(win, 'edge_history'):
            win.edge_history = []
        win.edge_history.append(url)

    # ---------- Start Menu ----------
    def toggle_start_menu(self):
        if self.start_menu and self.start_menu.winfo_exists():
            self.start_menu.destroy()
            self.start_menu = None
            return
        self.close_all_popups()

        self.start_menu = tk.Toplevel(self.root)
        self.start_menu.overrideredirect(True)
        self.start_menu.configure(bg='black')
        x = 60
        y = self.root.winfo_height() - 500
        self.start_menu.geometry(f'320x500+{x}+{y}')

        # Search box
        search = tk.Entry(self.start_menu, bg='black', fg='blue', insertbackground='blue',
                          font=('Segoe UI', 10), relief='flat')
        search.pack(fill='x', padx=8, pady=8)
        search.insert(0, 'Type here to search')

        # Pinned apps grid
        pinned_frame = tk.Frame(self.start_menu, bg='black')
        pinned_frame.pack(fill='both', expand=True, padx=8, pady=4)
        tk.Label(pinned_frame, text='Pinned', fg='blue', bg='black',
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        grid = tk.Frame(pinned_frame, bg='black')
        grid.pack(pady=4)
        apps = self.pinned_apps
        row, col = 0, 0
        for app in apps:
            b = tk.Button(grid, text=app, bg='black', fg='blue', font=('Segoe UI', 9),
                          relief='flat', activebackground='#333', width=14, anchor='w',
                          command=lambda n=app: (self.open_app(n), self.start_menu.destroy()))
            b.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 1:
                col = 0
                row += 1

        # Recommended section (simplified)
        rec_frame = tk.Frame(self.start_menu, bg='black')
        rec_frame.pack(fill='both', padx=8, pady=4)
        tk.Label(rec_frame, text='Recommended', fg='blue', bg='black',
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        for doc in ['Project Plan.docx', 'Budget.xlsx', 'Readme.txt']:
            tk.Label(rec_frame, text=f'  📄 {doc}', fg='blue', bg='black', font=('Segoe UI', 9)).pack(anchor='w')

        # User + power
        bottom = tk.Frame(self.start_menu, bg='black')
        bottom.pack(side='bottom', fill='x', padx=8, pady=8)
        tk.Button(bottom, text='👤 User', bg='black', fg='blue', relief='flat',
                  font=('Segoe UI', 9), activebackground='#333').pack(side='left')
        tk.Button(bottom, text='⏻ Power', bg='black', fg='blue', relief='flat',
                  font=('Segoe UI', 9), activebackground='#333',
                  command=self.root.destroy).pack(side='right')

        # Close when clicking outside
        self.start_menu.bind('<FocusOut>', lambda e: self.start_menu.after(50, self.check_start_focus))

    def check_start_focus(self):
        if self.start_menu and not self.start_menu.focus_get():
            self.start_menu.destroy()
            self.start_menu = None

    # ---------- Widgets panel ----------
    def toggle_widgets(self):
        if self.widgets_panel and self.widgets_panel.winfo_exists():
            self.widgets_panel.destroy()
            self.widgets_panel = None
            return
        self.close_all_popups()

        self.widgets_panel = tk.Toplevel(self.root)
        self.widgets_panel.overrideredirect(True)
        self.widgets_panel.configure(bg='black')
        h = self.root.winfo_height() - 48
        self.widgets_panel.geometry(f'300x{h}+0+0')
        # Weather, news, etc.
        tk.Label(self.widgets_panel, text='☁️ 22°C  Sunny', fg='blue', bg='black',
                 font=('Segoe UI', 14)).pack(pady=20)
        for headline in ['Latest News', 'Stock Market', 'Sports', 'Weather forecast']:
            tk.Label(self.widgets_panel, text=f'• {headline}', fg='blue', bg='black',
                     font=('Segoe UI', 10)).pack(anchor='w', padx=20, pady=2)
        # Close when focus lost
        self.widgets_panel.bind('<FocusOut>', lambda e: self.widgets_panel.destroy())

    # ---------- Quick Settings (network/sound/battery) ----------
    def toggle_quick_settings(self):
        if self.quick_settings and self.quick_settings.winfo_exists():
            self.quick_settings.destroy()
            self.quick_settings = None
            return
        self.close_all_popups()

        self.quick_settings = tk.Toplevel(self.root)
        self.quick_settings.overrideredirect(True)
        self.quick_settings.configure(bg='black')
        x = self.root.winfo_width() - 320
        y = self.root.winfo_height() - 300
        self.quick_settings.geometry(f'300x250+{x}+{y}')
        # Tiles
        toggles = [('Wi-Fi', 'On'), ('Bluetooth', 'Off'), ('Airplane mode', 'Off'),
                   ('Battery saver', 'Off'), ('Focus assist', 'Off')]
        for name, state in toggles:
            row = tk.Frame(self.quick_settings, bg='black')
            row.pack(fill='x', padx=10, pady=2)
            tk.Label(row, text=name, fg='blue', bg='black', font=('Segoe UI', 9)).pack(side='left')
            tk.Button(row, text=state, bg='black', fg='blue', relief='flat',
                      activebackground='#333', font=('Segoe UI', 9)).pack(side='right')
        # Brightness & volume sliders (simulated with scales)
        tk.Label(self.quick_settings, text='Brightness', fg='blue', bg='black', font=('Segoe UI', 9)).pack(anchor='w', padx=10)
        tk.Scale(self.quick_settings, from_=0, to=100, orient='horizontal', bg='black', fg='blue',
                 troughcolor='#333', highlightbackground='black').pack(fill='x', padx=10)
        tk.Label(self.quick_settings, text='Volume', fg='blue', bg='black', font=('Segoe UI', 9)).pack(anchor='w', padx=10)
        tk.Scale(self.quick_settings, from_=0, to=100, orient='horizontal', bg='black', fg='blue',
                 troughcolor='#333', highlightbackground='black').pack(fill='x', padx=10)
        self.quick_settings.bind('<FocusOut>', lambda e: self.quick_settings.destroy())

    # ---------- Notification center / calendar ----------
    def toggle_notif_center(self):
        if self.notif_center and self.notif_center.winfo_exists():
            self.notif_center.destroy()
            self.notif_center = None
            return
        self.close_all_popups()

        self.notif_center = tk.Toplevel(self.root)
        self.notif_center.overrideredirect(True)
        self.notif_center.configure(bg='black')
        x = self.root.winfo_width() - 380
        y = self.root.winfo_height() - 500
        self.notif_center.geometry(f'360x450+{x}+{y}')
        # Calendar (month view, simplified)
        cal = tk.Frame(self.notif_center, bg='black')
        cal.pack(fill='x', padx=10, pady=10)
        now = time.localtime()
        month_year = f'{now.tm_year}-{now.tm_mon:02d}'
        tk.Label(cal, text=month_year, fg='blue', bg='black', font=('Segoe UI', 10)).pack()
        days = ['Mo','Tu','We','Th','Fr','Sa','Su']
        header = tk.Frame(cal, bg='black')
        header.pack()
        for d in days:
            tk.Label(header, text=d, fg='blue', bg='black', width=3).pack(side='left')
        # Just a few rows
        for week in range(5):
            row = tk.Frame(cal, bg='black')
            row.pack()
            for day in range(7):
                num = week*7 + day + 1
                lbl = tk.Label(row, text=str(num) if num <= 31 else '', fg='blue', bg='black', width=3)
                lbl.pack(side='left')
        # Notifications
        tk.Label(self.notif_center, text='No new notifications', fg='blue', bg='black',
                 font=('Segoe UI', 9)).pack(pady=20)
        self.notif_center.bind('<FocusOut>', lambda e: self.notif_center.destroy())

    def close_all_popups(self):
        for win in [self.start_menu, self.widgets_panel, self.quick_settings, self.notif_center]:
            if win and win.winfo_exists():
                win.destroy()

    # ---------- Clock update ----------
    def update_clock(self):
        now = time.strftime('%H:%M')
        self.clock_label.config(text=now)
        self.root.after(30000, self.update_clock)

    def run(self):
        self.root.mainloop()

# ---------- Entry point ----------
if __name__ == '__main__':
    sim = Windows11_25H2()
    sim.run()