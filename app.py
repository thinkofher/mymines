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
        self.init_game()
        self.gen_buttons()

    def init_game(self):
        self._game = mine.MineGameField()

    def gen_buttons(self):

        for cords in self._game._cells_dict:
            text_string = self._game._cells_dict[cords].get_true_label()
            tk.Button(self, text=text_string, height=1, width=1,
                      state=tk.DISABLED, relief=tk.SUNKEN).grid(
                          row=cords[0], column=cords[1])


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


if __name__ == '__main__':
    root = Application()
    root.mainloop()
