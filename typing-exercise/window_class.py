import pickle
import random
import threading
import time
import tkinter as tk

from help_class import Help


class Window:

    def new_text(self):
        self.current_text = random.choice(self.texts_variants)
        while self.current_text == "":
            self.current_text = random.choice(self.texts_variants)
        self.TextLabel.config(text=self.current_text)

    def start_program(self, event):
        if not self.is_active:
            self.is_active = True
            prg = threading.Thread(target=self.timer)
            prg.daemon = True
            prg.start()

    def timer(self):
        self.time_passed = 0
        while self.is_active:
            time.sleep(self.INCREMENT)
            self.time_passed += self.INCREMENT
            self.TimePassedStat.config(text=f"{self.time_passed:.1f} s")
            if not self.time_passed == 0:
                cpm = self.SECONDS * (self.char_count / self.time_passed)
                self.words_per_minute = self.SECONDS * (self.word_counter / self.time_passed)
            else:
                cpm = 0
                self.words_per_minute = 0
            self.CPMStat.config(text=f"CPM: {cpm:.2f}")
            self.WPMStat.config(text=f"WPM: {self.words_per_minute:.2f}")

    def sentence_done(self):
        self.current_character_index = 0
        self.UserInputSpace.delete(0, len(self.current_text))
        self.new_text()
        self.word_counter += 1
        if not self.time_passed == 0:
            self.words_per_minute = self.SECONDS * (self.word_counter / self.time_passed)
        else:
            self.words_per_minute = 0
        self.UserInputSpace.after_idle(lambda: self.UserInputSpace.configure(validate="all"))
        self.WPMStat.config(text=f"WPM: {self.words_per_minute:.2f}")

    def valid_check(self, new_val):
        if len(new_val) == len(self.current_text) and new_val[-1] == self.current_text[self.current_character_index]:
            self.sentence_done()
            return True
        if len(new_val) != 0 and new_val[-1] == self.current_text[self.current_character_index]:
            if new_val[-1] == " ":
                self.word_counter += 1
                if not self.time_passed == 0:
                    self.words_per_minute = self.SECONDS * (self.word_counter / self.time_passed)
                else:
                    self.words_per_minute = 0
                self.WPMStat.config(text=f"WPM: {self.words_per_minute:.2f}")
            self.current_character_index += 1
            self.char_count += 1
            return True
        else:
            self.error_count += 1
            pickle.dump(self.error_count, open("error_log.dat", "wb"))
            self.ErrorsStat.config(text=f"{self.error_count} errors")
            return False

    @staticmethod
    def open_help():
        Help()

    def reset(self):
        self.error_count = 0
        pickle.dump(self.error_count, open("error_log.dat", "wb"))
        self.ErrorsStat.config(text=f"{self.error_count} errors")
        self.current_character_index = 0
        self.check = (self.root.register(self.valid_check), "%P")
        self.UserInputSpace = tk.Entry(self.root, width=80, bg='white', validate="key", validatecommand=self.check)
        self.UserInputSpace.bind("<KeyPress>", self.start_program)
        self.UserInputSpace.place(anchor="n", x=300, y=150)
        self.current_character_index = 0
        self.word_counter = 0
        self.WPMStat.config(text=f"WPM: {self.words_per_minute:.2f}")
        self.new_text()
        self.char_count = 0
        self.time_passed = -0.1
        self.is_active = False

    def __init__(self):
        self.SECONDS = 60
        self.INCREMENT = 0.1
        self.root = tk.Tk()
        self.time_passed = 0
        self.current_character_index = 0
        self.word_counter = 0
        self.error_count = 0
        self.char_count = 0
        self.error_count = pickle.load(open("error_log.dat", "rb"))
        self.texts_variants = open("texts.txt", "r").read().split('\n')
        self.is_active = False
        self.root.title("Typing simulator")
        self.root.geometry("600x400")
        self.root.configure(bg='#050A1A')
        self.current_text = "print('Hello, world!')"
        self.root.resizable(width=False, height=False)
        self.the_above_space = tk.Label(self.root, height=7, text="", bg='#050A1A')
        self.the_above_space.place(anchor="n", x=300, y=50)
        # Widgets:
        self.TextLabel = tk.Label(self.root, text=self.current_text, bg='#050A1A', font=("Arial", 15), fg="white")
        self.TextLabel.place(anchor="n", x=300, y=100)
        self.check = (self.root.register(self.valid_check), "%P")
        self.g = tk.Entry
        self.UserInputSpace = tk.Entry(self.root, width=80, bg='white', validate="key", validatecommand=self.check)
        self.UserInputSpace.bind("<KeyPress>", self.start_program)
        self.UserInputSpace.place(anchor="n", x=300, y=150)
        self.CPMStat = tk.Label(self.root, text="CPM: 0.0", bg='#050A1A', fg="white", font=("Arial", 10))
        self.CPMStat.place(anchor="n", x=300, y=300)
        self.TimePassedStat = tk.Label(self.root, text="0.0 s", bg='#050A1A', fg="white", font=("Arial", 10))
        self.TimePassedStat.place(anchor="n", x=300, y=225)
        self.ErrorsStat = tk.Label(self.root, text=f"{self.error_count} errors", bg='#050A1A', fg="white",
                                   font=("Arial", 10))
        self.ErrorsStat.place(anchor="n", x=300, y=250)
        self.words_per_minute = 0
        self.WPMStat = tk.Label(self.root, text="WPM: 0.0", bg='#050A1A', fg="white", font=("Arial", 10))
        self.WPMStat.place(anchor="n", x=300, y=275)
        self.ResetErrorButton = tk.Button(self.root, text="Reset", bg='#050A1A', fg="white", font=("Arial", 15),
                                          command=self.reset)
        self.ResetErrorButton.place(anchor="n", x=300, y=180)
        self.HelpButton = tk.Button(self.root, text="Help", bg='#050A1A', fg="white", font=("Arial", 10),
                                    command=self.open_help)
        self.HelpButton.place(anchor="n", x=300, y=330)
        self.root.mainloop()
