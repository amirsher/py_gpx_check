#!/usr/bin/python

from tkinter import *
from subprocess import check_output, Popen, PIPE
from tkinter import messagebox
import webbrowser, os

top = Tk()
top.title("Check gpx files")
top.geometry('800x600')

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

S2 = LabelFrame(top, text="")
S2.pack(padx="20",pady="20")
E2 = Entry(top, bd =5, width=100, font=("Ariel", "20"))
E2.pack(padx="20")
T2 = Label(top, text="30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70")
T2.pack()
B2 = Button(top, text ="speeding", command = speeding, font=("Ariel", "24"), bg="gray", fg="white", bd="5")
B2.pack(padx="20",pady="20")

S1 = LabelFrame(top, text="")
S1.pack(padx="20",pady="20")
E1 = Entry(top, bd =5, width=100, font=("Ariel", "20"))
E1.pack(padx="20")
T1 = Label(top, text="30.195176,35.04978 30.1749997,35.0642141")
T1.pack()
B1 = Button(top, text ="marshaling", command = marshaling, font=("Ariel", "24"), bg="gray", fg="white", bd="5")
B1.pack(padx="20",pady="20")
text = Text(top,height=25)
text.pack()
top.mainloop()
