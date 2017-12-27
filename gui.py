#!/usr/bin/python

from tkinter import *
from subprocess import call, Popen, PIPE
from tkinter import messagebox

top = Tk()
top.title("Check gpx files")


def speeding():
    B2.flash()
    p = Popen("python speeding.py " + E2.get(), shell=True, stdout=PIPE)
    output = p.communicate()
    text.insert(END, output)

    messagebox.showinfo("Information","Finished checking speeding")
    
def marshaling():
    B1.flash()
    p = Popen("python marshaling.py " + E1.get(), shell=True, stdout=PIPE)
    output = p.communicate()
    text.insert(END, output)

    messagebox.showinfo("Information","Finished checking marshaling")

E2 = Entry(top, bd =5, width=100, font=("Ariel", "28"))
E2.pack()
T2 = Label(top, text="30.195176,35.04978 30.1749997,35.0642141 40 30.195176,35.04978 30.1749997,35.0642141 70")
T2.pack()
B2 = Button(top, text ="speeding", command = speeding, font=("Ariel", "28"))
B2.pack()

E1 = Entry(top, bd =5, width=100, font=("Ariel", "28"))
E1.pack()
T1 = Label(top, text="30.195176,35.04978 30.1749997,35.0642141")
T1.pack()
B1 = Button(top, text ="marshaling", command = marshaling, font=("Ariel", "28"))
B1.pack()
text = Text(top,height=25)
text.pack()
top.mainloop()
