import os, sys
import tkinter as tk
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.general import check_game_state
from logic.general import transpose_board

STATE_CHOOSING = 1
STATE_THINKING = 2
STATE_WIN_DISPLAY = 3

STATE_YOU_FIRST = 1
STATE_COM_FIRST = 2


class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, move_function, **kwargs):
        self.bg = "grey"
        kwargs.setdefault("bg", self.bg)
        tk.Canvas.__init__(self, parent, **kwargs)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.move_function = move_function

        self.color = "#222222"
        self.linewidth = 3
        self.rows = 3

        self.gamestate = STATE_CHOOSING
        self.beginner = STATE_COM_FIRST
        self.matrix = np.zeros((self.rows, self.rows))

        self.bind("<Configure>", self.resize)
        self.bind("<ButtonRelease-1>", self.handle_click)

        self.fill_from_matrix()

    def fill_from_matrix(self):
        self.clear()

        # test matrix shape
        if self.matrix.shape != (self.rows, self.rows):
            exit()

        cell_width = self.width / self.rows
        cell_height = self.height / self.rows
        padding_factor = 0.2
        cell_width_padding = self.width / self.rows * padding_factor
        cell_height_padding = self.height / self.rows * padding_factor

        for row in range(0, self.rows):
            for column in range(0, self.rows):
                if self.matrix[row][column] == 1:
                    # draw cross
                    self.create_line(
                        cell_width * column + cell_width_padding,
                        cell_height * row + cell_height_padding,
                        cell_width * (column + 1) - cell_width_padding,
                        cell_height * (row + 1) - cell_height_padding,
                        fill=self.color,
                        width=self.linewidth,
                    )
                    self.create_line(
                        cell_width * column + cell_width_padding,
                        cell_height * (row + 1) - cell_height_padding,
                        cell_width * (column + 1) - cell_width_padding,
                        cell_height * row + cell_height_padding,
                        fill=self.color,
                        width=self.linewidth,
                    )
                elif self.matrix[row][column] == 2:
                    # draw circle
                    self.create_oval(
                        cell_width * column + cell_width_padding,
                        cell_height * row + cell_height_padding,
                        cell_width * (column + 1) - cell_width_padding,
                        cell_height * (row + 1) - cell_height_padding,
                        outline=self.color,
                        width=self.linewidth,
                    )
                else:
                    # nothing is drawn
                    pass

    def handle_click(self, event):
        click_row, click_column = self.translate_to_indicees(event.x, event.y)

        # check for game finish
        if self.gamestate == STATE_WIN_DISPLAY:
            # re-init
            self.matrix = np.zeros((self.rows, self.rows))
            self.fill_from_matrix()

            # set next state
            if self.beginner == STATE_YOU_FIRST:
                self.gamestate = STATE_CHOOSING
                self.beginner = STATE_COM_FIRST

                # wait for another click here
                return
            elif self.beginner == STATE_COM_FIRST:
                self.gamestate = STATE_THINKING
                self.beginner = STATE_YOU_FIRST

        # player move
        if self.gamestate == STATE_CHOOSING:
            if self.matrix[click_row][click_column] == 0:
                self.matrix[click_row][click_column] = 1
                self.fill_from_matrix()

                game_code = check_game_state(self.matrix)
                if game_code == 1 or game_code == 2 or game_code == 3:
                    self.gamestate = STATE_WIN_DISPLAY
                elif game_code == 0:
                    self.gamestate = STATE_THINKING

        # ai move
        if self.gamestate == STATE_THINKING:
            # transpose so that ai has right setup
            transpose_board(self.matrix)
            # make ai move
            self.move_function(self.matrix)
            # transpose back into player setup
            transpose_board(self.matrix)
            # render
            self.fill_from_matrix()

            game_code = check_game_state(self.matrix)
            if game_code == 1 or game_code == 2 or game_code == 3:
                self.gamestate = STATE_WIN_DISPLAY
            elif game_code == 0:
                self.gamestate = STATE_CHOOSING

        # check for game finish (print winner/loser)
        if self.gamestate == STATE_WIN_DISPLAY:
            game_code = check_game_state(self.matrix)
            if game_code == 1:
                print("X has won!")
            elif game_code == 2:
                print("O has won!")
            elif game_code == 3:
                print("Draw.")

    def translate_to_indicees(self, x, y):
        cell_width = self.width / self.rows
        cell_height = self.height / self.rows

        click_row = 0
        for row in range(1, self.rows):
            if y >= cell_height * row and y < cell_height * (row + 1):
                click_row = row

        click_column = 0
        for column in range(1, self.rows):
            if x >= cell_width * column and x < cell_width * (column + 1):
                click_column = column

        return (click_row, click_column)

    def clear(self):
        self.delete("all")
        self.init_grid()

    def init_grid(self):
        for i in range(1, self.rows):
            self.create_line(
                self.width / self.rows * i,
                0,
                self.width / self.rows * i,
                self.height,
                width=self.linewidth,
                fill=self.color,
            )
            self.create_line(
                0,
                self.height / 3 * i,
                self.width,
                self.height / 3 * i,
                width=self.linewidth,
                fill=self.color,
            )

    def resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)


def main(move_function):
    canvas_width = 500
    canvas_height = 500

    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    myframe = tk.Frame(root)
    myframe.pack(fill=tk.BOTH, expand=tk.YES)

    mycanvas = ResizingCanvas(
        myframe,
        move_function=move_function,
        width=canvas_width,
        height=canvas_height,
        highlightthickness=0,
    )
    mycanvas.pack(fill=tk.BOTH, expand=tk.YES)

    # message = tk.Label(root, text="Tic-Tac-Toe display")
    # message.pack(side=tk.BOTTOM)

    # tag all of the drawn widgets (later reference)
    mycanvas.addtag_all("all")

    # main draw loop
    root.mainloop()