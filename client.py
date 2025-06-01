import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import socket

HOST = '127.0.0.1'
PORT = 9090

def send_command(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(command.encode())
            return s.recv(4096).decode()
    except:
        return "ERROR"

class AuthWindow:
    def __init__(self, master):
        self.master = master
        master.title("HabitMaster - Login")
        master.geometry("300x200")

        self.username_label = tk.Label(master, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        self.password_label = tk.Label(master, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(master, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(master, text="Register", command=self.register)
        self.register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        response = send_command(f"LOGIN|{username}|{password}")
        if response != "FAIL" and response != "ERROR":
            user_id = int(response)
            self.master.destroy()
            open_main_window(user_id)
        else:
            messagebox.showerror("Error", "Login failed")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        response = send_command(f"REGISTER|{username}|{password}")
        if response == "OK":
            messagebox.showinfo("Success", "Registered successfully!")
        else:
            messagebox.showerror("Error", "Registration failed")

# --- Main Habit Tracker Window ---
class HabitWindow:
    def __init__(self, master, user_id):
        self.master = master
        self.user_id = user_id
        master.title("HabitMaster - Dashboard")
        master.geometry("500x400")

        self.label = tk.Label(master, text=f"User ID: {user_id}", font=("Arial", 12))
        self.label.pack(pady=10)

        self.habit_list = tk.Listbox(master, width=50)
        self.habit_list.pack(pady=10)

        self.refresh_button = tk.Button(master, text="Refresh Habits", command=self.load_habits)
        self.refresh_button.pack()

        self.add_button = tk.Button(master, text="Add Habit", command=self.add_habit)
        self.add_button.pack()

        self.done_button = tk.Button(master, text="Mark as Done", command=self.mark_done)
        self.done_button.pack()

        self.stats_button = tk.Button(master, text="View Stats", command=self.view_stats)
        self.stats_button.pack()

        self.change_button = tk.Button(master, text="Change Habit", command=self.change_habit)
        self.change_button.pack()

        self.delete_button = tk.Button(master, text="Delete Habit", command=self.delete_habit)
        self.delete_button.pack()

        self.load_habits()

    def load_habits(self):
        response = send_command(f"GET_HABITS|{self.user_id}")
        self.habit_list.delete(0, tk.END)
        if response.startswith("HABITS|"):
            habits = response.split("|")[1:]
            for habit in habits:
                self.habit_list.insert(tk.END, habit)

    def add_habit(self):
        name = simpledialog.askstring("Add Habit", "Enter habit name:")
        if name:
            res = send_command(f"ADD_HABIT|{self.user_id}|{name}")
            if res == "OK":
                self.load_habits()
            else:
                messagebox.showerror("Error", "Failed to add habit.")

    def mark_done(self):
        selection = self.habit_list.curselection()
        if selection:
            habit_line = self.habit_list.get(selection[0])
            habit_id = habit_line.split(":")[0]
            response = send_command(f"MARK_DONE|{habit_id}")
            if response == "OK":
                messagebox.showinfo("Done", "Habit marked as done.")
            else:
                messagebox.showerror("Error", "Failed to mark as done.")

    def view_stats(self):
        selection = self.habit_list.curselection()
        if selection:
            habit_line = self.habit_list.get(selection[0])
            habit_id = habit_line.split(":")[0]
            stats = send_command(f"GET_STATS|{habit_id}")
            messagebox.showinfo("Statistics", stats)

    def change_habit(self):
        selection = self.habit_list.curselection()
        if selection:
            habit_line = self.habit_list.get(selection[0])
            habit_id = habit_line.split(":")[0]
            new_name = simpledialog.askstring("Change Habit", "Enter new habit name:")
            if new_name:
                response = send_command(f"CHANGE_HABIT|{habit_id}|{new_name}")
                if response == "OK":
                    self.load_habits()
                else:
                    messagebox.showerror("Error", "Failed to change habit.")
        else:
            messagebox.showerror("Error", "Select a habit to change.")

    def delete_habit(self):
        selection = self.habit_list.curselection()
        if selection:
            habit_line = self.habit_list.get(selection[0])
            habit_id = habit_line.split(":")[0]
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this habit?")
            if confirm:
                response = send_command(f"DELETE_HABIT|{habit_id}")
                if response == "OK":
                    self.load_habits()
                else:
                    messagebox.showerror("Error", "Failed to delete habit.")
        else:
            messagebox.showerror("Error", "Select a habit to delete.")


def open_main_window(user_id):
    main = tk.Tk()
    app = HabitWindow(main, user_id)
    main.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthWindow(root)
    root.mainloop()
