import wx
import mine


class MinePanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        new_game_button = wx.Button(self, label='😎', size=wx.Size(40, 40))
        # main_sizer.Add(new_game_button, 0, wx.ALL | wx.CENTER, 5)

        field = mine.gen_field_matrix()
        field = mine.fill_with_bombs(field, 6)
        field = mine.numbering_field(field)
        self.mine_sizer = MineSizer(self, field)

        new_game_button.Bind(
            wx.EVT_BUTTON, self.mine_sizer.rearange_bombs_randomly)
        main_sizer.Add(new_game_button, 0, wx.ALL | wx.CENTER, 5)
        main_sizer.Add(self.mine_sizer, 1, wx.CENTER)
        self.SetSizer(main_sizer)


class MineSizer(wx.GridSizer):

    def __init__(self, parent, mine_field, vgap=0, hgap=0):
        self.mine_field = mine_field
        self.parent = parent
        columns, rows = len(self.mine_field[0]), len(self.mine_field)
        super().__init__(rows, columns, vgap, hgap)
        self.init_bomb_field()

    def init_bomb_field(self):
        self.Clear()
        for row in self.mine_field:
            for cell in row:
                self.Add(
                    wx.Button(self.parent, label=str(cell),
                              size=wx.Size(20, 20)),
                    0, wx.ALL | wx.ALIGN_TOP, 5)

    def rearange_bombs_randomly(self, event):
        self.Clear()
        self.mine_field = mine.fill_with_bombs(self.mine_field, 6)
        self.mine_field = mine.numbering_field(self.mine_field)
        for row in self.mine_field:
            for cell in row:
                self.Add(
                    wx.Button(self.parent, label=str(cell),
                              size=wx.Size(20, 20)),
                    0, wx.ALL | wx.ALIGN_TOP, 5
                )


class MineFrame(wx.Frame):

    def __init__(self):
        super().__init__(parent=None,
                         title='Python Mines')
        self.panel = MinePanel(self)
        self.Show()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MineFrame()
    app.MainLoop()
