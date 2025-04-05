
""" Task 2  by Brain Wave Matrics Solution
Create an Inventory Management System

Build a Python program to manage inventory for a store or warehouse. The
system should allow users to add, edit, and delete products, track inventory levels,

and generate reports such as low- stock alerts or sales summaries. Implement
features like user authentication,
data validation, and graphical user interface (GUI) for better usability."""


import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# ---------- Data Handling ----------
PRODUCT_FILE = "inventory.json"
USER_FILE = "users.json"


def load_data(file, default):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    else:
        return default


def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


products = load_data(PRODUCT_FILE, {})
users = load_data(USER_FILE, {"admin": "admin123"})  # Default admin login


# ---------- Main Application ----------
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.username = None
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if users.get(username) == password:
            self.username = username
            self.create_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

    def create_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome {self.username}!", font=("Arial", 14)).pack()

        tk.Button(self.root, text="Add Product", command=self.add_product_screen).pack(pady=5)
        tk.Button(self.root, text="Manage Products", command=self.manage_products_screen).pack(pady=5)
        tk.Button(self.root, text="Low Stock Report", command=self.low_stock_report).pack(pady=5)
        tk.Button(self.root, text="Sales Summary", command=self.sales_summary).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.create_login_screen).pack(pady=5)

    def add_product_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Add New Product").pack()

        self.name_entry = self.create_labeled_entry("Product Name")
        self.qty_entry = self.create_labeled_entry("Quantity")
        self.price_entry = self.create_labeled_entry("Price")

        tk.Button(self.root, text="Add", command=self.add_product).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.create_dashboard).pack()

    def create_labeled_entry(self, label):
        tk.Label(self.root, text=label).pack()
        entry = tk.Entry(self.root)
        entry.pack()
        return entry

    def add_product(self):
        name = self.name_entry.get()
        try:
            qty = int(self.qty_entry.get())
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer, and Price must be a number.")
            return

        if name in products:
            messagebox.showerror("Error", "Product already exists.")
        else:
            products[name] = {"quantity": qty, "price": price, "sold": 0}
            save_data(PRODUCT_FILE, products)
            messagebox.showinfo("Success", "Product added successfully!")
            self.create_dashboard()

    def manage_products_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Product List").pack()

        self.tree = ttk.Treeview(self.root, columns=('Name',"Qty", "Price"), show="headings")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Qty", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.pack()

        for name, data in products.items():
            self.tree.insert("", "end", iid=name, values=(name,data["quantity"], data["price"]))

        tk.Button(self.root, text="Edit", command=self.edit_product_screen).pack(pady=5)
        tk.Button(self.root, text="Delete", command=self.delete_product).pack()
        tk.Button(self.root, text="Back", command=self.create_dashboard).pack(pady=5)

    def edit_product_screen(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "No product selected.")
            return
        name = selected[0]
        data = products[name]

        self.clear_screen()
        tk.Label(self.root, text=f"Editing {name}").pack()

        self.edit_qty = self.create_labeled_entry("New Quantity")
        self.edit_qty.insert(0, str(data["quantity"]))
        self.edit_price = self.create_labeled_entry("New Price")
        self.edit_price.insert(0, str(data["price"]))

        tk.Button(self.root, text="Update", command=lambda: self.update_product(name)).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.manage_products_screen).pack()

    def update_product(self, name):
        try:
            qty = int(self.edit_qty.get())
            price = float(self.edit_price.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")
            return
        products[name]["quantity"] = qty
        products[name]["price"] = price
        save_data(PRODUCT_FILE, products)
        messagebox.showinfo("Updated", "Product updated successfully.")
        self.manage_products_screen()

    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "No product selected.")
            return
        name = selected[0]
        confirm = messagebox.askyesno("Confirm", f"Delete {name}?")
        if confirm:
            del products[name]
            save_data(PRODUCT_FILE, products)
            self.manage_products_screen()

    def low_stock_report(self):
        self.clear_screen()
        tk.Label(self.root, text="Low Stock Products (< 5)").pack()

        for name, data in products.items():
            if data["quantity"] < 5:
                tk.Label(self.root, text=f"{name} - {data['quantity']} left").pack()

        tk.Button(self.root, text="Back", command=self.create_dashboard).pack(pady=5)

    def sales_summary(self):
        self.clear_screen()
        tk.Label(self.root, text="Sales Summary").pack()
        tk.Button(self.root, text="Back", command=self.create_dashboard).pack()

        for name, data in products.items():
            total_sales = data["sold"] * data["price"]
            tk.Label(self.root, text=f"{name} - Sold: {data['sold']} - ₹{total_sales:.2f}").pack()

        tk.Button(self.root, text="Back", command=self.create_dashboard).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------- Run Program ----------
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x500")
    app = InventoryApp(root)
    root.mainloop()
