import training.train as Train
from tkinter import *

def clicked():
    train = Train.Train()

# Generate a Buy or Sell Recommendation based on current properties of the stock
window = Tk()

window.title("Stock Prediction")

window.geometry('480x320')

lbl = Label(window, text="Ticker Symbol")
lbl.grid(column=0, row=0)
txt = Entry(window,width=10)
txt.grid(column=1, row=0)

chk = Checkbutton(window, text='Process All Quotes')
chk.grid(column=0, row=1)
chk2 = Checkbutton(window, text='Display Comparison Graph')
chk2.grid(column=0, row=2)
btn = Button(window, text="Generate Prediction", command=clicked)
btn.grid(column=0, row=3)
window.mainloop()