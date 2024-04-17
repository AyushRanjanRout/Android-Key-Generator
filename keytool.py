import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
from ttkthemes import ThemedTk

class KeystoreGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("Android Keystore Generator")
        master.geometry("450x400")
        master.resizable(True, True)

        self.main_frame = ttk.Frame(master, padding=20)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(self.main_frame, text="Android Keystore Generator", font=("Helvetica", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        entries = [
            ("Keystore File Path:", 0),
            ("Alias:", 1),
            ("Password:", 2),
            ("Validity (years):", 3),
            ("First Name:", 4),
            ("Last Name:", 5)
        ]

        self.inputs = {}
        for label_text, row in entries:
            label = ttk.Label(self.main_frame, text=label_text)
            label.grid(row=row+1, column=0, sticky="w", pady=(10, 5))
            entry = ttk.Entry(self.main_frame, width=20 if label_text != "Keystore File Path:" else 30)
            entry.grid(row=row+1, column=1, columnspan=2, sticky="ew", pady=(10, 5))
            self.inputs[label_text] = entry

        self.browse_button = ttk.Button(self.main_frame, text="Browse", command=self.browse_keystore_path)
        self.browse_button.grid(row=1, column=3, pady=(0, 5))

        self.generate_button = ttk.Button(self.main_frame, text="Generate Keystore", command=self.generate_keystore)
        self.generate_button.grid(row=7, column=1, columnspan=2, pady=(20, 0), sticky="ew")

    def browse_keystore_path(self):
        filename = filedialog.asksaveasfilename(defaultextension=".jks", filetypes=(("Java Keystore files", "*.jks"), ("All files", "*.*")))
        if filename:
            self.inputs["Keystore File Path:"].delete(0, tk.END)
            self.inputs["Keystore File Path:"].insert(tk.END, filename)

    def generate_keystore(self):
        inputs = {key: entry.get() for key, entry in self.inputs.items()}

        for key, value in inputs.items():
            if not value:
                messagebox.showerror("Error", f"Please fill in {key}.")
                return

        if len(inputs["Password:"]) < 6:
            messagebox.showerror("Error", "Key password must be at least 6 characters.")
            return

        try:
            validity_years = int(inputs["Validity (years):"])
            if validity_years <= 0 or validity_years > 100:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Validity must be a positive integer less than or equal to 100.")
            return

        threading.Thread(target=self.generate_keystore_thread, args=(inputs,)).start()

    def generate_keystore_thread(self, inputs):
        try:
            subprocess.run([
                'keytool', '-genkey', '-v', '-keystore', inputs["Keystore File Path:"],
                '-alias', inputs["Alias:"], '-keyalg', 'RSA', '-keysize', '2048',
                '-validity', str(int(inputs["Validity (years):"]) * 365), '-storepass',
                inputs["Password:"], '-keypass', inputs["Password:"],
                '-dname', f'CN={inputs["First Name:"]} {inputs["Last Name:"]}, OU=Unknown, O=Unknown, L=Unknown, S=Unknown, C=Unknown',
                '-storetype', 'JKS'
            ], check=True)
            messagebox.showinfo("Success", "Keystore generated successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to generate keystore: {e}")

def main():
    root = ThemedTk(theme="arc")
    app = KeystoreGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
