import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect("sathi_jewellers_gui.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE NOT NULL,
            purity TEXT NOT NULL,
            purchased_pcs INTEGER DEFAULT 0,
            purchased_weight REAL DEFAULT 0.0,
            sold_pcs INTEGER DEFAULT 0,
            sold_weight REAL DEFAULT 0.0,
            remaining_pcs INTEGER DEFAULT 0,
            remaining_weight REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

# --- Main GUI App ---
class SathiJewellersApp:
    def __init__(self, root):
        self.root = root
        self.root.title("সাথী জুয়েলার্স - স্টক ও সেলস ম্যানেজমেন্ট")
        self.root.geometry("800x550")
        self.root.config(bg="#f4f4f9")

        # Title Header (কোডের এই জায়গায় টাইপোটি ঠিক করা হয়েছে)
        title_label = tk.Label(
            root, text="সাথী জুয়েলার্স", font=("Arial", 22, "bold"),
            bg="#800020", fg="white", pady=10
        )
        title_label.pack(fill=tk.X)

        # Tab Window Navigation (পারচেজ, সেলস, রিটেল স্টক)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=15, expand=True, fill=tk.BOTH)

        # Tab Frames
        self.purchase_frame = ttk.Frame(self.notebook)
        self.sales_frame = ttk.Frame(self.notebook)
        self.stock_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.purchase_frame, text="  পারচেজ অপশন (Stock In)  ")
        self.notebook.add(self.sales_frame, text="  সেলস অপশন (Sales)  ")
        self.notebook.add(self.stock_frame, text="  রিটেল স্টক (Retail Stock)  ")

        # Setup Windows
        self.setup_purchase_tab()
        self.setup_sales_tab()
        self.setup_stock_tab()

    # ১. পারচেজ অপশন (Purchase Tab)
    def setup_purchase_tab(self):
        frame = tk.LabelFrame(self.purchase_frame, text="নতুন স্টক ক্রয় বা এন্ট্রি করুন", font=("Arial", 12, "bold"), padx=20, pady=20)
        frame.pack(pady=20)

        tk.Label(frame, text="আইটেমের নাম:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.p_name = tk.Entry(frame, font=("Arial", 11), width=25)
        self.p_name.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="ক্যারেট/মান (22K/18K):", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.p_purity = tk.Entry(frame, font=("Arial", 11), width=25)
        self.p_purity.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="পরিমাণ (পিস):", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
        self.p_pcs = tk.Entry(frame, font=("Arial", 11), width=25)
        self.p_pcs.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="মোট ওজন (গ্রাম):", font=("Arial", 11)).grid(row=3, column=0, sticky="w", pady=5)
        self.p_wt = tk.Entry(frame, font=("Arial", 11), width=25)
        self.p_wt.grid(row=3, column=1, pady=5)

        btn = tk.Button(frame, text="স্টক যোগ করুন", command=self.add_purchase, bg="#28a745", fg="white", font=("Arial", 11, "bold"), padx=10)
        btn.grid(row=4, columnspan=2, pady=15)

    def add_purchase(self):
        name = self.p_name.get()
        purity = self.p_purity.get()
        try:
            pcs = int(self.p_pcs.get())
            wt = float(self.p_wt.get())
        except ValueError:
            messagebox.showerror("এরর", "পিস এবং ওজনের ঘরে সঠিক সংখ্যা দিন!")
            return

        conn = sqlite3.connect("sathi_jewellers_gui.db")
        cursor = conn.cursor()
        cursor.execute("SELECT purchased_pcs, purchased_weight, remaining_pcs, remaining_weight FROM inventory WHERE item_name = ?", (name,))
        row = cursor.fetchone()

        if row:
            p_pcs, p_wt, r_pcs, r_wt = row
            cursor.execute('''
                UPDATE inventory 
                SET purity = ?, purchased_pcs = ?, purchased_weight = ?, remaining_pcs = ?, remaining_weight = ?
                WHERE item_name = ?
            ''', (purity, p_pcs + pcs, p_wt + wt, r_pcs + pcs, r_wt + wt, name))
        else:
            cursor.execute('''
                INSERT INTO inventory (item_name, purity, purchased_pcs, purchased_weight, remaining_pcs, remaining_weight)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, purity, pcs, wt, pcs, wt))

        conn.commit()
        conn.close()
        messagebox.showinfo("সফল", f"'{name}' সফলভাবে স্টকে যোগ হয়েছে!")
        self.clear_entries([self.p_name, self.p_purity, self.p_pcs, self.p_wt])
        self.load_stock_data()

    # ২. সেলস অপশন (Sales Tab)
    def setup_sales_tab(self):
        frame = tk.LabelFrame(self.sales_frame, text="বিক্রি রেজিস্টার করুন", font=("Arial", 12, "bold"), padx=20, pady=20)
        frame.pack(pady=20)

        tk.Label(frame, text="বিক্রি হওয়া আইটেমের নাম:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.s_name = tk.Entry(frame, font=("Arial", 11), width=25)
        self.s_name.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="বিক্রির পরিমাণ (পিস):", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=5)
        self.s_pcs = tk.Entry(frame, font=("Arial", 11), width=25)
        self.s_pcs.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="বিক্রি হওয়া ওজন (গ্রাম):", font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=5)
        self.s_wt = tk.Entry(frame, font=("Arial", 11), width=25)
        self.s_wt.grid(row=2, column=1, pady=5)

        btn = tk.Button(frame, text="বিক্রি কনফার্ম করুন", command=self.add_sale, bg="#007bff", fg="white", font=("Arial", 11, "bold"), padx=10)
        btn.grid(row=3, columnspan=2, pady=15)

    def add_sale(self):
        name = self.s_name.get()
        try:
            pcs = int(self.s_pcs.get())
            wt = float(self.s_wt.get())
        except ValueError:
            messagebox.showerror("এরর", "পিস এবং ওজনের ঘরে সঠিক সংখ্যা দিন!")
            return

        conn = sqlite3.connect("sathi_jewellers_gui.db")
        cursor = conn.cursor()
        cursor.execute("SELECT sold_pcs, sold_weight, remaining_pcs, remaining_weight FROM inventory WHERE item_name = ?", (name,))
        row = cursor.fetchone()

        if row:
            s_pcs, s_wt, r_pcs, r_wt = row
            if r_pcs >= pcs and r_wt >= wt:
                cursor.execute('''
                    UPDATE inventory 
                    SET sold_pcs = ?, sold_weight = ?, remaining_pcs = ?, remaining_weight = ?
                    WHERE item_name = ?
                ''', (s_pcs + pcs, s_wt + wt, r_pcs - pcs, r_wt - wt, name))
                conn.commit()
                messagebox.showinfo("সফল", f"'{name}' বিক্রি সম্পন্ন হয়েছে!")
                self.clear_entries([self.s_name, self.s_pcs, self.s_wt])
                self.load_stock_data()
            else:
                messagebox.showwarning("সতর্কীকরণ", "দোকানে পর্যাপ্ত স্টক নেই!")
        else:
            messagebox.showerror("এরর", "এই নামের কোনো প্রোডাক্ট স্টকে নেই!")
        conn.close()

    # ৩. রিটেল স্টক টেবিল (Retail Stock Tab)
    def setup_stock_tab(self):
        columns = ("name", "purity", "p_pcs", "p_wt", "s_pcs", "s_wt", "r_pcs", "r_wt")
        self.tree = ttk.Treeview(self.stock_frame, columns=columns, show="headings")

        self.tree.heading("name", text="আইটেমের নাম")
        self.tree.heading("purity", text="ক্যারেট")
        self.tree.heading("p_pcs", text="মোট কেনা (পিস)")
        self.tree.heading("p_wt", text="মোট কেনা (গ্রাম)")
        self.tree.heading("s_pcs", text="মোট বিক্রি (পিস)")
        self.tree.heading("s_wt", text="মোট বিক্রি (গ্রাম)")
        self.tree.heading("r_pcs", text="অবশিষ্ট স্টক (পিস)")
        self.tree.heading("r_wt", text="অবশিষ্ট স্টক (গ্রাম)")

        for col in columns:
            self.tree.column(col, width=95, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_stock_data()

    def load_stock_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("sathi_jewellers_gui.db")
        cursor = conn.cursor()
        cursor.execute("SELECT item_name, purity, purchased_pcs, purchased_weight, sold_pcs, sold_weight, remaining_pcs, remaining_weight FROM inventory")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_entries(self, entries):
        for entry in entries:
            entry.delete(0, tk.END)

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = SathiJewellersApp(root)
    root.mainloop()
    import streamlit as st
import sqlite3

# পেজ টাইটেল ও হেডার
st.set_page_config(page_title="সাথী জুয়েলার্স", layout="centered")
st.title("সাথী জুয়েলার্স")
st.subheader("স্টক ও সেলস ম্যানেজমেন্ট")

# ট্যাব তৈরি (পারচেজ, সেলস, রিটার্ন স্টক)
tab1, tab2, tab3 = st.tabs(["পারচেজ অপশন (Stock In)", "সেলস অপশন (Sales)", "রিটেল স্টক (Retail Stock)"])

with tab1:
    st.header("নতুন স্টক ক্রয় বা এন্ট্রি করুন")
    
    # ইনপুট ফিল্ডসমূহ
    item_name = st.text_input("আইটেমের নাম:")
    karat = st.selectbox("ক্যারেট/মান:", ["22K", "18K", "24K"])
    quantity = st.number_input("পরিমাণ (পিস):", min_value=1, step=1)
    weight = st.number_input("মোট ওজন (গ্রাম):", min_value=0.0, format="%.2f")
    
    # স্টক যোগ করার বাটন
    if st.button("স্টক যোগ করুন"):
        if item_name and weight > 0:
            # এখানে আপনার ডাটাবেস এন্ট্রির ফাংশনটি কল করবেন
            # save_to_db(item_name, karat, quantity, weight)
            st.success(f"{item_name} সফলভাবে স্টকে যোগ করা হয়েছে!")
        else:
            st.error("সব তথ্য সঠিকভাব দিন।")
            