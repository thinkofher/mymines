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

    def set_new_game_text(self, text):
        self.new_game.config(text=text)


class Mines(tk.Frame):
    def __init__(self, game, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self._game = game
        self.gen_buttons()

    def gen_buttons(self):
        """
        Generate matrix of buttons
        """
        for cords in self._game._cells_dict:
            self.gen_button_from_cords(cords)

    def gen_button_from_cords(self, cords):
        """
        Generate signle button based on given cords
        and their properties in game
        """
        label = self._game._cells_dict[cords].get_label()

        # checking game status
        is_won = self._game.is_won()
        is_loss = self._game.is_loss()

        # sending information to master about game status
        if is_won:
            self.master.top_frame.set_new_game_text('You Won!')
        if is_loss:
            self.master.top_frame.set_new_game_text('You loss!')

        curr_button = tk.Button(self, height=1, width=1)

        # buttons style depends on cell label
        if label == mine.HIDDEN:
            state = tk.NORMAL
            relief = tk.RAISED
            text = ''
            curr_button.config(state=state, relief=relief, text=text)
        elif label == mine.EMPTY:
            state = tk.NORMAL
            relief = tk.SUNKEN
            text = ''
            curr_button.config(state=state, relief=relief, text=text)
        elif label == mine.FLAGGED:
            state = tk.NORMAL
            relief = tk.RAISED
            text = 'f'
            curr_button.config(state=state, relief=relief, text=text)
        elif label == mine.BOMB:
            state = tk.NORMAL
            relief = tk.SUNKEN
            text = 'x'
            curr_button.config(state=state, relief=relief, text=text)
        else:
            state = tk.NORMAL
            relief = tk.SUNKEN
            text = label
            curr_button.config(state=state, relief=relief, text=text)

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

        curr_button.bind('<Button-1>', left_click_func)
        curr_button.bind('<Button-2>', middle_click_func)
        curr_button.bind('<Button-3>', right_click_func)
        curr_button.grid(row=cords[0], column=cords[1])


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Python Mines")
        self._set_diff_levels()
        self._create_widgets()
        self._create_menubar()

    def start_new_game(self):
        self.mines_field.destroy()
        self.top_frame.set_new_game_text('New Game')
        self._init_game()
        self.mines_field = Mines(self._game, master=self)

    def _init_game(self):
        """
        Initialize new game based on difficulty level
        """
        diff_tuple = self._diff_levels[self._diff_level.get()]
        self._game = mine.MineGameField(
            diff_tuple[0], diff_tuple[1], diff_tuple[2])

    def _create_widgets(self):
        self.top_frame = TopFrame(self)
        self._init_game()
        self.mines_field = Mines(self._game, master=self)
        self.top_frame.set_new_game_command(self.start_new_game)

    def _set_diff_levels(self):
        """
        Sets fields with difficulty levels dictionary,
        containing their properties, and default difficulty
        level
        """
        self._diff_level = tk.StringVar()

        # tuple content is 0: width, 1: height, 2: n_of_bombs
        self._diff_levels = {
            'Easy': (8, 8, 10),
            'Medium': (16, 16, 40),
            'Hard': (30, 16, 99)
        }

        # default difficulty level
        self._diff_level.set('Easy')

    def _set_diff_level_func(self, var):
        """
        Returns func which sets given difficulty level
        and starts new game
        """
        def set_func():
            self._diff_level.set(var)
            self.start_new_game()
        return set_func

    def _create_menubar(self):
        menubar = tk.Menu(self)

        gamemenu = tk.Menu(menubar, tearoff=0)
        gamemenu.add_command(label='New Game', command=self.start_new_game)
        gamemenu.add_command(label='Exit', command=self.quit)
        menubar.add_cascade(label='Game', menu=gamemenu)

        difficulty = tk.Menu(menubar, tearoff=0)
        for var in self._diff_levels:
            difficulty.add_command(label=var,
                                   command=self._set_diff_level_func(var))
        menubar.add_cascade(label='Difficulty', menu=difficulty)

        self.config(menu=menubar)


if __name__ == '__main__':
    root = Application()
    root.mainloop()
