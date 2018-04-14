#!/usr/bin/python

from tkinter import *
from subprocess import check_output, Popen, PIPE
from tkinter import messagebox
import webbrowser, os
from tkinter import filedialog

top = Tk()
top.title("Check gpx files")
top.geometry('800x1000')

def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        e.widget.focus()

        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
               ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd, font=("Ariel", "12"))

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")

    except TclError:
        pass

    return "break"


def rClickbinder(r):

    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except TclError:
        pass


def speeding():
    B2.flash()
    text.delete(1.0,END)
    text1.delete(1.0,END)
    text.insert(END, "console\n")
    text1.insert(END, "warnings\n")
    top.update_idletasks()
    arg = "speeding.py {1},{2},{3},{4},{5} {0}".format(E2.get(),V21.get(),V22.get(),CheckVar21.get(),CheckVar22.get(),CheckVar23.get())
    p = Popen(arg , stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
    #p = Popen("speeding.py " + E2.get(), stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
    finished = 0
    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() != None: break
        print(output)
        if "WARNING" in output: 
             text1.insert(END, output+"\n")
        text.insert(END, output)
        top.update_idletasks()
        if "a.ok" in output:
            finished =  1
    if finished == 1 :
        filename = "SpeedingMap.html"
        result = messagebox.askquestion("Results", "saved results to {0}\n\nShow results in web browser?".format(os.path.realpath(filename)))
        if result == 'yes':
            webbrowser.open('file://' + os.path.realpath(filename))
    else :
            messagebox.showinfo("Information","something went wrong, \nplease check warnings for more information")

def marshaling():
    B1.flash()
    text.delete(1.0,END)
    text1.delete(1.0,END)
    text.insert(END, "console\n")
    text1.insert(END, "warnings\n")
    top.update_idletasks()
    arg = "marshaling.py {3},{4},{5},{1},{2},{6} {0}".format(E1.get(),CheckVar11.get(),CheckVar12.get(),V11.get(),V12.get(),CheckVar13.get(),CheckVar14.get())
    p = Popen(arg , stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
    #p = Popen("marshaling.py 90,120,line,0,0,0 " + E1.get(), stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
    finished = 0
    while True:
        output = p.stdout.readline()
        if output == '' and p.poll() != None: break
        print(output)
        if "WARNING" in output: 
             text1.insert(END, output+"\n")
        text.insert(END, output)
        top.update_idletasks()
        if "a.ok" in output:
            finished = 1
    if finished == 1 :
        filename = "TrackingMap.html"
        result = messagebox.askquestion("Results", "saved results to {0}\n\nShow results in web browser?".format(os.path.realpath(filename)))
        if result == 'yes':
            webbrowser.open('file://' + os.path.realpath(filename))
    else :
            messagebox.showinfo("Information","something went wrong, \nplease check warnings for more information")

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
E2 = Entry(top, bd =5, width=80, font=("Ariel", "12"))
E2.pack(padx="20")
T2 = Label(top, text="30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70")
T2.pack()

F21 = Frame(top)
T21 = Label(F21, text="grace zone in the start/end of the restricted zone (in meters)", font=("Ariel", "12"))
T21.pack(side = LEFT)
V21 = StringVar()
E21 = Entry(F21, textvariable=V21, bd =3, width=4, font=("Ariel", "14"))
E21.pack(side = RIGHT)
V21.set("90")
F21.pack()
F22 = Frame(top)
T22 = Label(F22, text="distance from enter/exit point allowed (ring for display only, in meters)", font=("Ariel", "12"))
T22.pack(side = LEFT)
V22 = StringVar()
E22 = Entry(F22, textvariable=V22, bd =3, width=4, font=("Ariel", "14"))
E22.pack(side = RIGHT)
V22.set("100")
F22.pack()
CheckVar21 = StringVar()
CheckVar22 = StringVar()
CheckVar23 = StringVar()
C21 = Checkbutton(top, text = "show all points in the restricted zone", variable = CheckVar21, onvalue = "yes", offvalue = "no", width = 30, font=("Ariel", "12"))
C22 = Checkbutton(top, text = "show all track points (very slow!)", variable = CheckVar22, onvalue = "points", offvalue = "line", width = 30, font=("Ariel", "12"))
C23 = Checkbutton(top, text = "merge segments(need testing)", variable = CheckVar23, onvalue = "yes", offvalue = "no", width = 30, font=("Ariel", "12"))
C21.deselect()
C22.deselect()
C23.deselect()
C21.pack()
C22.pack()
C23.pack()

B2 = Button(top, text ="speeding", command = speeding, font=("Ariel", "24"), bg="gray", fg="white", bd="5")
B2.pack(padx="20",pady="20")

S1 = LabelFrame(top, text="")
S1.pack(padx="20",pady="10")
E1 = Entry(top, bd =5, width=80, font=("Ariel", "12"))
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
CheckVar11 = StringVar()
CheckVar12 = StringVar()
CheckVar13 = StringVar()
CheckVar14 = StringVar()
C11 = Checkbutton(top, text = "show waypoints", variable = CheckVar11, onvalue = "yes", offvalue = "no", width = 20, font=("Ariel", "12"))
C12 = Checkbutton(top, text = "show waypoints line", variable = CheckVar12, onvalue = "yes", offvalue = "no", width = 20, font=("Ariel", "12"))
C13 = Checkbutton(top, text = "show all track points (very slow!)", variable = CheckVar13, onvalue = "points", offvalue = "line", width = 30, font=("Ariel", "12"))
C14 = Checkbutton(top, text = "merge segments(need testing)", variable = CheckVar14, onvalue = "yes", offvalue = "no", width = 30, font=("Ariel", "12"))
C11.deselect()
C12.deselect()
C13.deselect()
C14.deselect()
C11.pack()
C12.pack()
C13.pack()
C14.pack()

B1 = Button(top, text ="marshaling", command = marshaling, font=("Ariel", "24"), bg="gray", fg="white", bd="5")
B1.pack(padx="20",pady="20")

F13 = Frame(top)
#T3 = Label(F13, text="results")
#T3.pack(side = RIGHT)
text = Text(F13,bg="lightgray", width=40)
text.pack(side = RIGHT,padx="10",pady="10")
#T4 = Label(F13, text="warnings")
#T4.pack(side = LEFT)
text1 = Text(F13,bg="lightgray", width=40)
text1.pack(side = LEFT,padx="10",pady="10")
text.insert(END, "results\n")
text1.insert(END, "warnings\n")
F13.pack()
rClickbinder(top)
top.mainloop()
