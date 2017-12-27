#!/usr/bin/python

from tkinter import *
from subprocess import check_output, Popen, PIPE
from tkinter import messagebox
import webbrowser, os

top = Tk()
top.title("Check gpx files")


def speeding():
    B2.flash()
    p = Popen("python speeding.py " + E2.get(), stdout=PIPE, shell=True, universal_newlines=True)
    while True:
        retcode = p.poll()
        output = p.stdout.readline()
        print(output)
        text.insert(END, output)
        if retcode is not None:
            break
    text.insert(END, "\n")

    filename = "SpeedingMap.html"
    result = messagebox.askquestion("Results", "Show results in web browser?")
    if result == 'yes':
        webbrowser.open('file://' + os.path.realpath(filename))
    else:
        messagebox.showinfo("Information","saved results to " + filename)
    
def marshaling():
    B1.flash()
    p = Popen("python marshaling.py " + E1.get(), stdout=PIPE, shell=True, universal_newlines=True)
    while True:
        retcode = p.poll()
        output = p.stdout.readline()
        print(output)
        text.insert(END, output)
        if retcode is not None:
            break
    text.insert(END, "\n")

    filename = "TrackingMap.html"
    result = messagebox.askquestion("Results", "Show results in web browser?")
    if result == 'yes':
        webbrowser.open('file://' + os.path.realpath(filename))
    else:
        messagebox.showinfo("Information","saved results to " + filename)

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
