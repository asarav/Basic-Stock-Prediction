import training.train as Train
from tkinter import *
import subprocess as sub

# Generate a Buy or Sell Recommendation based on current properties of the stock
window = Tk()

window.title("Stock Prediction")

window.geometry('480x480')

lbl = Label(window, text="Ticker Symbol")
lbl.grid(column=0, row=0)
txt = Entry(window,width=10)
txt.grid(column=1, row=0)

chkValue = BooleanVar()
chk = Checkbutton(window, text='Process All Quotes', variable=chkValue)
chk.grid(column=0, row=1)
chk.select()

chkValue2 = BooleanVar()
chk2 = Checkbutton(window, text='Display Comparison Graph', variable=chkValue2)
chk2.grid(column=0, row=2)

output = Label(window)
output.grid(column=0, row=4)

def done():
    print("DONE")

def clicked():
    window.title("Stock Prediction (Processing)")
    train = None
    if bool(chkValue.get()):
        train = Train.Train(printGraph=bool(chkValue2.get()))
    else:
        quote = txt.get()
        callback=None
        if bool(chkValue2.get()):
            callback = done
        train = Train.Train(quote=quote, printGraph=bool(chkValue2.get()), callback=callback)
    done()

btn = Button(window, text="Generate Prediction", command=clicked)
btn.grid(column=0, row=3)

window.mainloop()