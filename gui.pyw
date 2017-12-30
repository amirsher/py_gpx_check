#!/usr/bin/python

from tkinter import *
from subprocess import check_output, Popen, PIPE
from tkinter import messagebox
import webbrowser, os
from tkinter import filedialog

top = Tk()
top.title("Check gpx files")
top.geometry('800x800')

def speeding():
    B2.flash()
    text.delete(1.0,END)
    p = Popen("speeding.py " + E2.get(), stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
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
    text.delete(1.0,END)
    arg = "marshaling.py {3},{4},{5},{1},{2} {0}".format(E1.get(),CheckVar1.get(),CheckVar2.get(),V11.get(),V12.get(),CheckVar3.get())
    print (arg)
    p = Popen(arg , stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
    #p = Popen("marshaling.py 90,120,line,1,1 " + E1.get(), stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
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

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)
    text.insert(END, filename)
    os.chdir(filename)


folder_path = StringVar()
lbl1 = Label(top,textvariable=folder_path, font=("Ariel", "20"))
lbl1.pack()
B3 = Button(top,text="Browse to Directory", command=browse_button, font=("Ariel", "20"), bg="gray", fg="white", bd="4")
B3.pack()

S2 = LabelFrame(top, text="")
S2.pack(padx="20",pady="20")
E2 = Entry(top, bd =5, width=100, font=("Ariel", "20"))
E2.pack(padx="20")
T2 = Label(top, text="30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70")
T2.pack()
B2 = Button(top, text ="speeding", command = speeding, font=("Ariel", "24"), bg="gray", fg="white", bd="5")
B2.pack(padx="20",pady="20")

S1 = LabelFrame(top, text="")
S1.pack(padx="20",pady="10")
E1 = Entry(top, bd =5, width=100, font=("Ariel", "20"))
E1.pack(padx="20")
T1 = Label(top, text="30.195176,35.04978 30.1749997,35.0642141")
T1.pack()
F11 = Frame(top)
T11 = Label(F11, text="distance to marshal allowed (in meters)", font=("Ariel", "12"))
T11.pack(side = LEFT)
V11 = StringVar()
E11 = Entry(F11, textvariable=V11, bd =3, width=4, font=("Ariel", "14"))
E11.pack(side = RIGHT)
V11.set("80")
F11.pack()

F12 = Frame(top)
T12 = Label(F12, text="distance to waypoint allowed (in meters)", font=("Ariel", "12"))
T12.pack(side = LEFT)
V12 = StringVar()
E12 = Entry(F12, textvariable=V12, bd =3, width=4, font=("Ariel", "14"))
E12.pack(side = RIGHT)
V12.set("100")
F12.pack()
CheckVar1 = StringVar()
CheckVar2 = StringVar()
CheckVar3 = StringVar()
C1 = Checkbutton(top, text = "show waypoints", variable = CheckVar1, onvalue = "yes", offvalue = "no", width = 20, font=("Ariel", "12"))
C2 = Checkbutton(top, text = "show waypoints line", variable = CheckVar2, onvalue = "yes", offvalue = "no", width = 20, font=("Ariel", "12"))
C3 = Checkbutton(top, text = "show all track points (very slow!)", variable = CheckVar3, onvalue = "points", offvalue = "line", width = 30, font=("Ariel", "12"))
C1.deselect()
C2.deselect()
C3.deselect()
C1.pack()
C2.pack()
C3.pack()
B1 = Button(top, text ="marshaling", command = marshaling, font=("Ariel", "24"), bg="gray", fg="white", bd="5")
B1.pack(padx="20",pady="20")

T3 = Label(top, text="console")
T3.pack()
text = Text(top)
text.pack(padx="20",pady="10")
top.mainloop()