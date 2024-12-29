from tkinter import *
import pandas as pd
import random
import csv

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
timer = None
to_learn={}


def next_card():
    global current_card, timer
    current_card = random.choice(to_learn)
    if timer:
        window.after_cancel(timer)
    canvas.itemconfig(canvas_image, image=image)
    canvas.itemconfig(title, text="Deutsch", fill="black")
    canvas.itemconfig(word, text=current_card["DEUTSCH"], fill="black")
    #window.after(3000,answer)
    count_down(3)



def is_known():
    global current_card
    to_learn.remove(current_card)
    data=pd.DataFrame(to_learn)
    data.to_csv('data\\words_to_learn.csv',index=False)
    next_card()


def count_down(count):
    global timer
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
        time.config(text=count)
    else:
        time.config(text=count)
        answer()


def answer():
    global current_card
    canvas.itemconfig(canvas_image, image=answ_image)
    canvas.itemconfig(title, text='English', fill="white")
    canvas.itemconfig(word, text=current_card['ENGLISH'], fill="white")


##############################read data###############################

try:
    learn = pd.read_csv('data\\words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data\\german words.csv')
    to_learn=original_data.to_dict(orient='records')
else:
    to_learn = learn.to_dict(orient="records")

#################################UI#####################3
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
time = Label(text='3', font=("Ariel", 50, 'bold'), bg=BACKGROUND_COLOR, fg="white")
time.grid(row=1, column=1, pady=20)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
image = PhotoImage(file='images\\card_front.png')
answ_image = PhotoImage(file='images\\card_back.png')
canvas_image = canvas.create_image(400, 275, image=image)

title = canvas.create_text(400, 150, text="LANGUAGE", font=("Ariel", 50, "italic"))
word = canvas.create_text(400, 263, text="WORD", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=3)

right_image = PhotoImage(file="images\\right.png")
wrong_image = PhotoImage(file='images\\wrong.png')
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=2)
unknown_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

next_card()

window.mainloop()
