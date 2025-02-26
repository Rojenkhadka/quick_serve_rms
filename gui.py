import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Main Dashboard
class MainDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QuickServe")
        self.geometry("400x300")
        self.configure(background='#98FB98')

        # Welcome Label
        welcome_label = ttk.Label(self, text="Welcome to QuickServe", font=("Arial", 16))
        welcome_label.pack(pady=20)

        # Admin Button
        admin_button = ttk.Button(self, text="Login", command=self.open_admin_login, width=20)
        admin_button.pack(pady=10)

        # Customer Button
        customer_button = ttk.Button(self, text="Signup", command=self.open_signup, width=20)
        customer_button.pack(pady=10)

        # Signup Button
        signup_button = ttk.Button(self, text="Customer Interface", command=self.open_customer_dashboard, width=20)
        signup_button.pack(pady=10)


    def open_admin_login(self):
        # Open the LoginWindow for admin authentication
        self.destroy()  # Close the MainDashboard
        login_window = LoginWindow()
        login_window.mainloop()

    def open_customer_dashboard(self):
        # Open the CustomerDashboard directly
        self.destroy()  # Close the MainDashboard
        customer_dashboard = CustomerDashboard()
        customer_dashboard.mainloop()

    def open_signup(self):
        # Open the SignupWindow
        signup_window = SignupWindow()
        signup_window.mainloop()


