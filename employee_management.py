# ============================================================
# Advanced Employee Management System
# Python CustomTkinter + Oracle Database
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import oracledb
import csv
import re
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set modern UI theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# ============================================================
# DATABASE CONFIGURATION 
# ============================================================
DB_USER     = "system"
DB_PASSWORD = "Arslanfareed72"
DB_DSN      = "localhost:1521/orcl"


def get_connection():
    try:
        conn = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=DB_DSN)
        return conn
    except oracledb.DatabaseError as e:
        messagebox.showerror("Database Error", f"Cannot connect to Oracle:\n{e}")
        return None

# ============================================================
#  LOGIN WINDOW
# ============================================================
class LoginWindow:
    # Colour palette — identical to the main dashboard
    _BG       = "#080d18"
    _PANEL    = "#0d1424"
    _CARD     = "#101828"
    _FIELD    = "#141f33"
    _GOLD     = "#c9a227"
    _GOLD_DIM = "#8a6d18"
    _TXT      = "#e8eaf0"
    _MUTED    = "#4a5568"
    _ERR      = "#ef4444"

    W, H = 820, 500

    def __init__(self, root):
        self.root = root
        self.root.title("System Login")
        self.root.resizable(False, False)
        self._center_window()
        self._build_ui()

    def _center_window(self):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{self.W}x{self.H}+{(sw - self.W)//2}+{(sh - self.H)//2}")

    def _build_ui(self):
        # Outer wrapper fills the CTk root
        outer = ctk.CTkFrame(self.root, fg_color=self._BG, corner_radius=0)
        outer.pack(fill="both", expand=True)

        # ── LEFT PANEL — geometric canvas art ─────────────────
        left = tk.Frame(outer, bg=self._PANEL, width=340)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        canvas = tk.Canvas(left, width=340, height=self.H,
                           bg=self._PANEL, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Layered angular polygons
        canvas.create_polygon(0, 0, 340, 0, 340, 180, 120, 120,
                              fill="#0a1220", outline="")
        canvas.create_polygon(0, 160, 220, 220, 340, 340, 340, 500, 0, 500,
                              fill="#0b1628", outline="")
        canvas.create_polygon(100, 0, 340, 0, 340, 120,
                              fill="#0f1e35", outline="")
        canvas.create_polygon(0, 280, 180, 310, 260, 500, 0, 500,
                              fill="#0a1422", outline="")

        # Dot grid texture
        for gy in range(0, self.H + 1, 28):
            for gx in range(0, 341, 28):
                canvas.create_oval(gx - 1, gy - 1, gx + 1, gy + 1,
                                   fill="#1a2e4a", outline="")

        # Gold accent lines
        canvas.create_line(0, 70, 340, 70, fill=self._GOLD_DIM, width=1)
        canvas.create_line(30, 420, 310, 420, fill=self._GOLD_DIM, width=1)
        canvas.create_line(260, 0, 340, 80, fill=self._GOLD, width=2)
        canvas.create_line(0, 390, 80, 500, fill=self._GOLD, width=2)

        # Brand text
        canvas.create_text(170, 185, text="EMP",
                           font=("Segoe UI", 58, "bold"),
                           fill=self._GOLD, anchor="center")
        canvas.create_text(170, 248, text="PORTAL",
                           font=("Segoe UI", 17, "bold"),
                           fill=self._TXT, anchor="center")
        canvas.create_text(170, 278, text="Enterprise Management System",
                           font=("Segoe UI", 9),
                           fill=self._MUTED, anchor="center")
        canvas.create_text(170, 390, text="Authorized Personnel Only",
                           font=("Segoe UI", 8, "italic"),
                           fill=self._MUTED, anchor="center")

        # Gold vertical separator
        tk.Frame(outer, bg=self._GOLD, width=2).pack(side="left", fill="y")

        # ── RIGHT PANEL — login form ───────────────────────────
        right = tk.Frame(outer, bg=self._CARD)
        right.pack(side="right", fill="both", expand=True)

        form = tk.Frame(right, bg=self._CARD)
        form.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form, text="Welcome Back",
                 bg=self._CARD, fg=self._TXT,
                 font=("Segoe UI", 24, "bold")).pack(anchor="w")
        tk.Label(form, text="Sign in to your account",
                 bg=self._CARD, fg=self._MUTED,
                 font=("Segoe UI", 11)).pack(anchor="w", pady=(4, 32))

        # Username
        tk.Label(form, text="USERNAME",
                 bg=self._CARD, fg=self._GOLD,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.username_var = tk.StringVar()
        u_box = tk.Frame(form, bg=self._FIELD)
        u_box.pack(fill="x", pady=(5, 0))
        tk.Entry(u_box, textvariable=self.username_var,
                 bg=self._FIELD, fg=self._TXT,
                 insertbackground=self._GOLD,
                 font=("Segoe UI", 13), bd=0, relief="flat",
                 width=30).pack(padx=14, pady=10)
        tk.Frame(u_box, bg=self._GOLD, height=2).pack(fill="x")

        # Password
        tk.Label(form, text="PASSWORD",
                 bg=self._CARD, fg=self._GOLD,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(20, 0))
        self.password_var = tk.StringVar()
        p_box = tk.Frame(form, bg=self._FIELD)
        p_box.pack(fill="x", pady=(5, 0))
        tk.Entry(p_box, textvariable=self.password_var, show="*",
                 bg=self._FIELD, fg=self._TXT,
                 insertbackground=self._GOLD,
                 font=("Segoe UI", 13), bd=0, relief="flat",
                 width=30).pack(padx=14, pady=10)
        tk.Frame(p_box, bg=self._GOLD, height=2).pack(fill="x")

        # Sign In button
        tk.Button(
            form, text="SIGN IN",
            bg=self._GOLD, fg=self._BG,
            font=("Segoe UI", 12, "bold"),
            activebackground="#a8841e", activeforeground=self._BG,
            bd=0, relief="flat", cursor="hand2",
            command=self._attempt_login
        ).pack(fill="x", pady=(28, 0), ipady=12)

        # Status / error
        self.status = tk.Label(form, text="",
                               bg=self._CARD, fg=self._ERR,
                               font=("Segoe UI", 10))
        self.status.pack(pady=(12, 0), anchor="w")

        self.root.bind("<Return>", lambda e: self._attempt_login())

    def _attempt_login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            self.status.configure(text="Please enter username and password.")
            return

        conn = get_connection()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT username, role FROM users "
                "WHERE username = :uname AND password = :pwd",
                {"uname": username, "pwd": password}
            )
            result = cur.fetchone()

            if result:
                logged_user, logged_role = result
                self.root.destroy()          
                new_root = ctk.CTk()
                EmployeeManagementApp(new_root, logged_user, logged_role)
                new_root.mainloop()
            else:
                self.status.configure(text="Invalid username or password.")
        except oracledb.DatabaseError as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

# ============================================================
#  MAIN EMPLOYEE MANAGEMENT DASHBOARD
# ============================================================
class EmployeeManagementApp:
    def __init__(self, root, username, role):
        self.root     = root
        self.username = username
        self.role     = role          
        self.is_admin = (role == "ADMIN")

        self.root.title("Advanced Employee Management System")
        self.root.geometry("1300x780")
        self.root.configure(fg_color="#080d18")
        self._center_window(1300, 780)

        # Shared palette — mirrors the Login page
        self.C_BG     = "#080d18"
        self.C_SURF   = "#0d1424"
        self.C_CARD   = "#101828"
        self.C_FIELD  = "#141f33"
        self.C_GOLD   = "#c9a227"
        self.C_GOLD_H = "#a8841e"
        self.C_TXT    = "#e8eaf0"
        self.C_MUTED  = "#4a5568"
        self.C_BORDER = "#1e3a5f"

        self.main_font  = ctk.CTkFont(family="Segoe UI", size=13)
        self.bold_font  = ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        self.title_font = ctk.CTkFont(family="Segoe UI", size=15, weight="bold")

        self._style_treeview()
        self._build_ui()
        self._load_all()             

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _style_treeview(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background="#0d1424", foreground="#e8eaf0",
            rowheight=32, fieldbackground="#0d1424",
            borderwidth=0, font=("Segoe UI", 11)
        )
        style.map(
            "Treeview",
            background=[("selected", "#c9a227")],
            foreground=[("selected", "#080d18")]
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 11, "bold"),
            background="#080d18", foreground="#c9a227",
            borderwidth=0, padding=6
        )
        style.map("Treeview.Heading", background=[("active", "#141f33")])

    def _build_ui(self):
        self._build_header()

        content = ctk.CTkFrame(self.root, fg_color=self.C_BG, corner_radius=0)
        content.pack(fill="both", expand=True, padx=16, pady=12)

        self._build_left_panel(content)
        self._build_right_panel(content)
        self._build_statusbar()

    def _build_header(self):
        hdr = tk.Frame(self.root, bg="#0d1424", height=62)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        # Left: gold slash + title
        left_hdr = tk.Frame(hdr, bg="#0d1424")
        left_hdr.pack(side="left", fill="y", padx=(0, 0))

        # Gold vertical accent bar
        tk.Frame(left_hdr, bg=self.C_GOLD, width=4).pack(side="left", fill="y")

        tk.Label(
            left_hdr, text="  Enterprise Employee Portal",
            bg="#0d1424", fg=self.C_TXT,
            font=("Segoe UI", 17, "bold")
        ).pack(side="left", padx=(10, 0), pady=12)

        # Right: user info + logout
        right_hdr = tk.Frame(hdr, bg="#0d1424")
        right_hdr.pack(side="right", fill="y", padx=16)

        logout_btn = tk.Button(
            right_hdr, text="Log Out",
            bg="#b91c1c", fg=self.C_TXT,
            font=("Segoe UI", 10, "bold"),
            activebackground="#991b1b", activeforeground=self.C_TXT,
            bd=0, relief="flat", cursor="hand2",
            command=self._logout
        )
        logout_btn.pack(side="right", padx=(10, 0), pady=16, ipady=4, ipadx=10)

        role_color = self.C_GOLD if self.is_admin else "#94a3b8"
        tk.Label(
            right_hdr,
            text=f"Logged in as: {self.username}   |   Role: {self.role}",
            bg="#0d1424", fg=role_color,
            font=("Segoe UI", 11, "bold")
        ).pack(side="right", pady=12)

        # Bottom gold rule
        tk.Frame(self.root, bg=self.C_GOLD, height=2).pack(fill="x")

    def _build_left_panel(self, parent):
        left = ctk.CTkFrame(parent, fg_color=self.C_BG, width=355)
        left.pack(side="left", fill="y", padx=(0, 14))
        left.pack_propagate(False)

        # ── Employee Details card ──────────────────────────────
        detail_frm = ctk.CTkFrame(left, fg_color=self.C_SURF, corner_radius=10)
        detail_frm.pack(fill="x", pady=(0, 12), ipady=6)

        # Card title with gold left border simulation
        title_row = tk.Frame(detail_frm, bg=self.C_SURF)
        title_row.pack(anchor="w", padx=16, pady=(14, 8), fill="x")
        tk.Frame(title_row, bg=self.C_GOLD, width=3).pack(side="left", fill="y")
        tk.Label(
            title_row, text="  Employee Details",
            bg=self.C_SURF, fg=self.C_TXT,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        fields_frm = ctk.CTkFrame(detail_frm, fg_color="transparent")
        fields_frm.pack(fill="x", padx=16)

        labels = ["Employee ID", "Full Name", "Department", "Salary", "Contact"]
        attrs  = ["eid", "ename", "edept", "esalary", "econtact"]

        for i, (lbl, attr) in enumerate(zip(labels, attrs)):
            ctk.CTkLabel(
                fields_frm, text=lbl, font=self.bold_font,
                text_color=self.C_GOLD
            ).grid(row=i, column=0, sticky="w", pady=6, padx=(0, 10))
            var = tk.StringVar()
            setattr(self, f"{attr}_var", var)
            entry = ctk.CTkEntry(
                fields_frm, textvariable=var, font=self.main_font,
                width=200, height=32, corner_radius=6,
                fg_color=self.C_FIELD, text_color=self.C_TXT,
                border_color=self.C_BORDER, border_width=1
            )
            entry.grid(row=i, column=1, pady=6)
            setattr(self, f"{attr}_entry", entry)

        ctk.CTkLabel(
            fields_frm, text="Gender", font=self.bold_font,
            text_color=self.C_GOLD
        ).grid(row=5, column=0, sticky="w", pady=6, padx=(0, 10))
        self.egender_var = tk.StringVar()
        self.egender_cb  = ctk.CTkComboBox(
            fields_frm, variable=self.egender_var,
            values=["Male", "Female", "Other"],
            font=self.main_font, width=200, height=32, corner_radius=6,
            fg_color=self.C_FIELD, text_color=self.C_TXT,
            button_color=self.C_GOLD, button_hover_color=self.C_GOLD_H,
            border_color=self.C_BORDER, border_width=1, state="readonly"
        )
        self.egender_cb.grid(row=5, column=1, pady=6)

        # ── Smart Filters & Sorting card ──────────────────────
        sf = ctk.CTkFrame(left, fg_color=self.C_SURF, corner_radius=10)
        sf.pack(fill="x", pady=(0, 12), ipady=6)

        title_row2 = tk.Frame(sf, bg=self.C_SURF)
        title_row2.pack(anchor="w", padx=16, pady=(14, 8), fill="x")
        tk.Frame(title_row2, bg=self.C_GOLD, width=3).pack(side="left", fill="y")
        tk.Label(
            title_row2, text="  Smart Filters & Sorting",
            bg=self.C_SURF, fg=self.C_TXT,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        sf_grid = ctk.CTkFrame(sf, fg_color="transparent")
        sf_grid.pack(fill="x", padx=16)

        ctk.CTkLabel(
            sf_grid, text="Min Salary:", font=self.main_font, text_color=self.C_GOLD
        ).grid(row=0, column=0, sticky="w", pady=5)
        self.min_sal_var = tk.StringVar()
        ctk.CTkEntry(
            sf_grid, textvariable=self.min_sal_var, font=self.main_font,
            width=98, height=30, corner_radius=6,
            fg_color=self.C_FIELD, text_color=self.C_TXT,
            border_color=self.C_BORDER, border_width=1
        ).grid(row=0, column=1, pady=5, padx=(5, 14))

        ctk.CTkLabel(
            sf_grid, text="Max Salary:", font=self.main_font, text_color=self.C_GOLD
        ).grid(row=0, column=2, sticky="w", pady=5)
        self.max_sal_var = tk.StringVar()
        ctk.CTkEntry(
            sf_grid, textvariable=self.max_sal_var, font=self.main_font,
            width=98, height=30, corner_radius=6,
            fg_color=self.C_FIELD, text_color=self.C_TXT,
            border_color=self.C_BORDER, border_width=1
        ).grid(row=0, column=3, pady=5, padx=(5, 0))

        self.sort_col_var = tk.StringVar(value="Name")
        self.sort_ord_var = tk.StringVar(value="ASC")

        ctk.CTkLabel(
            sf_grid, text="Sort By:", font=self.main_font, text_color=self.C_GOLD
        ).grid(row=1, column=0, sticky="w", pady=10)
        ctk.CTkComboBox(
            sf_grid, variable=self.sort_col_var,
            values=["ID", "Name", "Salary", "Department"],
            width=98, height=30, state="readonly",
            fg_color=self.C_FIELD, text_color=self.C_TXT,
            button_color=self.C_GOLD, button_hover_color=self.C_GOLD_H,
            border_color=self.C_BORDER, border_width=1
        ).grid(row=1, column=1, padx=(5, 14), pady=10)
        ctk.CTkComboBox(
            sf_grid, variable=self.sort_ord_var,
            values=["ASC", "DESC"],
            width=98, height=30, state="readonly",
            fg_color=self.C_FIELD, text_color=self.C_TXT,
            button_color=self.C_GOLD, button_hover_color=self.C_GOLD_H,
            border_color=self.C_BORDER, border_width=1
        ).grid(row=1, column=2, columnspan=2, sticky="w", padx=5, pady=10)

        self.ename_var.trace_add("write", lambda *_: self._smart_search(False))
        self.edept_var.trace_add("write", lambda *_: self._smart_search(False))

    def _build_right_panel(self, parent):
        right_wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        right_wrapper.pack(side="right", fill="both", expand=True)

        self._build_buttons(right_wrapper)

        tree_card = ctk.CTkFrame(right_wrapper, fg_color=self.C_SURF, corner_radius=10)
        tree_card.pack(fill="both", expand=True)

        cols   = ("ID", "Name", "Department", "Gender", "Salary", "Contact")
        widths = (70, 160, 140, 90, 120, 140)

        tree_frame = tk.Frame(tree_card, bg=self.C_SURF)
        tree_frame.pack(fill="both", expand=True, padx=12, pady=12)

        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=26)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col, command=lambda c=col: self._header_sort(c))
            self.tree.column(col, width=w, anchor="center")

        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Row highlighting — dark tinted (high salary = dark green, low = dark red)
        self.tree.tag_configure("high",   background="#0f2d1a", foreground="#6ee7a0")
        self.tree.tag_configure("low",    background="#2d0f0f", foreground="#fca5a5")
        self.tree.tag_configure("normal", background="#0d1424", foreground="#e8eaf0")

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

        self._hdr_sort_col   = None
        self._hdr_sort_order = "ASC"

    def _build_buttons(self, parent):
        btn_frm = ctk.CTkFrame(parent, fg_color=self.C_SURF, corner_radius=10)
        btn_frm.pack(fill="x", pady=(0, 12), ipady=6)

        title_row = tk.Frame(btn_frm, bg=self.C_SURF)
        title_row.pack(anchor="w", padx=16, pady=(12, 6), fill="x")
        tk.Frame(title_row, bg=self.C_GOLD, width=3).pack(side="left", fill="y")
        tk.Label(
            title_row, text="  Quick Actions",
            bg=self.C_SURF, fg=self.C_TXT,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        grid_frm = ctk.CTkFrame(btn_frm, fg_color="transparent")
        grid_frm.pack(anchor="center", pady=(0, 10))

        # (label, command, active_color, hover_color, text_color, admin_only)
        buttons = [
            ("Insert",       self._insert,          "#15803d", "#166534", self.C_TXT,  True),
            ("Update",       self._update,          "#1d4ed8", "#1e3a8a", self.C_TXT,  True),
            ("Delete",       self._delete,          "#b91c1c", "#991b1b", self.C_TXT,  True),
            ("Search",       self._smart_search,    "#5b21b6", "#4c1d95", self.C_TXT,  False),
            ("Show All",     self._load_all,        "#0369a1", "#075985", self.C_TXT,  False),
            ("Statistics",   self._show_statistics, self.C_GOLD, self.C_GOLD_H, "#080d18", False),
            ("Export CSV",   self._export_csv,      "#334155", "#1e293b", self.C_TXT,  True),
            ("Export TXT",   self._export_txt,      "#334155", "#1e293b", self.C_TXT,  True),
            ("Clear",        self._clear_form,      "#374151", "#1f2937", "#94a3b8",   False),
            ("Manage Users", self._manage_users,    "#0d1424", "#0a0f1c", self.C_GOLD, True),
        ]

        for i, (text, cmd, color, hover, txt_col, admin_only) in enumerate(buttons):
            state = "normal" if (not admin_only or self.is_admin) else "disabled"
            ctk.CTkButton(
                grid_frm, text=text, command=cmd,
                font=self.bold_font,
                text_color=txt_col if state == "normal" else "#4a5568",
                fg_color=color if state == "normal" else "#141f33",
                hover_color=hover if state == "normal" else "#141f33",
                border_color=self.C_BORDER if state == "disabled" else color,
                border_width=1 if state == "disabled" else 0,
                width=138, height=36, corner_radius=7,
                cursor="hand2" if state == "normal" else "arrow",
                state=state
            ).grid(row=i // 5, column=i % 5, padx=7, pady=5)

    def _build_statusbar(self):
        # Gold rule above status bar
        tk.Frame(self.root, bg=self.C_GOLD, height=1).pack(fill="x", side="bottom")

        status_frm = tk.Frame(self.root, bg="#0d1424", height=36)
        status_frm.pack(fill="x", side="bottom")
        status_frm.pack_propagate(False)

        # Left accent bar
        tk.Frame(status_frm, bg=self.C_GOLD, width=4).pack(side="left", fill="y")

        self.status_var = tk.StringVar(value="System Ready")
        tk.Label(
            status_frm, textvariable=self.status_var,
            bg="#0d1424", fg="#6ee7a0",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(side="left", padx=12, pady=8)

    # ─────────────────────────────────────────────────────────
    #  LOGOUT & USER MANAGEMENT
    # ─────────────────────────────────────────────────────────
    def _logout(self):
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            self.root.destroy()  
            new_root = ctk.CTk()
            LoginWindow(new_root)
            new_root.mainloop()

    def _manage_users(self):
        win = ctk.CTkToplevel(self.root)
        win.title("User Access Management")
        win.geometry("460x660")
        win.configure(fg_color=self.C_BG)
        win.attributes("-topmost", True)

        # ── CREATE USER SECTION ──────────────────────────────
        title_row = tk.Frame(win, bg=self.C_BG)
        title_row.pack(anchor="w", padx=24, pady=(20, 10), fill="x")
        tk.Frame(title_row, bg=self.C_GOLD, width=3).pack(side="left", fill="y")
        tk.Label(
            title_row, text="  Create New User",
            bg=self.C_BG, fg=self.C_TXT,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        create_card = ctk.CTkFrame(win, fg_color=self.C_SURF, corner_radius=10)
        create_card.pack(fill="x", padx=20, pady=(0, 20), ipady=6)

        new_uname = tk.StringVar()
        new_pwd   = tk.StringVar()
        new_role  = tk.StringVar(value="USER")

        for lbl, var, masked in [
            ("New Username", new_uname, False),
            ("New Password", new_pwd,   True),
        ]:
            ctk.CTkLabel(
                create_card, text=lbl, font=self.bold_font, text_color=self.C_GOLD
            ).pack(anchor="w", padx=24, pady=(10, 0))
            ctk.CTkEntry(
                create_card, textvariable=var, width=280,
                show="*" if masked else "",
                fg_color=self.C_FIELD, text_color=self.C_TXT,
                border_color=self.C_BORDER, border_width=1, corner_radius=6
            ).pack(pady=(4, 0))

        ctk.CTkLabel(
            create_card, text="Assign Role", font=self.bold_font, text_color=self.C_GOLD
        ).pack(anchor="w", padx=24, pady=(10, 0))
        ctk.CTkComboBox(
            create_card, variable=new_role, values=["ADMIN", "USER"],
            width=280, state="readonly",
            fg_color=self.C_FIELD, text_color=self.C_TXT,
            button_color=self.C_GOLD, button_hover_color=self.C_GOLD_H,
            border_color=self.C_BORDER, border_width=1, corner_radius=6
        ).pack(pady=(4, 0))

        def save_user():
            u = new_uname.get().strip()
            p = new_pwd.get().strip()
            r = new_role.get()

            if not u or not p:
                messagebox.showwarning("Incomplete", "Username and Password are required.", parent=win)
                return

            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM users WHERE username = :u", {"u": u})
                if cur.fetchone()[0] > 0:
                    messagebox.showerror("Error", "Username already exists!", parent=win)
                    return
                cur.execute("INSERT INTO users (username, password, role) VALUES (:u, :p, :r)", {"u": u, "p": p, "r": r})
                conn.commit()
                messagebox.showinfo("Success", f"User '{u}' created successfully as {r}!", parent=win)
                new_uname.set("")
                new_pwd.set("")
                refresh_user_list()  # Update the dropdown for deletion
            except oracledb.DatabaseError as e:
                conn.rollback()
                messagebox.showerror("DB Error", str(e), parent=win)
            finally:
                conn.close()

        ctk.CTkButton(
            create_card, text="Save User", font=self.bold_font,
            fg_color="#15803d", hover_color="#166534", text_color=self.C_TXT,
            corner_radius=7, command=save_user
        ).pack(pady=(12, 18))

        # ── REMOVE USER SECTION ─────────────────────────────
        title_row2 = tk.Frame(win, bg=self.C_BG)
        title_row2.pack(anchor="w", padx=24, pady=(0, 10), fill="x")
        tk.Frame(title_row2, bg=self.C_GOLD, width=3).pack(side="left", fill="y")
        tk.Label(
            title_row2, text="  Remove User",
            bg=self.C_BG, fg=self.C_TXT,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        delete_card = ctk.CTkFrame(win, fg_color=self.C_SURF, corner_radius=10)
        delete_card.pack(fill="x", padx=20, pady=(0, 20), ipady=6)

        del_uname = tk.StringVar()

        ctk.CTkLabel(
            delete_card, text="Select User to Remove", font=self.bold_font, text_color=self.C_GOLD
        ).pack(anchor="w", padx=24, pady=(12, 0))
        user_cb = ctk.CTkComboBox(
            delete_card, variable=del_uname, width=280, state="readonly",
            fg_color=self.C_FIELD, text_color=self.C_TXT,
            button_color=self.C_GOLD, button_hover_color=self.C_GOLD_H,
            border_color=self.C_BORDER, border_width=1, corner_radius=6
        )
        user_cb.pack(pady=(4, 0))

        def refresh_user_list():
            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                # Crucial UI Protection: Only fetch non-admin users
                cur.execute("SELECT username FROM users WHERE role = 'USER'")
                users = [row[0] for row in cur.fetchall()]
                user_cb.configure(values=users if users else ["No users found"])
                del_uname.set("Select User" if users else "No users found")
            except oracledb.DatabaseError as e:
                messagebox.showerror("DB Error", str(e), parent=win)
            finally:
                conn.close()

        def delete_user():
            u = del_uname.get()
            if not u or u in ["Select User", "No users found"]:
                messagebox.showwarning("Selection Error", "Please select a valid user to remove.", parent=win)
                return
            
            if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently remove '{u}'?", parent=win):
                return

            conn = get_connection()
            if not conn: return
            try:
                cur = conn.cursor()
                
                # Crucial Backend Protection: Double-check the role is not ADMIN
                cur.execute("SELECT role FROM users WHERE username = :u", {"u": u})
                res = cur.fetchone()
                if not res:
                    messagebox.showerror("Error", "User not found in database.", parent=win)
                    return
                if res[0] == 'ADMIN':
                    messagebox.showerror("Permission Denied", "Security Violation: You cannot remove an ADMIN account.", parent=win)
                    return

                cur.execute("DELETE FROM users WHERE username = :u", {"u": u})
                conn.commit()
                messagebox.showinfo("Success", f"User '{u}' removed successfully.", parent=win)
                refresh_user_list()
            except oracledb.DatabaseError as e:
                conn.rollback()
                messagebox.showerror("DB Error", str(e), parent=win)
            finally:
                conn.close()

        ctk.CTkButton(
            delete_card, text="Delete User", font=self.bold_font,
            fg_color="#b91c1c", hover_color="#991b1b", text_color=self.C_TXT,
            corner_radius=7, command=delete_user
        ).pack(pady=(12, 18))

        # Initialize the dropdown menu
        refresh_user_list()


    # ─────────────────────────────────────────────────────────
    #  HELPERS
    # ─────────────────────────────────────────────────────────
    def _set_status(self, msg, color="#059669"):
        self.status_var.set(msg)
        self.root.after(5000, lambda: self.status_var.set("System Ready"))

    def _clear_form(self):
        for attr in ["eid", "ename", "edept", "esalary", "econtact", "min_sal", "max_sal"]:
            getattr(self, f"{attr}_var").set("")
        self.egender_var.set("")

    def _on_row_select(self, _event):
        sel = self.tree.focus()
        if not sel: return
        v = self.tree.item(sel, "values")
        self.eid_var.set(v[0])
        self.ename_var.set(v[1])
        self.edept_var.set(v[2])
        self.egender_var.set(v[3])
        self.esalary_var.set(v[4])
        self.econtact_var.set(v[5])

    def _populate_tree(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in rows:
            try:
                sal = float(row[4])
            except (TypeError, ValueError):
                sal = 0
            tag = "high" if sal >= 80000 else ("low" if sal <= 30000 else "normal")
            self.tree.insert("", "end", values=row, tags=(tag,))

    def _get_sort_clause(self):
        col_map = {
            "ID": "empid",
            "Name": "name",
            "Salary": "salary",
            "Department": "department"
        }
        col = col_map.get(self.sort_col_var.get(), "name")
        order = self.sort_ord_var.get()
        return f"ORDER BY {col} {order}"

    def _header_sort(self, col):
        if self._hdr_sort_col == col:
            self._hdr_sort_order = "DESC" if self._hdr_sort_order == "ASC" else "ASC"
        else:
            self._hdr_sort_col   = col
            self._hdr_sort_order = "ASC"

        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            col_map = {
                "ID": "empid", "Name": "name", "Department": "department",
                "Gender": "gender", "Salary": "salary", "Contact": "contact",
            }
            sort_column = col_map.get(col, "name")
            cur.execute(
                f"SELECT empid, name, department, gender, salary, contact FROM employees "
                f"ORDER BY {sort_column} {self._hdr_sort_order}"
            )
            self._populate_tree(cur.fetchall())
        except oracledb.DatabaseError as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    # ─────────────────────────────────────────────────────────
    #  VALIDATION
    # ─────────────────────────────────────────────────────────
    def _validate(self, full=True):
        eid     = self.eid_var.get().strip()
        name    = self.ename_var.get().strip()
        salary  = self.esalary_var.get().strip()
        contact = self.econtact_var.get().strip()

        if not eid or not eid.isdigit():
            messagebox.showerror("Validation", "Employee ID must be a positive integer.")
            return False

        if full:
            if not name or not re.fullmatch(r"[A-Za-z\s]+", name):
                messagebox.showerror("Validation", "Name must contain letters only and is required.")
                return False
            if not salary or not re.fullmatch(r"\d+(\.\d+)?", salary) or float(salary) < 0:
                messagebox.showerror("Validation", "Salary must be a non-negative number.")
                return False
            if contact and (not contact.isdigit() or not (10 <= len(contact) <= 15)):
                messagebox.showerror("Validation", "Contact must be numeric with 10–15 digits.")
                return False
        return True

    # ─────────────────────────────────────────────────────────
    #  CRUD OPERATIONS
    # ─────────────────────────────────────────────────────────
    def _insert(self):
        if not self._validate(full=True): return

        eid     = int(self.eid_var.get().strip())
        name    = self.ename_var.get().strip()
        dept    = self.edept_var.get().strip()
        gender  = self.egender_var.get()
        salary  = float(self.esalary_var.get().strip())
        contact = self.econtact_var.get().strip() or None

        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM employees WHERE empid = :eid", {"eid": eid})
            if cur.fetchone()[0] > 0:
                messagebox.showerror("Duplicate", "Employee ID already exists.")
                return

            if contact:
                cur.execute("SELECT COUNT(*) FROM employees WHERE contact = :c", {"c": contact})
                if cur.fetchone()[0] > 0:
                    messagebox.showerror("Duplicate", "Contact number already registered.")
                    return

            cur.execute(
                "INSERT INTO employees (empid, name, department, gender, salary, contact) "
                "VALUES (:eid, :name, :dept, :gender, :salary, :contact)",
                {"eid": eid, "name": name, "dept": dept, "gender": gender, "salary": salary, "contact": contact}
            )
            conn.commit()
            self._set_status(f"Employee '{name}' inserted successfully.")
            self._clear_form()
            self._load_all()
        except oracledb.DatabaseError as e:
            conn.rollback()
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    def _update(self):
        if not self._validate(full=True): return

        eid     = int(self.eid_var.get().strip())
        name    = self.ename_var.get().strip()
        dept    = self.edept_var.get().strip()
        gender  = self.egender_var.get()
        salary  = float(self.esalary_var.get().strip())
        contact = self.econtact_var.get().strip() or None

        sel = self.tree.focus()
        if sel:
            old = self.tree.item(sel, "values")
            try:
                old_sal = float(old[4])
            except ValueError:
                old_sal = -1
            if (old[1] == name and old[2] == dept and old[3] == gender and old_sal == salary and (old[5] == (contact or ""))):
                messagebox.showinfo("No Changes", "No changes detected.")
                return

        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE employees SET name=:name, department=:dept, gender=:gender, salary=:salary, contact=:contact WHERE empid=:eid",
                {"name": name, "dept": dept, "gender": gender, "salary": salary, "contact": contact, "eid": eid}
            )
            if cur.rowcount == 0:
                messagebox.showwarning("Not Found", f"No employee found with ID {eid}.")
            else:
                conn.commit()
                self._set_status(f"Employee {eid} updated successfully.")
                self._load_all()
        except oracledb.DatabaseError as e:
            conn.rollback()
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    def _delete(self):
        eid = self.eid_var.get().strip()
        if not eid or not eid.isdigit():
            messagebox.showerror("Error", "Select a row or enter a valid Employee ID.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Permanently delete Employee ID {eid}?"): return

        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM employees WHERE empid = :eid", {"eid": int(eid)})
            if cur.rowcount == 0:
                messagebox.showwarning("Not Found", f"No employee with ID {eid}.")
            else:
                conn.commit()
                self._set_status(f"Employee {eid} deleted.")
                self._clear_form()
                self._load_all()
        except oracledb.DatabaseError as e:
            conn.rollback()
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    # ─────────────────────────────────────────────────────────
    #  SMART DYNAMIC SEARCH
    # ─────────────────────────────────────────────────────────
    def _smart_search(self, show_errors=True):
        eid = self.eid_var.get().strip()
        name = self.ename_var.get().strip()
        dept = self.edept_var.get().strip()
        gender = self.egender_var.get()
        min_sal = self.min_sal_var.get().strip()
        max_sal = self.max_sal_var.get().strip()

        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            query = "SELECT empid, name, department, gender, salary, contact FROM employees WHERE 1=1"
            params = {}

            # --- ALL FILTERS COMBINED ---
            if eid:
                query += " AND empid = :eid"
                params["eid"] = int(eid)
            if name:
                query += " AND UPPER(name) LIKE UPPER(:name)"
                params["name"] = f"%{name}%"
            if dept:
                query += " AND UPPER(department) LIKE UPPER(:dept)"
                params["dept"] = f"%{dept}%"
            if gender:
                query += " AND gender = :gender"
                params["gender"] = gender
            if min_sal:
                query += " AND salary >= :minsal"
                params["minsal"] = float(min_sal)
            if max_sal:
                query += " AND salary <= :maxsal"
                params["maxsal"] = float(max_sal)

            query += " " + self._get_sort_clause()
            cur.execute(query, params)
            rows = cur.fetchall()
            self._populate_tree(rows)
            self._set_status(f"{len(rows)} record(s) found.")
        except Exception as e:
            if show_errors: messagebox.showerror("Search Error", str(e))
        finally:
            conn.close()

    def _load_all(self):
        conn = get_connection()
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute(f"SELECT empid, name, department, gender, salary, contact FROM employees {self._get_sort_clause()}")
            rows = cur.fetchall()
            self._populate_tree(rows)
            self._set_status(f"{len(rows)} employee(s) loaded.")
        except oracledb.DatabaseError as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            conn.close()

    # ─────────────────────────────────────────────────────────
    #  STATISTICS MODULE
    # ─────────────────────────────────────────────────────────
    def _show_statistics(self):
        conn = get_connection()
        if not conn:
            return
        try:
            cur = conn.cursor()

            # Salary overview
            cur.execute(
                "SELECT MAX(salary), MIN(salary), AVG(salary), SUM(salary) FROM employees"
            )
            max_s, min_s, avg_s, sum_s = cur.fetchone()

            # Department headcount
            cur.execute(
                "SELECT department, COUNT(*) FROM employees "
                "GROUP BY department ORDER BY department"
            )
            dept_rows = cur.fetchall()

            # Average salary per department
            cur.execute(
                "SELECT department, AVG(salary) FROM employees "
                "GROUP BY department ORDER BY AVG(salary) DESC"
            )
            dept_avg_rows = cur.fetchall()

            # Gender distribution
            cur.execute(
                "SELECT gender, COUNT(*) FROM employees GROUP BY gender"
            )
            gender_rows = cur.fetchall()

            # Top 5 earners
            cur.execute(
                "SELECT name, salary FROM employees "
                "ORDER BY salary DESC FETCH FIRST 5 ROWS ONLY"
            )
            top5_rows = cur.fetchall()

            # Salary bands
            cur.execute(
                "SELECT "
                "  SUM(CASE WHEN salary < 100000 THEN 1 ELSE 0 END), "
                "  SUM(CASE WHEN salary BETWEEN 100000 AND 200000 THEN 1 ELSE 0 END), "
                "  SUM(CASE WHEN salary BETWEEN 200001 AND 300000 THEN 1 ELSE 0 END), "
                "  SUM(CASE WHEN salary > 300000 THEN 1 ELSE 0 END) "
                "FROM employees"
            )
            bands = cur.fetchone()

        except oracledb.DatabaseError as e:
            messagebox.showerror("DB Error", str(e))
            return
        finally:
            conn.close()

        # ── Window setup ──────────────────────────────────────
        win = ctk.CTkToplevel(self.root)
        win.title("Analytics Dashboard")
        win.geometry("1060x760")
        win.configure(fg_color=self.C_BG)
        win.attributes("-topmost", True)
        win.resizable(True, True)

        # Scrollable canvas so nothing gets cut off
        outer_canvas = tk.Canvas(win, bg=self.C_BG, highlightthickness=0)
        scrollbar    = ttk.Scrollbar(win, orient="vertical",
                                     command=outer_canvas.yview)
        outer_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        outer_canvas.pack(side="left", fill="both", expand=True)

        scroll_frame = tk.Frame(outer_canvas, bg=self.C_BG)
        scroll_win   = outer_canvas.create_window((0, 0), window=scroll_frame,
                                                  anchor="nw")

        def _on_resize(event):
            outer_canvas.itemconfig(scroll_win, width=event.width)
        def _on_frame_configure(event):
            outer_canvas.configure(scrollregion=outer_canvas.bbox("all"))

        outer_canvas.bind("<Configure>", _on_resize)
        scroll_frame.bind("<Configure>", _on_frame_configure)
        win.bind("<MouseWheel>",
                 lambda e: outer_canvas.yview_scroll(-1*(e.delta//120), "units"))

        # ── Shared chart style helpers ────────────────────────
        BG   = self.C_BG
        SURF = self.C_SURF
        GOLD = self.C_GOLD
        TXT  = self.C_TXT
        MUTED = self.C_MUTED

        def style_ax(ax, fig):
            fig.patch.set_facecolor(SURF)
            ax.set_facecolor(BG)
            ax.tick_params(colors=TXT, labelsize=9)
            for spine in ax.spines.values():
                spine.set_color("#1e3a5f")
            ax.xaxis.label.set_color(MUTED)
            ax.yaxis.label.set_color(MUTED)
            ax.title.set_color(TXT)

        def section_title(parent, text):
            row = tk.Frame(parent, bg=BG)
            row.pack(anchor="w", padx=24, pady=(18, 8), fill="x")
            tk.Frame(row, bg=GOLD, width=3).pack(side="left", fill="y")
            tk.Label(row, text=f"  {text}", bg=BG, fg=TXT,
                     font=("Segoe UI", 13, "bold")).pack(side="left")

        def embed_chart(parent, fig):
            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="x", padx=24, pady=(0, 6))

        def fmt(val):
            return f"PKR {val:,.0f}" if val is not None else "N/A"

        # ══ SECTION 1 — Salary Overview cards ════════════════
        section_title(scroll_frame, "Salary Overview")

        cards_row = tk.Frame(scroll_frame, bg=BG)
        cards_row.pack(fill="x", padx=24, pady=(0, 4))

        stat_items = [
            ("Highest Salary", fmt(max_s), "#15803d"),
            ("Lowest Salary",  fmt(min_s), "#b91c1c"),
            ("Average Salary", fmt(avg_s), GOLD),
            ("Total Expense",  fmt(sum_s), "#0369a1"),
        ]
        for label, value, accent in stat_items:
            card = tk.Frame(cards_row, bg=SURF)
            card.pack(side="left", expand=True, fill="x", padx=(0, 10), ipady=10, ipadx=10)
            tk.Frame(card, bg=accent, height=3).pack(fill="x")
            tk.Label(card, text=label, bg=SURF, fg=MUTED,
                     font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(8, 2))
            tk.Label(card, text=value, bg=SURF, fg=accent,
                     font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=12, pady=(0, 8))

        # ══ SECTION 2 — Two charts side by side ══════════════
        section_title(scroll_frame, "Department Analytics")

        row2 = tk.Frame(scroll_frame, bg=BG)
        row2.pack(fill="x", padx=24, pady=(0, 6))

        # Chart A — Pie: Department headcount
        dept_names  = [r[0] or "N/A" for r in dept_rows]
        dept_counts = [r[1] for r in dept_rows]

        PALETTE = ["#c9a227", "#15803d", "#0369a1", "#7c3aed",
                   "#b91c1c", "#0891b2", "#92400e", "#065f46",
                   "#4338ca", "#be185d"]

        fig_pie = Figure(figsize=(4.6, 3.4), dpi=96)
        ax_pie  = fig_pie.add_subplot(111)
        wedges, texts, autotexts = ax_pie.pie(
            dept_counts,
            labels=None,
            autopct="%1.0f%%",
            startangle=140,
            colors=PALETTE[:len(dept_names)],
            pctdistance=0.75,
            wedgeprops={"linewidth": 1.5, "edgecolor": SURF}
        )
        for at in autotexts:
            at.set_color(BG)
            at.set_fontsize(8)
            at.set_fontweight("bold")
        ax_pie.set_title("Headcount by Department", fontsize=10, pad=10)
        ax_pie.legend(wedges, dept_names, loc="lower center",
                      bbox_to_anchor=(0.5, -0.22), ncol=3,
                      fontsize=7, framealpha=0,
                      labelcolor=TXT)
        style_ax(ax_pie, fig_pie)
        fig_pie.tight_layout()

        pie_frame = tk.Frame(row2, bg=SURF)
        pie_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))
        c1 = FigureCanvasTkAgg(fig_pie, master=pie_frame)
        c1.draw()
        c1.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)

        # Chart B — Horizontal bar: Avg salary per department
        avg_depts   = [r[0] or "N/A" for r in dept_avg_rows]
        avg_salaries = [float(r[1]) for r in dept_avg_rows]

        fig_avg = Figure(figsize=(4.6, 3.4), dpi=96)
        ax_avg  = fig_avg.add_subplot(111)
        bars = ax_avg.barh(avg_depts, avg_salaries,
                           color=PALETTE[:len(avg_depts)],
                           edgecolor=SURF, linewidth=0.8)
        ax_avg.set_xlabel("Avg Salary (PKR)", fontsize=8)
        ax_avg.set_title("Avg Salary by Department", fontsize=10, pad=10)
        ax_avg.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K")
        )
        ax_avg.tick_params(axis="y", labelsize=8)
        ax_avg.tick_params(axis="x", labelsize=8)
        ax_avg.grid(axis="x", color="#1e3a5f", linewidth=0.5, linestyle="--")
        ax_avg.set_axisbelow(True)
        # Value labels on bars
        for bar, val in zip(bars, avg_salaries):
            ax_avg.text(bar.get_width() + max(avg_salaries) * 0.01,
                        bar.get_y() + bar.get_height() / 2,
                        f"{val/1000:.0f}K",
                        va="center", ha="left",
                        color=GOLD, fontsize=7, fontweight="bold")
        style_ax(ax_avg, fig_avg)
        fig_avg.tight_layout()

        avg_frame = tk.Frame(row2, bg=SURF)
        avg_frame.pack(side="right", fill="both", expand=True)
        c2 = FigureCanvasTkAgg(fig_avg, master=avg_frame)
        c2.draw()
        c2.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)

        # ══ SECTION 3 — Two more charts ═══════════════════════
        section_title(scroll_frame, "Workforce & Salary Distribution")

        row3 = tk.Frame(scroll_frame, bg=BG)
        row3.pack(fill="x", padx=24, pady=(0, 6))

        # Chart C — Bar: Gender distribution
        genders = [r[0] or "N/A" for r in gender_rows]
        g_counts = [r[1] for r in gender_rows]
        g_colors = {"Male": "#0369a1", "Female": "#be185d", "Other": GOLD}
        bar_colors = [g_colors.get(g, GOLD) for g in genders]

        fig_gen = Figure(figsize=(4.6, 3.2), dpi=96)
        ax_gen  = fig_gen.add_subplot(111)
        b = ax_gen.bar(genders, g_counts, color=bar_colors,
                       edgecolor=SURF, linewidth=0.8, width=0.4)
        ax_gen.set_title("Gender Distribution", fontsize=10, pad=10)
        ax_gen.set_ylabel("Employees", fontsize=8)
        ax_gen.grid(axis="y", color="#1e3a5f", linewidth=0.5, linestyle="--")
        ax_gen.set_axisbelow(True)
        ax_gen.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        for bar, val in zip(b, g_counts):
            ax_gen.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.1,
                        str(val), ha="center", va="bottom",
                        color=TXT, fontsize=9, fontweight="bold")
        style_ax(ax_gen, fig_gen)
        fig_gen.tight_layout()

        gen_frame = tk.Frame(row3, bg=SURF)
        gen_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))
        c3 = FigureCanvasTkAgg(fig_gen, master=gen_frame)
        c3.draw()
        c3.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)

        # Chart D — Horizontal bar: Salary bands
        band_labels = ["< 100K", "100K – 200K", "200K – 300K", "> 300K"]
        band_vals   = [int(v or 0) for v in bands]
        band_colors = ["#b91c1c", GOLD, "#0369a1", "#15803d"]

        fig_band = Figure(figsize=(4.6, 3.2), dpi=96)
        ax_band  = fig_band.add_subplot(111)
        brs = ax_band.barh(band_labels, band_vals,
                           color=band_colors, edgecolor=SURF,
                           linewidth=0.8)
        ax_band.set_title("Salary Band Distribution", fontsize=10, pad=10)
        ax_band.set_xlabel("No. of Employees", fontsize=8)
        ax_band.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
        ax_band.grid(axis="x", color="#1e3a5f", linewidth=0.5, linestyle="--")
        ax_band.set_axisbelow(True)
        for bar, val in zip(brs, band_vals):
            ax_band.text(bar.get_width() + 0.05,
                         bar.get_y() + bar.get_height() / 2,
                         str(val), va="center", ha="left",
                         color=TXT, fontsize=9, fontweight="bold")
        style_ax(ax_band, fig_band)
        fig_band.tight_layout()

        band_frame = tk.Frame(row3, bg=SURF)
        band_frame.pack(side="right", fill="both", expand=True)
        c4 = FigureCanvasTkAgg(fig_band, master=band_frame)
        c4.draw()
        c4.get_tk_widget().pack(fill="both", expand=True, padx=4, pady=4)

        # ══ SECTION 4 — Top 5 Earners ═════════════════════════
        section_title(scroll_frame, "Top 5 Earners")

        top_frame = tk.Frame(scroll_frame, bg=SURF)
        top_frame.pack(fill="x", padx=24, pady=(0, 24))

        # Header row
        hdr = tk.Frame(top_frame, bg="#080d18")
        hdr.pack(fill="x")
        for txt, w in [("Rank", 60), ("Name", 280), ("Salary", 200)]:
            tk.Label(hdr, text=txt, bg="#080d18", fg=GOLD,
                     font=("Segoe UI", 10, "bold"),
                     width=w // 8, anchor="w").pack(side="left", padx=14, pady=8)

        for rank, (name, sal) in enumerate(top5_rows, 1):
            row_bg = SURF if rank % 2 == 0 else "#0a1220"
            row = tk.Frame(top_frame, bg=row_bg)
            row.pack(fill="x")
            rank_color = [GOLD, "#94a3b8", "#92400e", TXT, TXT][rank - 1]
            tk.Label(row, text=f"#{rank}", bg=row_bg, fg=rank_color,
                     font=("Segoe UI", 10, "bold"),
                     width=6, anchor="w").pack(side="left", padx=14, pady=7)
            tk.Label(row, text=name, bg=row_bg, fg=TXT,
                     font=("Segoe UI", 10),
                     width=28, anchor="w").pack(side="left", padx=4, pady=7)
            tk.Label(row, text=f"PKR {float(sal):,.0f}", bg=row_bg, fg=GOLD,
                     font=("Segoe UI", 10, "bold"),
                     anchor="w").pack(side="left", padx=4, pady=7)

    # ─────────────────────────────────────────────────────────
    #  EXPORT
    # ─────────────────────────────────────────────────────────
    def _get_tree_rows(self):
        headers = ["ID", "Name", "Department", "Gender", "Salary", "Contact"]
        rows = [self.tree.item(i, "values") for i in self.tree.get_children()]
        return headers, rows

    def _export_csv(self):
        headers, rows = self._get_tree_rows()
        if not rows:
            messagebox.showwarning("Empty", "No data to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if path:
            with open(path, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(headers)
                csv.writer(f).writerows(rows)
            self._set_status(f"Exported CSV: {path}")

    def _export_txt(self):
        headers, rows = self._get_tree_rows()
        if not rows:
            messagebox.showwarning("Empty", "No data to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\t".join(headers) + "\n" + "─" * 80 + "\n")
                for row in rows: f.write("\t".join(str(v) for v in row) + "\n")
            self._set_status(f"Exported TXT: {path}")

# ============================================================
#  ENTRY POINT
# ============================================================
if __name__ == "__main__":
    root = ctk.CTk()
    LoginWindow(root)
    root.mainloop()