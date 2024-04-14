import tkinter as tk


class Help:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing help")
        self.root.geometry("700x250")
        self.root.configure(bg='#050A1A')
        self.root.resizable(width=False, height=False)
        self.help_text = tk.Label(self.root, text=open("help_text.txt", "r").read(), fg="white", bg="#050A1A",
                                  font=("Arial", 14), wraplength=700, justify="center")
        self.help_text.pack()
        self.quit_button = tk.Button(self.root, text="Understood", fg="white", bg="#050A1A", command=self.root.destroy,
                                     font=("Arial", 13))
        self.quit_button.pack()
        self.root.mainloop()
