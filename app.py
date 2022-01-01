from tkinter import *
from button import Btn


class App(Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Quiz Game')
        self.wm_iconbitmap('quiz.ico')

        self.mainloop()