class LoginWindow(tk.TK):
    def __init__(self):
        super().__init__()
        self.title("Restaurant Management System - Login")
        self.geometry("300x150")
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # Style configuration
        style = ttk.Style(self)
        style.configure('TButton', background='#28A745', foreground='black', font=('Arial', 10, 'bold'))
        style.configure('TLabel', font=('Arial', 10), background='#FFD700')
        style.configure('TEntry', font=('Arial', 10), fieldbackground='#FFD700')
        style.configure('TCombobox', font=('Arial', 10), fieldbackground='#FFD700')
        style.configure('TFrame', background='#98FB98')
        style.configure('TNotebook', background='#98FB98')
        style.configure('TNotebook.Tab', background='#007BFF', foreground='black', font=('Arial', 10, 'bold'))
        
        self.configure(background='#98FB98')
        
        ttk.Label(self, text="Username:").grid(row=0, padx=10, pady=5)
        ttk.Entry(self, textvariable=self.username).grid(row=0, column=1, padx=10)
        
        ttk.Label(self, text="Password:").grid(row=1, padx=10, pady=5)
        ttk.Entry(self, textvariable=self.password, show="*").grid(row=1, column=1)
        
        ttk.Button(self, text="Login", command=self.authenticate).grid(row=2, columnspan=2, pady=10)

    def open_signup(self):
        SignupWindow()

    def authenticate(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        
        if username == "":
            messagebox.showerror("Error", "Username cannot be empty")
            return
        if password == "":
            messagebox.showerror("Error", "Password cannot be empty")
            return

        conn = None
        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('SELECT role FROM Users WHERE username=? AND password=?',
                          (username, password))
            result = cursor.fetchone()
            
            if result:
                role = result[0]
                self.destroy()  # Close login window before opening dashboard
                if role == 'admin':
                    Admindashboard()
                elif role == 'staff':
                    KitchenDashboard()
                else:
                    messagebox.showerror("Error", "Invalid role")
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

class SignupWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sign Up")
        self.geometry("300x200")
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.role = tk.StringVar(value='admin')

        ttk.Label(self, text="Username:").grid(row=0, padx=10, pady=5)
        ttk.Entry(self, textvariable=self.username).grid(row=0, column=1, padx=10)

        ttk.Label(self, text="Password:").grid(row=1, padx=10, pady=5)
        ttk.Entry(self, textvariable=self.password, show="*").grid(row=1, column=1)

        # Role is fixed to 'admin' for signups
        ttk.Label(self, text="Role: admin").grid(row=2, padx=10, pady=5)

        ttk.Button(self, text="Sign Up", command=self.signup).grid(row=3, columnspan=2, pady=10)

    def signup(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        role = self.role.get().strip()

        if not username or len(username) > 20:
            messagebox.showerror("Error", "Username must be 1-20 characters")
            return
        if not password or len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        if role != 'admin':
            messagebox.showerror("Error", "Invalid role")
            return
        if not password or len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        if role not in ['admin', 'staff']:
            messagebox.showerror("Error", "Invalid role selected")
            return

        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Users (username, password, role) VALUES (?, ?, ?)',
                           (username, password, role))
            conn.commit()
            messagebox.showinfo("Success", "User created successfully")
            self.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

class Admindashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("1000x600")
        
        # Style configuration
        style = ttk.Style(self)
        style.configure('TButton', background='#007BFF', foreground='black', font=('Arial', 10, 'bold'))
        style.configure('TLabel', font=('Arial', 10), background='#FFD700')
        style.configure('TEntry', font=('Arial', 10), fieldbackground='#FFD700')
        style.configure('TCombobox', font=('Arial', 10), fieldbackground='#FFD700')
        style.configure('TFrame', background='#98FB98')
        style.configure('TNotebook', background='#98FB98')
        style.configure('TNotebook.Tab', background='#007BFF', foreground='black', font=('Arial', 10, 'bold'))
        
        self.configure(background='#98FB98')
        self.create_menu_bar()
        self.create_widgets()
        self.create_logout_button()

        # Add a "Back" button
        back_button = ttk.Button(self, text="Back to Main", command=self.go_back_to_main)
        back_button.pack(side='bottom', pady=10)

        # Notify customer dashboard to refresh menu items
        self.refresh_customer_dashboard()

    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("1000x600")
        
        # Style configuration
        style = ttk.Style(self)
        style.configure('TButton', background='#007BFF', foreground='black', font=('Arial', 10, 'bold'))
        style.configure('TLabel', font=('Arial', 10), background='#FFD700')
        style.configure('TEntry', font=('Arial', 10), fieldbackground='#FFD700')
        style.configure('TCombobox', font=('Arial', 10), fieldbackground='#FFD700')
        style.configure('TFrame', background='#98FB98')
        style.configure('TNotebook', background='#98FB98')
        style.configure('TNotebook.Tab', background='#007BFF', foreground='black', font=('Arial', 10, 'bold'))
        
        self.configure(background='#98FB98')
        self.create_menu_bar()
        self.create_widgets()
        # self.create_logout_button()

        # Add a "Back" button
        back_button = ttk.Button(self, text="Logout", command=self.go_back_to_main)
        back_button.pack(side='bottom', pady=10)
    
    def go_back_to_main(self):
        """Close the AdminDashboard and reopen the MainDashboard."""
        self.destroy()  # Close the AdminDashboard
        main_dashboard = MainDashboard()  # Reopen the MainDashboard
        main_dashboard.mainloop()

    def create_menu_bar(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        
        self.config(menu=menubar)

    def logout(self):
        self.destroy()  # Close the KitchenDashboard
        main_dashboard = MainDashboard()  # Reopen the MainDashboard
        main_dashboard.mainloop()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        
        # Menu Management Tab
        menu_tab = ttk.Frame(notebook)
        self.create_menu_management(menu_tab)
        
        # Users Tab
        users_tab = ttk.Frame(notebook)
        self.create_user_management(users_tab)
        
        # Reports Tab
        reports_tab = ttk.Frame(notebook)
        self.create_reports(reports_tab)
        
        notebook.add(menu_tab, text="Menu")
        notebook.add(users_tab, text="Users")
        notebook.add(reports_tab, text="Reports")
        notebook.pack(expand=True, fill='both')

    # Menu Management
    def create_menu_management(self, parent):
        input_frame = ttk.Frame(parent)
        input_frame.pack(pady=10, fill='x')
        
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5)
        self.menu_name = ttk.Entry(input_frame)
        self.menu_name.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5)
        self.menu_category = ttk.Combobox(input_frame, values=["Appetizer", "Main Course", "Dessert", "Beverage"])
        self.menu_category.grid(row=0, column=3, padx=5)
        
        ttk.Label(input_frame, text="Price:").grid(row=0, column=4, padx=5)
        self.menu_price = ttk.Entry(input_frame)
        self.menu_price.grid(row=0, column=5, padx=5)
        
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Name', 'Category', 'Price')
        self.menu_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        for col in columns:
            self.menu_tree.heading(col, text=col)
            self.menu_tree.column(col, width=100)
        
        self.menu_tree.pack(fill='both', expand=True)
        
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add Item", command=self.add_menu_item).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update Item", command=self.update_menu_item).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.load_menu_items).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Delete Item", command=self.delete_menu_item).grid(row=0, column=2, padx=5)
        
        self.load_menu_items()

    def refresh_customer_dashboard(self):
        """Notify the CustomerDashboard to refresh its menu items."""
        for window in self.winfo_children():
            if isinstance(window, CustomerDashboard):
                window.refresh_menu_items()
    
    def load_menu_items(self):

        for item in self.menu_tree.get_children():
            self.menu_tree.delete(item)
        
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM MenuItems')
        for item in cursor.fetchall():
            self.menu_tree.insert('', 'end', values=item[:-1])
        conn.close()

    def add_menu_item(self):
        name = self.menu_name.get().strip()
        category = self.menu_category.get().strip()
        price = self.menu_price.get().strip()
        
        if not name or len(name) > 50:
            messagebox.showerror("Error", "Name must be 1-50 characters")
            return
        if not category or category not in ["Appetizer", "Main Course", "Dessert", "Beverage"]:
            messagebox.showerror("Error", "Invalid category selected")
            return
        try:
            price = float(price)
            if price <= 0 or price > 1000:
                messagebox.showerror("Error", "Price must be between $0.01 and $1000")
                return
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number")
            return
        
        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO MenuItems (name, category, price) VALUES (?, ?, ?)',
                           (name, category, float(price)))
            conn.commit()
            self.load_menu_items()
            messagebox.showinfo("Success", "Menu item added successfully")
        except ValueError:
            messagebox.showerror("Error", "Invalid price format")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def update_menu_item(self):
        selected = self.menu_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an item to update")
            return
        
        item_id = self.menu_tree.item(selected[0], 'values')[0]
        name = self.menu_name.get().strip()
        category = self.menu_category.get().strip()
        price = self.menu_price.get().strip()
        
        if not name or len(name) > 50:
            messagebox.showerror("Error", "Name must be 1-50 characters")
            return
        if not category or category not in ["Appetizer", "Main Course", "Dessert", "Beverage"]:
            messagebox.showerror("Error", "Invalid category selected")
            return
        try:
            price = float(price)
            if price <= 0 or price > 1000:
                messagebox.showerror("Error", "Price must be between $0.01 and $1000")
                return
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number")
            return
        
        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE MenuItems SET 
                            name=?, category=?, price=? 
                            WHERE item_id=?''',
                          (name, category, float(price), item_id))
            conn.commit()
            self.load_menu_items()
        except ValueError:
            messagebox.showerror("Error", "Invalid price format")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def delete_menu_item(self):
        selected = self.menu_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No item selected")
            return
        
        item_id = self.menu_tree.item(selected[0], 'values')[0]
        
        confirm = messagebox.askyesno("Confirm", "Delete this item?")
        if confirm:
            try:
                conn = sqlite3.connect('restaurant.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM MenuItems WHERE item_id=?', (item_id,))
                conn.commit()
                self.load_menu_items()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                if conn:
                    conn.close()

    # User Management
    def create_user_management(self, parent):
        input_frame = ttk.Frame(parent)
        input_frame.pack(pady=10, fill='x')
        
        ttk.Label(input_frame, text="Username:").grid(row=0, column=0, padx=5)
        self.user_name = ttk.Entry(input_frame)
        self.user_name.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Password:").grid(row=0, column=2, padx=5)
        self.user_pass = ttk.Entry(input_frame)
        self.user_pass.grid(row=0, column=3, padx=5)
        
        ttk.Label(input_frame, text="Role:").grid(row=0, column=4, padx=5)
        self.user_role = ttk.Combobox(input_frame, values=['admin', 'staff'])
        self.user_role.grid(row=0, column=5, padx=5)
        
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('ID', 'Username', 'Role')
        self.user_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=100)
        
        self.user_tree.pack(fill='both', expand=True)
        
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Add User", command=self.add_user).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update User", command=self.update_user).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete User", command=self.delete_user).grid(row=0, column=2, padx=5)
        
        self.load_users()

    def add_user(self):
        username = self.user_name.get().strip()
        password = self.user_pass.get().strip()
        role = self.user_role.get().strip()
        
        if not username or len(username) > 20:
            messagebox.showerror("Error", "Username must be 1-20 characters")
            return
        if not password or len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        if role not in ['admin', 'staff']:
            messagebox.showerror("Error", "Invalid role selected")
            return
        
        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Users (username, password, role) VALUES (?, ?, ?)',
                          (username, password, role))
            conn.commit()
            self.load_users()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def load_users(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, username, role FROM Users')
        for user in cursor.fetchall():
            self.user_tree.insert('', 'end', values=user)
        conn.close()

    def update_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No user selected")
            return
        
        user_id = self.user_tree.item(selected[0], 'values')[0]
        username = self.user_name.get().strip()
        password = self.user_pass.get().strip()
        role = self.user_role.get().strip()
        
        if not username or len(username) > 20:
            messagebox.showerror("Error", "Username must be 1-20 characters")
            return
        if not password or len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        if role not in ['admin', 'staff']:
            messagebox.showerror("Error", "Invalid role selected")
            return
        
        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('''UPDATE Users SET 
                            username=?, password=?, role=? 
                            WHERE user_id=?''',
                          (username, password, role, user_id))
            conn.commit()
            self.load_users()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def delete_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showerror("Error", "No user selected")
            return
        
        user_id = self.user_tree.item(selected[0], 'values')[0]
        
        if user_id in [1, 2, 3]:  
            messagebox.showerror("Error", "Cannot delete default users")
            return
        
        confirm = messagebox.askyesno("Confirm", "Delete this user?")
        if confirm:
            try:
                conn = sqlite3.connect('restaurant.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM Users WHERE user_id=?', (user_id,))
                conn.commit()
                self.load_users()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                if conn:
                    conn.close()

    # Reports
    def create_reports(self, parent):
        report_frame = ttk.Frame(parent)
        report_frame.pack(pady=10, fill='x')
        
        ttk.Label(report_frame, text="Report Type:").grid(row=0, column=0)
        self.report_type = ttk.Combobox(report_frame, values=['Sales'])
        self.report_type.grid(row=0, column=1, padx=5)
        
        ttk.Button(report_frame, text="Generate", command=self.generate_report).grid(row=0, column=2)
        
        self.report_text = tk.Text(parent, wrap=tk.WORD)
        self.report_text.pack(fill='both', expand=True, padx=10, pady=10)

    def generate_report(self):
        report_type = self.report_type.get()
        self.report_text.delete(1.0, tk.END)
        
        if report_type == 'Sales':
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(total_price) FROM Orders')
            total_sales = cursor.fetchone()[0] or 0
            
            cursor.execute('''SELECT m.name, SUM(od.quantity) 
                            FROM OrderDetails od
                            JOIN MenuItems m ON od.item_id = m.item_id
                            GROUP BY od.item_id
                            ORDER BY SUM(od.quantity) DESC LIMIT 5''')
            popular_items = cursor.fetchall()
            
            report = f"=== Sales Report ===\n"
            report += f"Total Sales: Rs {total_sales:.2f}\n\n"
            report += "Most Popular Items:\n"
            for item in popular_items:
                report += f"- {item[0]}: {item[1]} orders\n"
            
            self.report_text.insert(tk.END, report)
            conn.close()

class KitchenDashboard(tk.TK):
    def create_logout_button(self):
        logout_frame = ttk.Frame(self)
        logout_frame.pack(side='bottom', fill='x', pady=10)
        ttk.Button(logout_frame, text="Logout", command=self.logout).pack()

    def logout(self):
        # Cancel the scheduled refresh_orders callback
        if hasattr(self, 'after_id'):
            self.after_cancel(self.after_id)
        self.destroy()  # Close the KitchenDashboard
        main_dashboard = MainDashboard()  # Reopen the MainDashboard
        main_dashboard.mainloop()
        

    def __init__(self):
        super().__init__()
        self.title("Kitchen Dashboard")
        self.geometry("1000x600")
        self.configure(background='#98FB98')
        self.create_widgets()
        logout_frame=ttk.Frame(self)
        logout_frame.pack(side='bottom', fill='x', pady=10)
        ttk.Button(logout_frame, text="Logout", command=self.logout).pack()
        self.refresh_orders()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Define the columns for the Treeview
        columns = ('Order ID', 'Table', 'Items', 'Status', 'Timestamp')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        self.tree.pack(fill='both', expand=True)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Mark Preparing", command=lambda: self.update_status('preparing')).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Mark Ready", command=lambda: self.update_status('ready')).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_orders).pack(side='left', padx=5)

    def refresh_orders(self):
        try:
            # Clear the existing items in the tree
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Fetch and display new orders
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT o.order_id, o.table_number, 
                             GROUP_CONCAT(m.name || ' x' || od.quantity, ', '), 
                             o.status, o.timestamp
                             FROM Orders o
                             JOIN OrderDetails od ON o.order_id = od.order_id
                             JOIN MenuItems m ON od.item_id = m.item_id
                             WHERE o.status NOT IN ('completed', 'ready')
                             GROUP BY o.order_id''')
            
            for order in cursor.fetchall():
                # Ensure the order of values matches the Treeview columns
                self.tree.insert('', 'end', values=order)
            conn.close()
        except Exception as e:
            print(f"Error refreshing orders: {e}")
        finally:
            # Schedule the next refresh only if the window still exists
            if self.winfo_exists():
                self.after_id = self.after(5000, self.refresh_orders)

    def update_status(self, status):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error", "No order selected")
            return
        
        order_id = self.tree.item(selected[0], 'values')[0]
        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE Orders SET status=? WHERE order_id=?', (status, order_id))
            conn.commit()

            # Refresh only the updated row
            self.refresh_order_row(order_id)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update order status: {e}")
        finally:
            if conn:
                conn.close()

    def refresh_order_row(self, order_id):
        """Refresh only the row corresponding to the given order_id."""
        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT o.order_id, o.table_number, 
                             GROUP_CONCAT(m.name || ' x' || od.quantity, ', '), 
                             o.status, o.timestamp
                             FROM Orders o
                             JOIN OrderDetails od ON o.order_id = od.order_id
                             JOIN MenuItems m ON od.item_id = m.item_id
                             WHERE o.order_id = ?
                             GROUP BY o.order_id''', (order_id,))
            
            updated_order = cursor.fetchone()
            conn.close()

            if updated_order:
                # Find the item in the Treeview and update its values
                for item in self.tree.get_children():
                    if self.tree.item(item, 'values')[0] == order_id:
                        self.tree.item(item, values=updated_order)
                        break
        except Exception as e:
            print(f"Error refreshing order row: {e}")


class CustomerDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Customer Dashboard")
        self.geometry("1000x600")
        
        # Style configuration
        style = ttk.Style(self)
        style.configure('TButton', background='#007BFF', foreground='black', font=('Arial', 10, 'bold'))
        style.configure('TLabel', font=('Arial', 10), background='#FFD700')
        style.configure('TEntry', font=('Arial', 10), fieldbackground='#FFD700')
        style.configure('TCombobox', font=('Arial', 10), fieldbackground='#FFD700')
        style.configure('TFrame', background='#98FB98')
        style.configure('TNotebook', background='#98FB98')
        style.configure('TNotebook.Tab', background='#007BFF', foreground='black', font=('Arial', 10, 'bold'))
        
        self.configure(background='#98FB98')
        self.create_widgets()
        
        # Add a "Back" button
        back_button = ttk.Button(self, text="Back to Main", command=self.go_back_to_main)
        back_button.pack(side='bottom', pady=10)
    
    def go_back_to_main(self):
        """Close the CustomerDashboard and reopen the MainDashboard."""
        self.destroy()  # Close the CustomerDashboard
        main_dashboard = MainDashboard()  # Reopen the MainDashboard
        main_dashboard.mainloop()
    
    def create_widgets(self):
        notebook = ttk.Notebook(self)
        
        # Order Management Tab
        order_tab = ttk.Frame(notebook)
        self.create_order_management(order_tab)
        ttk.Button(self, text="Refresh", command=self.refresh_menu_items).pack(pady=10)

        notebook.add(order_tab, text="Orders")
        notebook.pack(expand=True, fill='both')
    
    def create_order_management(self, parent):
        order_frame = ttk.Frame(parent)
        order_frame.pack(pady=10, fill='x')
        
        ttk.Label(order_frame, text="Table Number:").grid(row=0, column=0)
        self.table_number = ttk.Spinbox(order_frame, from_=1, to=20)
        self.table_number.grid(row=0, column=1, padx=5)
        
        ttk.Label(order_frame, text="Menu Items:").grid(row=0, column=2)
        self.item_combobox = ttk.Combobox(order_frame)
        self.item_combobox.grid(row=0, column=3, padx=5)
        self.item_combobox['values'] = [item[1] for item in self.get_menu_items() if item[1] is not None]
        
        ttk.Label(order_frame, text="Quantity:").grid(row=0, column=4)
        self.quantity = ttk.Spinbox(order_frame, from_=1, to=10)
        self.quantity.grid(row=0, column=5, padx=5)
        
        ttk.Button(order_frame, text="Add to Cart", command=self.add_to_order).grid(row=0, column=6, padx=5)
        
        self.order_tree = ttk.Treeview(parent, columns=('Item', 'Quantity', 'Price'), show='headings')
        self.order_tree.heading('Item', text='Item')
        self.order_tree.heading('Quantity', text='Quantity')
        self.order_tree.heading('Price', text='Price')
        self.order_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.total_label = ttk.Label(parent, text="Total: Rs 0.00")
        self.total_label.pack(pady=5)
        
        ttk.Button(parent, text="Submit Order", command=self.submit_order).pack(pady=10)
        
        self.current_order = []

    def refresh_menu_items(self):
        menu_items = self.get_menu_items()
        self.item_combobox['values'] = [item[1] for item in menu_items]
        self.order_tree.delete(*self.order_tree.get_children())

    def get_menu_items(self):
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM MenuItems')
        items = cursor.fetchall()
        conn.close()
        return items

    def add_to_order(self):
        item_name = self.item_combobox.get()
        quantity = int(self.quantity.get())
        
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        cursor.execute('SELECT item_id, price FROM MenuItems WHERE name=?', (item_name,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            item_id, price = result
            self.current_order.append({
                'item_id': item_id,
                'name': item_name,
                'quantity': quantity,
                'price': price
            })
            self.order_tree.insert('', 'end', values=(item_name, quantity, f"Rs {price * quantity:.2f}"))
            self.update_total()
        else:
            messagebox.showerror("Error", "Invalid item selection")

    def update_total(self):
        total = sum(item['price'] * item['quantity'] for item in self.current_order)
        self.total_label.config(text=f"Total: Rs {total:.2f}")

    def submit_order(self):
        if not self.current_order:
            messagebox.showerror("Error", "No items in order")
            return
        
        try:
            table_number = int(self.table_number.get().strip())
            if table_number < 1 or table_number > 20:
                messagebox.showerror("Error", "Table number must be 1-20")
                return
        except ValueError:
            messagebox.showerror("Error", "Table number must be a valid number")
            return
            
        user_id = 2  # Default staff user

        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            total = sum(item['price'] * item['quantity'] for item in self.current_order)
            
            cursor.execute('''INSERT INTO Orders 
                            (table_number, user_id, total_price)
                            VALUES (?, ?, ?)''',
                          (int(table_number), user_id, total))
            order_id = cursor.lastrowid
            
            for item in self.current_order:
                cursor.execute('''INSERT INTO OrderDetails 
                                (order_id, item_id, quantity)
                                VALUES (?, ?, ?)''',
                              (order_id, item['item_id'], item['quantity']))
            
            conn.commit()
            messagebox.showinfo("Success", "Order submitted successfully")
            self.current_order = []
            self.order_tree.delete(*self.order_tree.get_children())
            self.update_total()
        except ValueError:
            messagebox.showerror("Error", "Invalid table number")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    app = LoginWindow()
