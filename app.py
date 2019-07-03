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
            self.gen_button_from_cords(cords)

    def gen_button_from_cords(self, cords):
        label = self._game._cells_dict[cords].get_label()

        if label == mine.HIDDEN:
            state = tk.NORMAL
            relief = tk.RAISED
            text = ''
        elif label == mine.EMPTY:
            state = tk.NORMAL
            relief = tk.SUNKEN
            text = ''
        elif label == mine.FLAGGED:
            state = tk.NORMAL
            relief = tk.RAISED
            text = 'f'
        else:
            state = tk.NORMAL
            relief = tk.SUNKEN
            text = label

        def left_click_func(event):
            """
            Helper func for left mouse click event
            """
            if is_won or is_loss:
                pass
            else:
                self._game.player_check(cords)
                self.gen_buttons()

        def right_click_func(event):
            """
            Helper func for right mouse click event
            """
            if is_won or is_loss:
                pass
            else:
                self._game.player_check_arround(cords)
                self.gen_buttons()

        def middle_click_func(event):
            """
            Helper func for middle mouse click event
            """
            if is_won or is_loss:
                pass
            else:
                self._game.toggle_flag(cords)
                self.gen_buttons()

        curr_button = tk.Button(self, text=text, height=1, width=1,
                                state=state, relief=relief)
        curr_button.bind('<Button-1>', left_click_func)
        curr_button.bind('<Button-2>', middle_click_func)
        curr_button.bind('<Button-3>', right_click_func)
        curr_button.grid(row=cords[0], column=cords[1])


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
