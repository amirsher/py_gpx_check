#!/usr/bin/python

import webbrowser, os 
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QCheckBox, QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, QComboBox, QPlainTextEdit, QFileDialog
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import pyqtSlot, Qt
from subprocess import check_output, Popen, PIPE
            

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Check gpx files'
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
   #     self.setStyleSheet("background-color: lightgray;")

         
        # Create textbox
        self.textbox0 = QPlainTextEdit(self)
        self.textbox0.insertPlainText("plaese select folder")
        self.textbox0.setStyleSheet("QPlainTextEdit {font-size:36px; background-color:#eff0f1; color:blue; border:none; margin-top:50%;}")
        self.textbox0.setReadOnly(True)
#        self.textbox0.setMinimumWidth(400)        

        # Create a button in the window
        self.button1 = QPushButton('select folder')
        # connect button to function marshal
        self.button1.clicked.connect(self.selectFolder)
        self.button1.setStyleSheet("QPushButton {font-size:48px; background-color:lightgray; color:black; margin:30px;}")

        self.textbox4 = QPlainTextEdit(self)
#        self.textbox4.setFixedWidth(600)
#        self.textbox4.setFixedHeight(600)
        self.textbox4.setMinimumHeight(400)        
        self.textbox4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textbox4.insertPlainText("warnings:\n\n")
        self.textbox4.setReadOnly(True)
        self.textbox4.setStyleSheet("QPlainTextEdit {margin:20px;}")
        self.textbox5 = QPlainTextEdit(self)
#        self.textbox5.setFixedWidth(600)
#        self.textbox5.setFixedHeight(600)
        self.textbox5.setMinimumHeight(400)        
        self.textbox5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textbox5.insertPlainText("output\n\n")
        self.textbox5.setReadOnly(True)
        self.textbox5.setStyleSheet("QPlainTextEdit {margin:20px;}")


#########################################
########        speeding     ############
#########################################


        # Create label
#        self.s_label = QLabel("30.195176,35.04978 30.1749997,35.0642141")
#        self.s_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#        self.s_label.setAlignment(Qt.AlignCenter)
#        self.s_label.setStyleSheet("QLabel {font-size:24px; background-color:black; color:white;}")     
        self.s_label1 = QLabel("grace zone in the start/end of the restricted zone (in meters)")
        self.s_label2 = QLabel("distance from enter/exit point allowed (ring for display only, in meters)")

        # Create checkbox
        self.s_checkbox1 = QCheckBox("show all points in the restricted zone")
        self.s_checkbox1.setChecked(False)
        self.s_checkbox3 = QCheckBox("merge segments(need testing)")
        self.s_checkbox3.setChecked(False)
 
        # Create textbox
        self.s_textbox = QLineEdit(self)
#        self.s_textbox.setText("30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70") # FOR TESTING
        self.s_textbox.setPlaceholderText('Ex: 30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70') 
        self.s_textbox1 = QLineEdit(self)
        self.s_textbox1.setFixedWidth(80)
        self.s_textbox1.setText("90")
        self.s_textbox2 = QLineEdit(self)
        self.s_textbox2.setFixedWidth(80)
        self.s_textbox2.setText("120")
        
        self.s_button = QPushButton('speeding')
        self.s_button.setToolTip('check speeding zones')
        self.s_button.setStyleSheet("QPushButton {font-size:48px; background-color:lightgray; color:blue; margin:30px;}")
        # connect button to function marshal
        self.s_button.clicked.connect(self.spedding)
 
        self.s_label3 = QLabel("show track as (points is very slow): ")
        self.s_comboBox = QComboBox(self)
        self.s_comboBox.addItem("line")
        self.s_comboBox.addItem("points")
        self.s_comboBox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


#########################################
########       marshaling    ############
#########################################


        # Create label
#        self.label = QLabel("30.195176,35.04978 30.1749997,35.0642141")
#        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#        self.label.setAlignment(Qt.AlignCenter)
#        self.label.setStyleSheet("QLabel {font-size:24px; background-color:black; color:white;}")     
        self.label1 = QLabel("distance to marshal allowed (in meters)")
        self.label2 = QLabel("distance to waypoint allowed (in meters)")

        # Create checkbox
        self.checkbox1 = QCheckBox("show waypoints")
        self.checkbox1.setChecked(False)
        self.checkbox2 = QCheckBox("show waypoints line")
        self.checkbox2.setChecked(False)
        self.checkbox3 = QCheckBox("merge segments(need testing)")
        self.checkbox3.setChecked(False)
 
        self.textbox = QLineEdit(self)
#        self.textbox.setText("30.195176,35.04978 30.1749997,35.0642141") # FOR TESTING
        self.textbox.setPlaceholderText('Ex: 30.195176,35.04978 30.1749997,35.0642141') 
        self.textbox1 = QLineEdit(self)
        self.textbox1.setFixedWidth(80)
        self.textbox1.setText("80")
        self.textbox2 = QLineEdit(self)
        self.textbox2.setFixedWidth(80)
        self.textbox2.setText("100")
        
        # Create a button in the window
        self.button = QPushButton('marshaling')
        self.button.setToolTip('check marshaling points')
        self.button.setStyleSheet("QPushButton {font-size:48px; background-color:lightgray; color:blue; margin:30px;}")
        # connect button to function marshal
        self.button.clicked.connect(self.marshal)
 
        self.label3 = QLabel("show track as (points is very slow): ")
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("line")
        self.comboBox.addItem("points")
        self.comboBox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

