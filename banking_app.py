import tkinter as tk
from tkinter import messagebox
import random
import string

# Function to generate a random password
def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(5))
    return password

# Function to handle deposits
def deposit(balance, amount):
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        balance += amount
        update_transaction_log("Deposit", amount)
        messagebox.showinfo("Success", f"Deposit of R{amount} successful.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")
    return balance

# Function to handle withdrawals
def withdraw(balance, amount):
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > balance:
            raise ValueError("Insufficient funds")
        balance -= amount
        update_transaction_log("Withdrawal", amount)
        messagebox.showinfo("Success", f"Withdrawal of R{amount} successful.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")
    return balance

# Function to update transaction log
def update_transaction_log(transaction_type, amount):
    with open("TransactionLog.txt", "a") as log_file:
        log_file.write(f"{transaction_type}: R{amount}\n")

# Function to update bank data
def update_bank_data(balance):
    with open("BankData.txt", "w") as bank_data_file:
        bank_data_file.write(str(balance))

# Function to read current balance from bank data
def read_balance():
    try:
        with open("BankData.txt", "r") as bank_data_file:
            balance = float(bank_data_file.read())
    except FileNotFoundError:
        balance = 0.0
    return balance

# Function to read transaction log
def read_transaction_log():
    try:
        with open("TransactionLog.txt", "r") as log_file:
            log_content = log_file.read()
    except FileNotFoundError:
        log_content = "Transaction log not found."
    return log_content

# Main application class
class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Application")

        self.balance = read_balance()
        self.user_password = generate_password()

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()

        self.password_label = tk.Label(self.root, text="Enter User Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Login", command=self.verify_user_password)
        self.login_button.pack()

        self.generated_password_label = tk.Label(self.root, text=f"Generated User Password: {self.user_password}")
        self.generated_password_label.pack()

    def verify_user_password(self):
        entered_password = self.password_entry.get()
        if entered_password == self.user_password:
            messagebox.showinfo("Success", "User login successful.")
            self.show_customer_options()
        else:
            messagebox.showerror("Error", "Incorrect password. Please try again.")
            self.password_entry.delete(0, tk.END)

    def show_customer_options(self):
        self.clear_screen()

        self.balance_label = tk.Label(self.root, text=f"Current balance: R{self.balance}")
        self.balance_label.pack()

        self.transaction_label = tk.Label(self.root, text="Would you like to make a transaction?")
        self.transaction_label.pack()

        self.transaction_button = tk.Button(self.root, text="Make a transaction", command=self.transaction_prompt)
        self.transaction_button.pack()

        self.show_bank_data_button = tk.Button(self.root, text="Show Bank Data", command=self.show_bank_data)
        self.show_bank_data_button.pack()

        self.show_transaction_log_button = tk.Button(self.root, text="Show Transaction Log", command=self.show_transaction_log)
        self.show_transaction_log_button.pack()

    def transaction_prompt(self):
        self.transaction_type_label = tk.Label(self.root, text="Would you like to make a deposit or withdrawal?")
        self.transaction_type_label.pack()

        self.transaction_type = tk.StringVar()
        self.deposit_radio = tk.Radiobutton(self.root, text="Deposit", variable=self.transaction_type, value="deposit",
                                            command=self.deposit_prompt)
        self.deposit_radio.pack()
        self.withdraw_radio = tk.Radiobutton(self.root, text="Withdrawal", variable=self.transaction_type,
                                             value="withdrawal", command=self.withdraw_prompt)
        self.withdraw_radio.pack()

    def deposit_prompt(self):
        self.clear_screen()

        self.amount_label = tk.Label(self.root, text="How much would you like to deposit?")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.confirm_button = tk.Button(self.root, text="Confirm", command=self.make_deposit)
        self.confirm_button.pack()

    def withdraw_prompt(self):
        self.clear_screen()

        self.amount_label = tk.Label(self.root, text="How much would you like to withdraw?")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        self.confirm_button = tk.Button(self.root, text="Confirm", command=self.make_withdrawal)
        self.confirm_button.pack()

    def make_deposit(self):
        amount = self.amount_entry.get()
        self.balance = deposit(self.balance, amount)
        update_bank_data(self.balance)
        self.clear_screen()
        self.show_customer_options()
        self.show_close_button()

    def make_withdrawal(self):
        amount = self.amount_entry.get()
        self.balance = withdraw(self.balance, amount)
        update_bank_data(self.balance)
        self.clear_screen()
        self.show_customer_options()
        self.show_close_button()

    def show_bank_data(self):
        bank_data_content = read_balance()
        messagebox.showinfo("Bank Data", f"Bank Data:\n\n{bank_data_content}")

    def show_transaction_log(self):
        log_content = read_transaction_log()
        messagebox.showinfo("Transaction Log", f"Transaction Log:\n\n{log_content}")

    def show_close_button(self):
        close_button = tk.Button(self.root, text="Close", command=self.root.quit)
        close_button.pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
