import webbrowser, os 
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QCheckBox, QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, QComboBox, QPlainTextEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from subprocess import check_output, Popen, PIPE
            

class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Check gpx files'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 200
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

         
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
 
        # Create textbox
        self.textbox0 = QPlainTextEdit(self)
        self.textbox0.insertPlainText("plaese select folder")
        self.textbox0.setStyleSheet("QPlainTextEdit {background-color:lightgray; color:blue;}")
        self.textbox0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textbox0.setReadOnly(True)
        self.textbox = QLineEdit(self)
#        self.textbox.setText("30.195176,35.04978 30.1749997,35.0642141") # FOR TESTING
        self.textbox.setPlaceholderText('please as follow: "30.195176,35.04978 30.1749997,35.0642141"') 
        self.textbox1 = QLineEdit(self)
        self.textbox1.setFixedWidth(80)
        self.textbox1.setText("80")
        self.textbox2 = QLineEdit(self)
        self.textbox2.setFixedWidth(80)
        self.textbox2.setText("100")
        self.textbox4 = QPlainTextEdit(self)
        self.textbox4.setFixedWidth(600)
        self.textbox4.setFixedHeight(600)
        self.textbox4.insertPlainText("warnings\n")
        self.textbox4.setReadOnly(True)
        self.textbox5 = QPlainTextEdit(self)
        self.textbox5.setFixedWidth(600)
        self.textbox5.setFixedHeight(600)
        self.textbox5.insertPlainText("output\n")
        self.textbox5.setReadOnly(True)
        
        # Create a button in the window
        self.button1 = QPushButton('select folder')
        # connect button to function marshal
        self.button1.clicked.connect(self.selectFolder)
        self.button = QPushButton('marshaling')
        self.button.setToolTip('check marshaling points')
        # connect button to function marshal
        self.button.clicked.connect(self.marshal)
 
        self.label3 = QLabel("show track as (points is very slow): ")
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("line")
        self.comboBox.addItem("points")
        self.comboBox.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

#        h_box = QVBoxLayout()
#        h_box.addStretch()
#        h_box.addWidget(self.label)
#        h_box.addStretch()

        h_box0 = QHBoxLayout()
        h_box0.addStretch()
        h_box0.addWidget(self.textbox0)
        h_box0.addStretch()

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

        box = QVBoxLayout()
        box.addLayout(h_box0)
        box.addWidget(self.button1)
        box.addWidget(self.textbox)
#        box.addLayout(h_box)
        box.addLayout(h_box1)
        box.addLayout(h_box2)
#        box.addWidget(self.comboBox)
        box.addLayout(h_box3)
        box.addWidget(self.checkbox1)
        box.addWidget(self.checkbox2)
        box.addWidget(self.checkbox3)
        box.addWidget(self.button)

        box.addLayout(h_box4)

        self.setLayout(box)
        self.show()
 
    @pyqtSlot()
    def marshal(self):
    #    print('PyQt5 button click')
   #     print(self.comboBox.currentText())
        self.textbox4.setStyleSheet("QPlainTextEdit {background-color:white; color:black;}")
        self.textbox5.setStyleSheet("QPlainTextEdit {background-color:white; color:black;}")
        self.textbox4.clear()
        self.textbox5.clear()
        self.textbox4.insertPlainText("warnings\n")
        self.textbox5.insertPlainText("output\n")
        QApplication.processEvents() # update gui
        if not self.textbox.text():
            self.textbox4.clear()
            self.textbox4.setStyleSheet("QPlainTextEdit {background-color:red; color:white;}")
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
            sys.stdout.flush()

            if "WARNING" in output:
                self.textbox4.insertPlainText(output+"\n")
            self.textbox5.insertPlainText(output+"\n")
#            text.insert(END, output)
#            top.update_idletasks()



            if "a.ok" in output:
                finished = 1
                self.textbox5.setStyleSheet("QPlainTextEdit {background-color:green; color:white;}")

        if finished == 1 :
            filename = "TrackingMap.html"


            buttonReply = QMessageBox.question(self, 'finished message', "saved results to {0}\n\nShow results in web browser?".format(os.path.realpath(filename)), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                webbrowser.open('file://' + os.path.realpath(filename))
        else:
            print("something went wrong, \nplease check warnings for more information")
            self.textbox5.setStyleSheet("QPlainTextEdit {background-color:red; color:white;}")



        #self.textbox.setText("")

    def selectFolder(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(None, "Select Folder")
        print(folder_path)
        self.textbox0.clear()
        self.textbox0.insertPlainText(folder_path)
        os.chdir(folder_path)
        return folder_path        
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
