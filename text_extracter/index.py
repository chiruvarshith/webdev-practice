import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SetupWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sample Setup Wizard")
        self.geometry("400x300")
        self.frames = {}

        for F in (WelcomePage, LicensePage, InstallLocationPage, CompletePage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Welcome to the Sample Setup Wizard", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=20)

        next_button = ttk.Button(self, text="Next", command=lambda: controller.show_frame("LicensePage"))
        next_button.pack(side="right", padx=10, pady=10)

class LicensePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="License Agreement", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=10)

        license_text = tk.Text(self, height=10, wrap="word")
        license_text.insert("1.0", "Please read the following license agreement...")
        license_text.config(state=tk.DISABLED)
        license_text.pack(fill="both", expand=True)

        self.accept_var = tk.BooleanVar()
        accept_check = ttk.Checkbutton(self, text="I accept the terms of the agreement", variable=self.accept_var)
        accept_check.pack()

        self.option_var1 = tk.BooleanVar()
        option_check1 = ttk.Checkbutton(self, text="Option 1", variable=self.option_var1)
        option_check1.pack()

        self.option_var2 = tk.BooleanVar()
        option_check2 = ttk.Checkbutton(self, text="Option 2", variable=self.option_var2)
        option_check2.pack()

        button_frame = ttk.Frame(self)
        button_frame.pack(side="bottom", fill="x", pady=10)

        prev_button = ttk.Button(button_frame, text="Previous", command=lambda: controller.show_frame("WelcomePage"))
        prev_button.pack(side="left", padx=10)

        next_button = ttk.Button(button_frame, text="Next", command=self.next_page)
        next_button.pack(side="right", padx=10)

    def next_page(self):
        if self.accept_var.get():
            self.controller.show_frame("InstallLocationPage")
        else:
            messagebox.showwarning("License Agreement", "You must accept the license agreement to proceed.")

class InstallLocationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Choose Installation Location", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=10)

        self.install_path = tk.StringVar()
        path_entry = ttk.Entry(self, textvariable=self.install_path, width=40)
        path_entry.pack()

        browse_button = ttk.Button(self, text="Browse", command=self.browse_folder)
        browse_button.pack()

        button_frame = ttk.Frame(self)
        button_frame.pack(side="bottom", fill="x", pady=10)

        prev_button = ttk.Button(button_frame, text="Previous", command=lambda: controller.show_frame("LicensePage"))
        prev_button.pack(side="left", padx=10)

        next_button = ttk.Button(button_frame, text="Next", command=lambda: controller.show_frame("CompletePage"))
        next_button.pack(side="right", padx=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.install_path.set(folder_selected)

class CompletePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Installation Complete", font=("Helvetica", 16))
        label.pack(side="top", fill="x", pady=20)

        complete_label = ttk.Label(self, text="The software has been successfully installed.")
        complete_label.pack()

        button_frame = ttk.Frame(self)
        button_frame.pack(side="bottom", fill="x", pady=10)

        finish_button = ttk.Button(button_frame, text="Finish", command=self.show_success)
        finish_button.pack(side="left", padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancel Installation", command=self.cancel_installation)
        cancel_button.pack(side="right", padx=10)

    def show_success(self):
        messagebox.showinfo("Installation", "Installed successfully")
        self.controller.quit()

    def cancel_installation(self):
        if messagebox.askokcancel("Cancel Installation", "Are you sure you want to cancel the installation?"):
            messagebox.showinfo("Installation", "Installation cancelled")
            self.controller.quit()

if __name__ == "__main__":
    app = SetupWizard()
    app.mainloop()
