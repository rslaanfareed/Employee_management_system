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

# Set modern UI theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# ============================================================
# DATABASE CONFIGURATION 
# ============================================================
DB_USER     = " "                   #your username
DB_PASSWORD = " "                   #your password
DB_DSN      = " "                   #your dsn (e.g., "localhost/orclpdb1")


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
    def __init__(self, root):
        self.root = root
        self.root.title("System Login")
        self.root.geometry("400x450")
        self.root.resizable(False, False)
        self._center_window(400, 450)
        self._build_ui()

    def _center_window(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build_ui(self):
        bg_frame = ctk.CTkFrame(self.root, fg_color="#F0F2F5", corner_radius=0)
        bg_frame.pack(fill="both", expand=True)

        card = ctk.CTkFrame(bg_frame, fg_color="white", corner_radius=15, width=320, height=380)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(
            card, text="Welcome Back",
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#1f2937"
        ).pack(pady=(30, 5))
        
        ctk.CTkLabel(
            card, text="Sign in to continue",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#6b7280"
        ).pack(pady=(0, 20))

        # Username Label and Entry
        ctk.CTkLabel(
            card, text="Username", 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), 
            text_color="#4b5563"
        ).pack(anchor="w", padx=30)
        
        self.username_var = tk.StringVar()
        ctk.CTkEntry(
            card, textvariable=self.username_var,
            font=ctk.CTkFont(family="Segoe UI", size=13),
            width=260, height=40, corner_radius=8, border_width=1
        ).pack(pady=(2, 10))

        # Password Label and Entry
        ctk.CTkLabel(
            card, text="Password", 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), 
            text_color="#4b5563"
        ).pack(anchor="w", padx=30)
        
        self.password_var = tk.StringVar()
        ctk.CTkEntry(
            card, textvariable=self.password_var, show="*",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            width=260, height=40, corner_radius=8, border_width=1
        ).pack(pady=(2, 20))

        ctk.CTkButton(
            card, text="LOGIN", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            width=260, height=40, corner_radius=8, cursor="hand2",
            fg_color="#3b82f6", hover_color="#2563eb",
            command=self._attempt_login
        ).pack(pady=10)

        self.status = ctk.CTkLabel(card, text="", text_color="#ef4444", font=ctk.CTkFont(size=12))
        self.status.pack()

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
        self.root.configure(bg="#F0F2F5")
        self._center_window(1300, 780)

        self.main_font = ctk.CTkFont(family="Segoe UI", size=13)
        self.bold_font = ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        self.title_font = ctk.CTkFont(family="Segoe UI", size=18, weight="bold")

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
            background="#ffffff", foreground="#1f2937", 
            rowheight=35, fieldbackground="#ffffff", 
            borderwidth=0, font=("Segoe UI", 11)
        )
        style.map("Treeview", background=[("selected", "#3b82f6")], foreground=[("selected", "white")])
        style.configure(
            "Treeview.Heading", font=("Segoe UI", 12, "bold"), 
            background="#f3f4f6", foreground="#374151", borderwidth=0, padding=5
        )

    def _build_ui(self):
        self._build_header()

        content = ctk.CTkFrame(self.root, fg_color="#F0F2F5", corner_radius=0)
        content.pack(fill="both", expand=True, padx=20, pady=15)

        self._build_left_panel(content)
        self._build_right_panel(content)
        self._build_statusbar()

    def _build_header(self):
        hdr = ctk.CTkFrame(self.root, height=65, fg_color="#1f2937", corner_radius=0)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        ctk.CTkLabel(
            hdr, text="Enterprise Employee Portal",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"), 
            text_color="white"
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            hdr, text="Log Out", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="#ef4444", hover_color="#dc2626", width=80, height=30,
            command=self._logout
        ).pack(side="right", padx=(10, 20))

        role_color = "#10b981" if self.is_admin else "#f59e0b"
        ctk.CTkLabel(
            hdr,
            text=f"Logged in as: {self.username}  |  Role: {self.role}  ",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
            text_color=role_color
        ).pack(side="right")

    def _build_left_panel(self, parent):
        left = ctk.CTkFrame(parent, fg_color="#F0F2F5", width=360)
        left.pack(side="left", fill="y", padx=(0, 20))
        left.pack_propagate(False)

        detail_frm = ctk.CTkFrame(left, fg_color="white", corner_radius=12)
        detail_frm.pack(fill="x", pady=(0, 15), ipady=10)

        ctk.CTkLabel(detail_frm, text="Employee Details", font=self.title_font, text_color="#111827").pack(anchor="w", padx=20, pady=(15, 10))

        fields_frm = ctk.CTkFrame(detail_frm, fg_color="transparent")
        fields_frm.pack(fill="x", padx=20)

        labels = ["Employee ID", "Full Name", "Department", "Salary", "Contact"]
        attrs  = ["eid", "ename", "edept", "esalary", "econtact"]

        for i, (lbl, attr) in enumerate(zip(labels, attrs)):
            ctk.CTkLabel(fields_frm, text=lbl, font=self.bold_font, text_color="#4b5563").grid(row=i, column=0, sticky="w", pady=8, padx=(0,10))
            var = tk.StringVar()
            setattr(self, f"{attr}_var", var)
            entry = ctk.CTkEntry(fields_frm, textvariable=var, font=self.main_font, width=200, height=32, corner_radius=6, border_width=1)
            entry.grid(row=i, column=1, pady=8)
            setattr(self, f"{attr}_entry", entry)

        ctk.CTkLabel(fields_frm, text="Gender", font=self.bold_font, text_color="#4b5563").grid(row=5, column=0, sticky="w", pady=8, padx=(0,10))
        self.egender_var = tk.StringVar()
        self.egender_cb  = ctk.CTkComboBox(
            fields_frm, variable=self.egender_var,
            values=["Male", "Female", "Other"],
            font=self.main_font, width=200, height=32, corner_radius=6, border_width=1, state="readonly"
        )
        self.egender_cb.grid(row=5, column=1, pady=8)

        sf = ctk.CTkFrame(left, fg_color="white", corner_radius=12)
        sf.pack(fill="x", pady=(0, 15), ipady=10)

        ctk.CTkLabel(sf, text="Smart Filters & Sorting", font=self.title_font, text_color="#111827").pack(anchor="w", padx=20, pady=(15, 10))
        
        sf_grid = ctk.CTkFrame(sf, fg_color="transparent")
        sf_grid.pack(fill="x", padx=20)

        ctk.CTkLabel(sf_grid, text="Min Sal:", font=self.main_font, text_color="#4b5563").grid(row=0, column=0, sticky="w", pady=5)
        self.min_sal_var = tk.StringVar()
        ctk.CTkEntry(sf_grid, textvariable=self.min_sal_var, font=self.main_font, width=100, height=30, corner_radius=6).grid(row=0, column=1, pady=5, padx=(5,15))

        ctk.CTkLabel(sf_grid, text="Max Sal:", font=self.main_font, text_color="#4b5563").grid(row=0, column=2, sticky="w", pady=5)
        self.max_sal_var = tk.StringVar()
        ctk.CTkEntry(sf_grid, textvariable=self.max_sal_var, font=self.main_font, width=100, height=30, corner_radius=6).grid(row=0, column=3, pady=5, padx=(5,0))

        self.sort_col_var = tk.StringVar(value="Name")
        self.sort_ord_var = tk.StringVar(value="ASC")

        ctk.CTkLabel(sf_grid, text="Sort By:", font=self.main_font, text_color="#4b5563").grid(row=1, column=0, sticky="w", pady=10)
        ctk.CTkComboBox(sf_grid, variable=self.sort_col_var, values=["ID", "Name", "Salary", "Department"], width=100, height=30, state="readonly").grid(row=1, column=1, padx=(5,15), pady=10)
        ctk.CTkComboBox(sf_grid, variable=self.sort_ord_var, values=["ASC", "DESC"], width=100, height=30, state="readonly").grid(row=1, column=2, columnspan=2, sticky="w", padx=5, pady=10)

        self.ename_var.trace_add("write", lambda *_: self._smart_search(False))
        self.edept_var.trace_add("write", lambda *_: self._smart_search(False))

    def _build_right_panel(self, parent):
        right_wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        right_wrapper.pack(side="right", fill="both", expand=True)

        self._build_buttons(right_wrapper)

        tree_card = ctk.CTkFrame(right_wrapper, fg_color="white", corner_radius=12)
        tree_card.pack(fill="both", expand=True)

        cols = ("ID", "Name", "Department", "Gender", "Salary", "Contact")
        widths = (70, 160, 140, 90, 120, 140)

        tree_frame = tk.Frame(tree_card, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=26)
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col, command=lambda c=col: self._header_sort(c))
            self.tree.column(col, width=w, anchor="center")

        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure("high",   background="#d1fae5")
        self.tree.tag_configure("low",    background="#fee2e2")
        self.tree.tag_configure("normal", background="#ffffff")

        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

        self._hdr_sort_col   = None
        self._hdr_sort_order = "ASC"

    def _build_buttons(self, parent):
        btn_frm = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        btn_frm.pack(fill="x", pady=(0, 15), ipady=5)
        
        ctk.CTkLabel(btn_frm, text="Quick Actions", font=self.title_font, text_color="#111827").pack(anchor="w", padx=20, pady=(10, 5))

        grid_frm = ctk.CTkFrame(btn_frm, fg_color="transparent")
        grid_frm.pack(anchor="center", pady=(0, 10))

        buttons = [
            ("Insert",       self._insert,          "#10b981", "#059669", True),
            ("Update",       self._update,          "#3b82f6", "#2563eb", True),
            ("Delete",       self._delete,          "#ef4444", "#dc2626", True),
            ("Search",       self._smart_search,    "#8b5cf6", "#7c3aed", False),
            ("Show All",     self._load_all,        "#0ea5e9", "#0284c7", False),
            ("Statistics",   self._show_statistics, "#f59e0b", "#d97706", False),
            ("Export CSV",   self._export_csv,      "#4b5563", "#374151", True),
            ("Export TXT",   self._export_txt,      "#4b5563", "#374151", True),
            ("Clear",        self._clear_form,      "#9ca3af", "#6b7280", False),
            ("Manage Users", self._manage_users,    "#1f2937", "#111827", True),
        ]

        for i, (text, cmd, color, hover, admin_only) in enumerate(buttons):
            state = "normal" if (not admin_only or self.is_admin) else "disabled"
            
            ctk.CTkButton(
                grid_frm, text=text, command=cmd,
                font=self.bold_font, text_color="white",
                fg_color=color if state == "normal" else "#d1d5db", 
                hover_color=hover if state == "normal" else "#d1d5db",
                width=135, height=36, corner_radius=8,
                cursor="hand2" if state == "normal" else "arrow",
                state=state
            ).grid(row=i // 5, column=i % 5, padx=8, pady=6)

    def _build_statusbar(self):
        status_frm = ctk.CTkFrame(self.root, height=40, fg_color="#e5e7eb", corner_radius=0)
        status_frm.pack(fill="x", side="bottom")
        status_frm.pack_propagate(False)

        self.status_var = tk.StringVar(value="System Ready")
        ctk.CTkLabel(
            status_frm, textvariable=self.status_var,
            font=self.bold_font, text_color="#059669", anchor="w"
        ).pack(side="left", padx=20, pady=8)

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
        win.geometry("450x650")
        win.configure(bg="#F0F2F5")
        win.attributes("-topmost", True)

        # ── CREATE USER SECTION ──
        ctk.CTkLabel(win, text="Create New User", font=self.title_font, text_color="#1f2937").pack(pady=(20, 10))

        create_card = ctk.CTkFrame(win, fg_color="white", corner_radius=12)
        create_card.pack(fill="x", padx=20, pady=(0, 20))

        new_uname = tk.StringVar()
        new_pwd = tk.StringVar()
        new_role = tk.StringVar(value="USER")

        ctk.CTkLabel(create_card, text="New Username", font=self.bold_font, text_color="#4b5563").pack(anchor="w", padx=80, pady=(15, 0))
        ctk.CTkEntry(create_card, textvariable=new_uname, width=250).pack(pady=(2, 10))
        
        ctk.CTkLabel(create_card, text="New Password", font=self.bold_font, text_color="#4b5563").pack(anchor="w", padx=80)
        ctk.CTkEntry(create_card, textvariable=new_pwd, show="*", width=250).pack(pady=(2, 10))
        
        ctk.CTkLabel(create_card, text="Assign Role", font=self.bold_font, text_color="#4b5563").pack(anchor="w", padx=80)
        ctk.CTkComboBox(create_card, variable=new_role, values=["ADMIN", "USER"], width=250, state="readonly").pack(pady=(2, 10))

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

        ctk.CTkButton(create_card, text="Save User", font=self.bold_font, fg_color="#10b981", hover_color="#059669", command=save_user).pack(pady=(10, 20))

        # ── REMOVE USER SECTION ──
        ctk.CTkLabel(win, text="Remove User", font=self.title_font, text_color="#1f2937").pack(pady=(10, 10))

        delete_card = ctk.CTkFrame(win, fg_color="white", corner_radius=12)
        delete_card.pack(fill="x", padx=20, pady=(0, 20))

        del_uname = tk.StringVar()
        
        ctk.CTkLabel(delete_card, text="Select standard User to remove", font=self.bold_font, text_color="#4b5563").pack(anchor="w", padx=80, pady=(15, 0))
        user_cb = ctk.CTkComboBox(delete_card, variable=del_uname, width=250, state="readonly")
        user_cb.pack(pady=(2, 10))

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

        ctk.CTkButton(delete_card, text="Delete User", font=self.bold_font, fg_color="#ef4444", hover_color="#dc2626", command=delete_user).pack(pady=(10, 20))

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
        if not conn: return
        try:
            cur = conn.cursor()
            cur.execute("SELECT MAX(salary), MIN(salary), AVG(salary), SUM(salary) FROM employees")
            max_s, min_s, avg_s, sum_s = cur.fetchone()

            cur.execute("SELECT department, COUNT(*) FROM employees GROUP BY department ORDER BY department")
            dept_rows = cur.fetchall()
        except oracledb.DatabaseError as e:
            messagebox.showerror("DB Error", str(e))
            return
        finally:
            conn.close()

        win = ctk.CTkToplevel(self.root)
        win.title("Analytics Dashboard")
        win.geometry("500x550")
        win.configure(bg="#F0F2F5")
        win.attributes("-topmost", True)

        ctk.CTkLabel(win, text="Salary Statistics", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1f2937").pack(pady=(25, 15))

        def fmt(val): return f"PKR {val:,.2f}" if val is not None else "N/A"

        card1 = ctk.CTkFrame(win, fg_color="white", corner_radius=12)
        card1.pack(fill="x", padx=30, pady=10, ipady=10)

        for label, value in [("Highest Salary", fmt(max_s)), ("Lowest Salary", fmt(min_s)), ("Average Salary", fmt(avg_s)), ("Total Expense", fmt(sum_s))]:
            row = ctk.CTkFrame(card1, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(row, text=label, font=self.main_font, text_color="#6b7280").pack(side="left")
            ctk.CTkLabel(row, text=value, font=self.bold_font, text_color="#1f2937").pack(side="right")

        ctk.CTkLabel(win, text="Department Count", font=ctk.CTkFont(size=20, weight="bold"), text_color="#1f2937").pack(pady=(20, 15))
        
        card2 = ctk.CTkFrame(win, fg_color="white", corner_radius=12)
        card2.pack(fill="x", padx=30, pady=10, ipady=10)

        for dept, count in dept_rows:
            row = ctk.CTkFrame(card2, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(row, text=(dept or "Unassigned"), font=self.main_font, text_color="#6b7280").pack(side="left")
            ctk.CTkLabel(row, text=str(count), font=self.bold_font, text_color="#10b981").pack(side="right")

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