#########################################
########       speeding    ############
#########################################

#        s_h_box = QVBoxLayout()
#        s_h_box.addStretch()
#        s_h_box.addWidget(self.label)
#        s_h_box.addStretch()


        s_h_box1 = QHBoxLayout()
        s_h_box1.addWidget(self.s_textbox1)
        s_h_box1.addWidget(self.s_label1)

        s_h_box2 = QHBoxLayout()
        s_h_box2.addWidget(self.s_textbox2)
        s_h_box2.addWidget(self.s_label2)

        s_h_box3 = QHBoxLayout()
        s_h_box3.addWidget(self.s_label3)
        s_h_box3.addWidget(self.s_comboBox)
        s_h_box3.addStretch()

        s_h_box5 = QHBoxLayout()
        s_h_box5.addStretch()
        s_h_box5.addWidget(self.s_button)
        s_h_box5.addStretch()

#########################################
########       marshaling    ############
#########################################

#        h_box = QVBoxLayout()
#        h_box.addStretch()
#        h_box.addWidget(self.label)
#        h_box.addStretch()


        h_box1 = QHBoxLayout()
        h_box1.addWidget(self.textbox1)
        h_box1.addWidget(self.label1)

        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.textbox2)
        h_box2.addWidget(self.label2)

        h_box3 = QHBoxLayout()
        h_box3.addWidget(self.label3)
        h_box3.addWidget(self.comboBox)
        h_box3.addStretch()

        h_box4 = QHBoxLayout()
        h_box4.addWidget(self.textbox5)
        h_box4.addWidget(self.textbox4)

        h_box5 = QHBoxLayout()
        h_box5.addStretch()
        h_box5.addWidget(self.button)
        h_box5.addStretch()

####combined

        h_box0 = QHBoxLayout()
        h_box0.addStretch()
        h_box0.addWidget(self.button1)
        h_box0.addWidget(self.textbox0)
        h_box0.addStretch()

        box = QVBoxLayout()
        box.addStretch()
        box.addLayout(h_box0)
#        box.addWidget(self.button1)

### speeding
        box.addWidget(self.s_textbox)
#        box.addLayout(s_h_box)
        box.addLayout(s_h_box1)
        box.addLayout(s_h_box2)
#        box.addWidget(self.s_comboBox)
        box.addLayout(s_h_box3)
        box.addWidget(self.s_checkbox1)
        box.addWidget(self.s_checkbox3)
        box.addLayout(s_h_box5)
#        box.addWidget(self.s_button)

### marshaling
        box.addWidget(self.textbox)
#        box.addLayout(h_box)
        box.addLayout(h_box1)
        box.addLayout(h_box2)
#        box.addWidget(self.comboBox)
        box.addLayout(h_box3)
        box.addWidget(self.checkbox1)
        box.addWidget(self.checkbox2)
        box.addWidget(self.checkbox3)
        box.addLayout(h_box5)
