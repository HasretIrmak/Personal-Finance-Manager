import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from datetime import datetime


class FinanceManager:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Personal Finance Manager")
        self.window.geometry("800x900")
        self.window.configure(bg="#f0f0f0")

        # Stil ayarları
        self.style = ttk.Style()
        self.style.configure("Custom.TFrame", background="#f0f0f0")
        self.style.configure("Title.TLabel",
                             font=("Helvetica", 16, "bold"),
                             background="#f0f0f0")
        self.style.configure("Header.TLabel",
                             font=("Helvetica", 12, "bold"),
                             background="#f0f0f0")
        self.style.configure("Custom.TButton",
                             font=("Helvetica", 10),
                             padding=10)

        self.data = self.load_data()
        self.create_widgets()
        self.update_summary()

    def load_data(self, filename="finance_data.json"):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"income": [], "expenses": []}

    def save_data(self, filename="finance_data.json"):
        with open(filename, 'w') as f:
            json.dump(self.data, f)

    def create_widgets(self):
        # Ana container
        main_frame = ttk.Frame(self.window, style="Custom.TFrame", padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Başlık
        title = ttk.Label(main_frame,
                          text="Personal Finance Manager",
                          style="Title.TLabel")
        title.pack(pady=(0, 20))

        # Giriş alanları için frame
        input_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        input_frame.pack(fill=tk.X, pady=10)

        # Gelir Bölümü
        income_frame = ttk.LabelFrame(input_frame,
                                      text="Add Income",
                                      padding="10",
                                      style="Custom.TFrame")
        income_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        ttk.Label(income_frame, text="Amount ($):", style="Header.TLabel").pack()
        self.income_amount = ttk.Entry(income_frame, width=20)
        self.income_amount.pack(pady=5)

        ttk.Label(income_frame, text="Description:", style="Header.TLabel").pack()
        self.income_desc = ttk.Entry(income_frame, width=20)
        self.income_desc.pack(pady=5)

        ttk.Button(income_frame,
                   text="Add Income",
                   style="Custom.TButton",
                   command=self.add_income).pack(pady=10)

        # Gider Bölümü
        expense_frame = ttk.LabelFrame(input_frame,
                                       text="Add Expense",
                                       padding="10",
                                       style="Custom.TFrame")
        expense_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

        ttk.Label(expense_frame, text="Amount ($):", style="Header.TLabel").pack()
        self.expense_amount = ttk.Entry(expense_frame, width=20)
        self.expense_amount.pack(pady=5)

        ttk.Label(expense_frame, text="Description:", style="Header.TLabel").pack()
        self.expense_desc = ttk.Entry(expense_frame, width=20)
        self.expense_desc.pack(pady=5)

        ttk.Button(expense_frame,
                   text="Add Expense",
                   style="Custom.TButton",
                   command=self.add_expense).pack(pady=10)

        # Özet bölümü
        summary_frame = ttk.LabelFrame(main_frame,
                                       text="Financial Summary",
                                       padding="10",
                                       style="Custom.TFrame")
        summary_frame.pack(fill=tk.X, pady=20, padx=10)

        self.total_income_label = ttk.Label(summary_frame,
                                            style="Header.TLabel",
                                            foreground="green")
        self.total_income_label.pack()

        self.total_expense_label = ttk.Label(summary_frame,
                                             style="Header.TLabel",
                                             foreground="red")
        self.total_expense_label.pack()

        self.savings_label = ttk.Label(summary_frame,
                                       style="Header.TLabel",
                                       foreground="blue")
        self.savings_label.pack()

        # Grafik alanı
        self.graph_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=20)

    def add_income(self):
        try:
            amount = float(self.income_amount.get())
            description = self.income_desc.get()

            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return

            self.data["income"].append({
                "amount": amount,
                "description": description,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.save_data()
            self.income_amount.delete(0, tk.END)
            self.income_desc.delete(0, tk.END)
            self.update_summary()
            messagebox.showinfo("Success", "Income added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def add_expense(self):
        try:
            amount = float(self.expense_amount.get())
            description = self.expense_desc.get()

            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0")
                return

            self.data["expenses"].append({
                "amount": amount,
                "description": description,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.save_data()
            self.expense_amount.delete(0, tk.END)
            self.expense_desc.delete(0, tk.END)
            self.update_summary()
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def update_summary(self):
        total_income = sum(item['amount'] for item in self.data['income'])
        total_expenses = sum(item['amount'] for item in self.data['expenses'])
        savings = total_income - total_expenses

        self.total_income_label.config(
            text=f"Total Income: ${total_income:,.2f}")
        self.total_expense_label.config(
            text=f"Total Expenses: ${total_expenses:,.2f}")
        self.savings_label.config(
            text=f"Net Savings: ${savings:,.2f}")

        self.plot_graph(total_income, total_expenses)

    def plot_graph(self, income, expenses):
        # Önceki grafiği temizle
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor('#f0f0f0')

        # Bar grafik
        categories = ['Income', 'Expenses']
        values = [income, expenses]
        colors = ['#2ecc71', '#e74c3c']

        ax1.bar(categories, values, color=colors)
        ax1.set_title("Income vs Expenses")
        ax1.set_ylabel("Amount ($)")

        # Pasta grafik
        if income > 0 or expenses > 0:
            ax2.pie([income, expenses],
                    labels=['Income', 'Expenses'],
                    colors=colors,
                    autopct='%1.1f%%')
            ax2.set_title("Income/Expense Distribution")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = FinanceManager()
    app.run()
