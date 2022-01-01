from button import Btn
import requests
from tkinter import *
from functools import partial
from score import Score
import html
import time

category_id = None
FONT = ('Open Sans', 10)
BG = '#375362'
FG = '#ffffff'
answer = ''

def get_id(aid):
    global category_id
    category_id = aid
    start_screen.destroy()
    get_question()


def get_question():
    global answer
    response = requests.get(f'https://opentdb.com/api.php?amount=1&category={category_id}&type=boolean')
    response.raise_for_status()
    quiz_db = response.json()
    question = html.unescape(quiz_db['results'][0]['question'])
    answer = quiz_db['results'][0]['correct_answer']
    question_label.configure(text=question, bg='#ffffff')


def check_answer(guess):
    global answer
    if guess == answer:
        update_score()
        get_question()
    else:
        get_question()


def update_score():
    global score
    score += 1
    score_label['text'] = f"Score: {score}"


score = 0
root = Tk()
root.title('Quiz Game')
root.wm_iconbitmap('quiz.ico')
root.configure(bg=BG, padx=20, pady=20)

score_label = Label(root, text=f'Score: {score}', bg=BG, fg=FG, font=FONT)
score_label.pack(side='top')

question_label = Label(root, text='', fg=BG, font=('Open Sans', 15, 'bold'), wraplength=300, justify='center')
question_label.pack(ipadx=30, ipady=50)

trueImg = PhotoImage(file='true.png')
trueHoverImg = PhotoImage(file='true-hover.png')

falseImg = PhotoImage(file='false.png')
falseHoverImg = PhotoImage(file='false-hover.png')

true_button = Btn(root, trueImg, trueHoverImg, borderwidth=0,
                  highlightthickness=0, highlightbackground=BG, command=lambda: check_answer('True'))
true_button.pack(side='right', padx=10, pady=10, anchor='se')

false_button = Btn(root, falseImg, falseHoverImg, borderwidth=0, highlightthickness=0, highlightbackground=BG, command=lambda: check_answer('False'))
false_button.pack(side='left', padx=10, pady=10, anchor='sw')


start_screen = Tk()
start_screen.title('Select Category')
start_screen.configure(bg=BG, padx=20, pady=20)
start_screen.wm_iconbitmap('quiz.ico')

select_cat = Label(start_screen, text='Select A Category:', fg='#ffffff', font=('Open Sans', 13, 'bold'), bg=BG)
select_cat.pack()

categories = requests.get('https://opentdb.com/api_category.php')
categories.raise_for_status()
names = categories.json()['trivia_categories']

for name in names:
    name = Button(start_screen, text=f'{name["name"]}', command=partial(get_id, name['id']),
                  borderwidth=0, font=FONT, fg='#ffffff',
                  bg=BG, activeforeground='#cccccc', activebackground=BG)
    name.pack()


root.mainloop()