#        box.addWidget(self.button)

        box.addLayout(h_box4)

        self.setLayout(box)
        self.show()
 
    @pyqtSlot()
    def spedding(self):
    #    print('PyQt5 button click')
   #     print(self.s_comboBox.currentText())
        self.textbox4.setStyleSheet("QPlainTextEdit {background-color:white; color:black; margin:20px;}")
        self.textbox5.setStyleSheet("QPlainTextEdit {background-color:white; color:black; margin:20px;}")
        self.textbox4.clear()
        self.textbox5.clear()
        self.textbox4.insertPlainText("warnings:\n\n")
        self.textbox5.insertPlainText("checking...\n\n")
        QApplication.processEvents() # update gui
        if not self.s_textbox.text():
            self.textbox4.clear()
            self.textbox4.setStyleSheet("QPlainTextEdit {background-color:red; color:white; margin:20px;}")
            self.textbox4.insertPlainText("ERROR: \nno spedding points to check! \nplease enter valid points")
            QApplication.processEvents() # update gui
            return

        s_textboxValue = self.s_textbox.text() # 30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70
        s_textboxValue1 = self.s_textbox1.text() # grace zone in the start/end of the restricted zone (in meters)
        s_textboxValue2 = self.s_textbox2.text() # distance from enter/exit point allowed (ring for display only, in meters)
 # self.checkbox1.checkState() returns 2 for checked, 0 for unchecked and 1 for partial
 #       print(1 if self.s_checkbox1.checkState() > 0 else 0) # show waypoints
 #       print(1 if self.s_checkbox3.checkState() > 0 else 0) # merge segments(need testing)
        s_textboxValue3 = (1 if self.s_checkbox1.checkState() > 0 else 0) # show all points in the restricted zone
        s_textboxValue5 = (1 if self.s_checkbox3.checkState() > 0 else 0) # merge segments(need testing)

        arg = "speeding.py {0},{1},{2},{3},{4} {5}".format(s_textboxValue1 ,s_textboxValue2 ,s_textboxValue3, self.s_comboBox.currentText() ,s_textboxValue5 ,s_textboxValue)
        print(arg)
        p = Popen(arg , stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
        
        #p = Popen("speeding.py 90,120,line,0,0,0 " + textboxValue, stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
        finished = 0
        while True:
            output = p.stdout.readline()
            if output == '' and p.poll() != None: break
            print(output)
            self.textbox5.insertPlainText(output+"\n")
            self.textbox5.moveCursor(QTextCursor.End)
            QApplication.processEvents() # update gui

            if "WARNING" in output:
                self.textbox4.insertPlainText(output+"\n")

            if "a.ok" in output:
                finished = 1
                self.textbox5.setStyleSheet("QPlainTextEdit {background-color:green; color:white; margin:20px;}")

        if finished == 1 :
            filename = "SpeedingMap.html"


            buttonReply = QMessageBox.question(self, 'finished message', "saved results to {0}\n\nShow results in web browser?".format(os.path.realpath(filename)), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                webbrowser.open('file://' + os.path.realpath(filename))
        else:
            print("something went wrong, \nplease check warnings for more information")
            self.textbox5.setStyleSheet("QPlainTextEdit {background-color:red; color:white; margin:20px;}")


    @pyqtSlot()
    def marshal(self):
    #    print('PyQt5 button click')
   #     print(self.comboBox.currentText())
        self.textbox4.setStyleSheet("QPlainTextEdit {background-color:white; color:black; margin:20px;}")
        self.textbox5.setStyleSheet("QPlainTextEdit {background-color:white; color:black; margin:20px;}")
        self.textbox4.clear()
        self.textbox5.clear()
        self.textbox4.insertPlainText("warnings:\n\n")
        self.textbox5.insertPlainText("checking...\n\n")
        QApplication.processEvents() # update gui
        if not self.textbox.text():
            self.textbox4.clear()
            self.textbox4.setStyleSheet("QPlainTextEdit {background-color:red; color:white; margin:20px;}")
            self.textbox4.insertPlainText("ERROR: \nno marshal points to check! \nplease enter valid points")
            QApplication.processEvents() # update gui
            return

        textboxValue = self.textbox.text() # 30.195176,35.04978 30.1749997,35.0642141
        textboxValue1 = self.textbox1.text() # distance to marshal allowed (in meters)
        textboxValue2 = self.textbox2.text() # distance to waypoint allowed (in meters)
 # self.checkbox1.checkState() returns 2 for checked, 0 for unchecked and 1 for partial
 #       print(1 if self.checkbox1.checkState() > 0 else 0) # show waypoints
 #       print(1 if self.checkbox2.checkState() > 0 else 0) # show waypoints line
 #       print(1 if self.checkbox3.checkState() > 0 else 0) # merge segments(need testing)
        textboxValue3 = (1 if self.checkbox1.checkState() > 0 else 0) # show waypoints
        textboxValue4 = (1 if self.checkbox2.checkState() > 0 else 0) # show waypoints line
        textboxValue5 = (1 if self.checkbox3.checkState() > 0 else 0) # merge segments(need testing)

        arg = "marshaling.py {0},{1},{2},{3},{4},{5} {6}".format(textboxValue1 ,textboxValue2 ,self.comboBox.currentText() ,textboxValue3 ,textboxValue4 ,textboxValue5 ,textboxValue)
        print(arg)
        p = Popen(arg , stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
        
        #p = Popen("marshaling.py 90,120,line,0,0,0 " + textboxValue, stdout=PIPE, shell=True, universal_newlines=True) # to run on windows need to add "python"
        finished = 0
        while True:
            output = p.stdout.readline()
            if output == '' and p.poll() != None: break
            print(output)
            self.textbox5.insertPlainText(output+"\n")
            self.textbox5.moveCursor(QTextCursor.End)
            QApplication.processEvents() # update gui

            if "WARNING" in output:
                self.textbox4.insertPlainText(output+"\n")

            if "a.ok" in output:
                finished = 1
                self.textbox5.setStyleSheet("QPlainTextEdit {background-color:green; color:white; margin:20px;}")

        if finished == 1 :
            filename = "TrackingMap.html"


            buttonReply = QMessageBox.question(self, 'finished message', "saved results to {0}\n\nShow results in web browser?".format(os.path.realpath(filename)), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                webbrowser.open('file://' + os.path.realpath(filename))
        else:
            print("something went wrong, \nplease check warnings for more information")
            self.textbox5.setStyleSheet("QPlainTextEdit {background-color:red; color:white; margin:20px;}")


    def selectFolder(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            print(folder_path)
            os.chdir(folder_path)
            self.textbox0.clear()
            self.textbox0.insertPlainText(folder_path)
    #        return folder_path        
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
