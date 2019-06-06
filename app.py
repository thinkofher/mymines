import tkinter as tk
import mine


class TopFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.set_new_game_button()

    def set_new_game_button(self):
        self.new_game = tk.Button(self, text="New Game")
        self.new_game.pack(side="top", padx=10, pady=10)

    def set_new_game_command(self, func):
        self.new_game.config(command=func)

    def say_hi(self):
        print("hi there, everyone!")


class Mines(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.gen_buttons()

    def gen_buttons(self):

        field = mine.gen_field_matrix()
        field = mine.fill_with_bombs(field, 6)
        field = mine.numbering_field(field)
        # width, heigth = len(field[0]), len(field)

        for i, row in enumerate(field):
            for j, cell in enumerate(row):
                tk.Button(self, text=f'{str(cell)}', height=1, width=1).grid(
                    row=i, column=j)


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Python Mines")
        self.create_widgets()

    def create_widgets(self):
        self.top_frame = TopFrame(self)
        self.mines_field = Mines(self)
        self.top_frame.set_new_game_command(self.start_new_game)

    def start_new_game(self):
        self.mines_field.destroy()
        self.mines_field = Mines(self)


root = Application()
# app = TopFrame(master=root)
# mines = Mines(master=root)
root.mainloop()
