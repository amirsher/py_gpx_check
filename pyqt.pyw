#!/usr/bin/python

#import webbrowser
#import datetime
import os, sys
import logging
import gpxpy
import gpxpy.gpx
import math
import csv
import glob
import folium
from folium.plugins import FloatImage

from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QCheckBox, QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, QComboBox, QPlainTextEdit, QFileDialog, QTabWidget, QProgressBar, QStatusBar
from PySide2.QtGui import QIcon, QTextCursor
from PySide2.QtCore import Slot, Qt, QUrl, QDateTime
from subprocess import Popen, PIPE
from PySide2.QtWebEngineWidgets import QWebEngineView


#from pathlib import Path
#print(str(Path.home()))

#script_folder = os.getcwd()
scriptDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.expanduser("~/Desktop"))

class App(QMainWindow):
 
    def __init__(self):
        super(App, self).__init__()
        self.title = 'GPX Check'
#        self.left = 0
 #       self.top = 0
  #      self.width = 300
   #     self.height = 200
        self.setWindowTitle(self.title)
  #      self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'logo-512x512.png')) 

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()
 

class MyTableWidget(QWidget):        
 
    def __init__(self, parent):   
        super(MyTableWidget, self).__init__(parent)
 #       self.layout = QVBoxLayout(self)
        self.layout = QVBoxLayout()
        self.web = QWebEngineView()
 #       self.web.setWindowIcon(QIcon(scriptDir + os.path.sep + 'logo-512x512.png')) 

        # Initialize tab screen
        self.tabs = QTabWidget()
 #       self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
#        self.tabs.resize(300,200) 
        self.tabs.setStyleSheet("QTabBar{font: bold;}")

        # Add tabs
  #      self.tabs.addTab(self.tab1,"Folder")
        self.tabs.addTab(self.tab2,"Speeding")
        self.tabs.addTab(self.tab3,"Marshaling")
        self.tabs.addTab(self.web,"Results")
         
        # Create textbox
        self.textbox0 = QLabel(self)
        self.textbox0.setText("plaese select folder!")
        self.textbox0.setToolTip("Please select the folder where all the GPX files are.\nAll the results files will be saved to the this folder as well.\nIf no folder is selected, Desktop will be used.")
        self.textbox0.setStyleSheet("QLabel {font-size:36px; background-color:#eff0f1; color:black; border:none;}")
#        self.textbox0.setReadOnly(True)
#        self.textbox0.setMinimumWidth(400)        
        self.textbox0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Create a button in the window
        self.button1 = QPushButton('  select folder  ')
        # connect button to function marshal
        self.button1.clicked.connect(self.selectFolder)
        self.button1.setStyleSheet("QPushButton {font-size:48px; background-color:lightgray; color:black; margin:20px;}")
        self.button1.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.textbox5 = QPlainTextEdit(self)
#        self.textbox5.setFixedWidth(600)
#        self.textbox5.setFixedHeight(600)
        self.textbox5.setMinimumHeight(400)        
        self.textbox5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.textbox5.insertPlainText("results\n\n")
        self.textbox5.setReadOnly(True)
        self.textbox5.setStyleSheet("QPlainTextEdit {margin:10px;}")

        # Creating a progress bar and setting the value limits
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)
        self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.progressBar.setTextVisible(0)

#########################################
########        speeding     ############
#########################################


        # Create label
#        self.s_label = QLabel("30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70")
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
   #     self.s_textbox.setText("30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70 30.195176,35.04978 30.1749997,35.0642141 50 30.0310113,34.933191 29.978476,34.934311 80") # FOR TESTING
        self.s_textbox.setPlaceholderText('Ex: 30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70') 
        self.s_textbox.setToolTip('Please enter the speed restricted zone(s) "lat,lon speed lat,lon speed"\nFormat could be DD: 30.195176,35.04978 or DMS: 30.11.42.635,35.02.59.208')
        self.s_textbox1 = QLineEdit(self)
        self.s_textbox1.setFixedWidth(80)
        self.s_textbox1.setText("90")
        self.s_textbox2 = QLineEdit(self)
        self.s_textbox2.setFixedWidth(80)
        self.s_textbox2.setText("120")
        
        self.s_button = QPushButton('  check speeding  ')
        self.s_button.setToolTip('check speeding zones')
        self.s_button.setStyleSheet("QPushButton {font-size:48px; background-color:lightgray; color:black; margin:30px;}")
        # connect button to function spedding
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
        self.textbox.setToolTip('Please enter the marshaling point(s) "lat,lon lat,lon"\nFormat could be DD: 30.195176,35.04978 or DMS: 30.11.42.635,35.02.59.208')
        self.textbox1 = QLineEdit(self)
        self.textbox1.setFixedWidth(80)
        self.textbox1.setText("80")
        self.textbox2 = QLineEdit(self)
        self.textbox2.setFixedWidth(80)
        self.textbox2.setText("100")
        
        # Create a button in the window
        self.button = QPushButton('  check marshaling  ')
        self.button.setToolTip('check marshaling points')
        self.button.setStyleSheet("QPushButton {font-size:48px; background-color:lightgray; color:black; margin:30px;}")
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

        h_box4 = QVBoxLayout()
        h_box4.addWidget(self.progressBar)
        h_box4.addWidget(self.textbox5)

        h_box5 = QHBoxLayout()
        h_box5.addStretch()
        h_box5.addWidget(self.button)
        h_box5.addStretch()

####combined

 
        h_box0 = QHBoxLayout()
#        h_box0.addStretch()
        h_box0.addWidget(self.button1)
        h_box0.addWidget(self.textbox0)
#        h_box0.addStretch()

        # Create first tab
#        self.tab1.layout = QVBoxLayout(self)
#        box = QVBoxLayout()
#        self.tab1.layout.addStretch()
#        self.tab1.layout.addLayout(h_box0)
#        box.addWidget(self.button1)
#        self.tab1.setLayout(self.tab1.layout)

### speeding
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.s_textbox)
#        box.addLayout(s_h_box)
        self.tab2.layout.addLayout(s_h_box1)
        self.tab2.layout.addLayout(s_h_box2)
#        box.addWidget(self.s_comboBox)
        self.tab2.layout.addLayout(s_h_box3)
        self.tab2.layout.addWidget(self.s_checkbox1)
        self.tab2.layout.addWidget(self.s_checkbox3)
        self.tab2.layout.addLayout(s_h_box5)
#        box.addWidget(self.s_button)
        self.tab2.setLayout(self.tab2.layout)

### marshaling
        self.tab3.layout = QVBoxLayout(self)
        self.tab3.layout.addWidget(self.textbox)
#        box.addLayout(h_box)
        self.tab3.layout.addLayout(h_box1)
        self.tab3.layout.addLayout(h_box2)
#        box.addWidget(self.comboBox)
        self.tab3.layout.addLayout(h_box3)
        self.tab3.layout.addWidget(self.checkbox1)
        self.tab3.layout.addWidget(self.checkbox2)
        self.tab3.layout.addWidget(self.checkbox3)
        self.tab3.layout.addLayout(h_box5)
#        box.addWidget(self.button)
#        self.tab3.layout.addLayout(h_box4)
        self.tab3.setLayout(self.tab3.layout)

        self.tab4.layout = QVBoxLayout(self)
        self.tab4.setLayout(self.tab4.layout)

        layout2 = QVBoxLayout()
        layout2.addLayout(h_box0)

        layout3 = QVBoxLayout()
        layout3.addLayout(h_box4)

        self.layout.addLayout( layout2 )  # Add "select folder" to widget              
        self.layout.addWidget(self.tabs) # Add tabs to widget
        self.layout.addLayout( layout3 )# Add output/warnings to widget

        self.setLayout(self.layout)
 



    @Slot()
    def spedding(self):
        self.progressBar.setValue( 0 )
  #      now = datetime.datetime.now() 
        cwd = os.getcwd()
        logFile = "spedding_results.txt"
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=os.path.realpath(logFile), filemode='w', format='%(message)s', level=logging.INFO)
#        logging.basicConfig(filename='spedding_results_{0}.txt'.format(now.strftime("%Y%m%d_%H%M%S")), filemode='w', format='%(message)s', level=logging.INFO)
        
        self.textbox5.setStyleSheet("QPlainTextEdit {background-color:white; color:black; margin:20px;}")
        self.textbox5.clear()
   #     self.textbox5.insertPlainText("checking...\n\n")
        QApplication.processEvents() # update gui
        global warning
        warning = 0
        if not self.s_textbox.text():
            self.textbox5.clear()
            self.textbox5.setStyleSheet("QPlainTextEdit {background-color:red; color:white; margin:20px;}")
            self.textbox5.insertPlainText("ERROR: \nno speeding zone(s) to check! \nplease enter valid zone(s)")
            QApplication.processEvents() # update gui
            return App()


        s_textboxValue = self.s_textbox.text() # 30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70
        s_textboxValue1 = self.s_textbox1.text() # grace zone in the start/end of the restricted zone (in meters)
        s_textboxValue2 = self.s_textbox2.text() # distance from enter/exit point allowed (ring for display only, in meters)
 # self.checkbox1.checkState() returns 2 for checked, 0 for unchecked and 1 for partial
 #       print(1 if self.s_checkbox1.checkState() > 0 else 0) # show waypoints
 #       print(1 if self.s_checkbox3.checkState() > 0 else 0) # merge segments(need testing)
        s_textboxValue3 = (1 if self.s_checkbox1.checkState() > 0 else 0) # show all points in the restricted zone
        s_textboxValue5 = (1 if self.s_checkbox3.checkState() > 0 else 0) # merge segments(need testing)





        graceZone = int(s_textboxValue1) # grace zone in the start/end of the restricted zone, in meters
        distance_from_point_allowed = int(s_textboxValue2) # ring for display only, in meters
        showAllRestrictedPoints = s_textboxValue3 # show all point of competitor in the restricted zone
        line_points = self.s_comboBox.currentText() # display "line" or "points", points is very slow.
        merge_segments = s_textboxValue5 # merege segments
        reverse = 0 # check for speeding on the reverse track FIXME


        '''
        graceZone = 90 # grace zone in the start/end of the restricted zone, in meters
        distance_from_point_allowed = 80 # ring for display only, in meters
        showAllRestrictedPoints = 1 # show all point of competitor in the restricted zone
        line_points = "line" # display "line" or "points", points is very slow.
        reverse = 0 # check for speeding on the reverse track
        '''
        color = ['#FF0000', '#008000', '#0000FF', '#FFFF00', '#00FF00', '#FF00FF', '#00FFFF', '#800000', '#008080', '#800080', '#000080', '#808000', '#FFA500', '#A52A2A', '#0000A0', '#FFFFFF', '#000000', ]
        c = 0



        if line_points != "line" and line_points != "points":
            line_points = "line"

  #      with open("{0}/spedding_results.txt".format(cwd), "w"): pass # clear the txt file

  #      with open("{0}/spedding_results.txt".format(cwd), "a") as speddingfile:
                
    #    restrictedZones= int((len(sys.argv)-2)/3)
        pointsCheck = s_textboxValue.split()
        restrictedZones = int(len(pointsCheck)/3)
    #    print("restrictedZones "+str(restrictedZones))
        checkArguments = 0
        if int(restrictedZones) < 1: # check if we have at least 1 zone
            checkArguments = 1
            
        output = ("File generated on {1}.\n\nThere are {0} restricted Zone(s).\n".format(restrictedZones,QDateTime.currentDateTime().toString(Qt.ISODate)))
    #       print("\n{}".format(output))
     #   speddingfile.write("{}\n\n".format(output))
        self.textbox5.insertPlainText("{}\n\n".format(output))
        self.textbox5.moveCursor(QTextCursor.End)
        QApplication.processEvents() # update gui
        logging.info(output)

        # loging the zones
        for z in range(0, restrictedZones):

#            print ("start zone {0}: {1}\n".format(z+1, pointsCheck[(3*z)]))
#            print ("end zone {0}: {1}\n".format(z+1, pointsCheck[(3*z)+1]))
#            print ("restricted speed zone {0}: {1} kph\n".format(z+1, pointsCheck[(3*z)+2]))
            output = ("start zone {0}: {1}\nend zone {0}: {2}\nrestricted speed zone {0}: {3} kph\n".format(z+1, pointsCheck[(3*z)], pointsCheck[(3*z)+1], pointsCheck[(3*z)+2]))
      #      speddingfile.write(output)
            self.textbox5.insertPlainText(output)
            self.textbox5.moveCursor(QTextCursor.End)
            QApplication.processEvents() # update gui
            logging.info(output)

            if (("," not in pointsCheck[(3*z)]) or ("," not in pointsCheck[(3*z)+1]) or ("," in pointsCheck[(3*z)+2])): # check the first 2 elements has "," and the third dont
                checkArguments = 1

        #   print("checkArguments "+str(checkArguments))
        
        output = ("\nchecking folder: {0}\n".format(cwd))
    #    speddingfile.write(output)
#        print(output)
        self.textbox5.insertPlainText(output)
        self.textbox5.moveCursor(QTextCursor.End)
        QApplication.processEvents() # update gui
        logging.info(output)

        if (((len(pointsCheck))%3 == 0) and (checkArguments == 0)): # check in number of arguments are devided by 3 using modulo and it structured right
            if (glob.glob("*.gpx")) :
                my_map=self.SfoliumMap(glob.glob("*.gpx")[0])
                speeding_feature_group = folium.FeatureGroup(name="speeding zone")

            else:
                output = ("\n\nNo gpx file(s)!\n")
        #        print(output)
          #      speddingfile.write(output)
                self.textbox5.insertPlainText(output)
                self.textbox5.moveCursor(QTextCursor.End)
                self.textbox5.setStyleSheet("QPlainTextEdit {background-color:red; color:white; margin:20px;}")
                QApplication.processEvents() # update gui
                logging.info(output)
                return App()

            # for progressBar
            n = len(glob.glob("*.gpx"))
            n = 100/n
            v = 0

            for file in glob.glob("*.gpx"):
                
                self.progressBar.setValue(int(v))
                v =  n + v

                cleanFile = os.path.splitext(file)[0]                

                output = ("\nChecking file: {0}\n".format(cleanFile))
           #     speddingfile.write(output)
                self.textbox5.insertPlainText(output)
                self.textbox5.moveCursor(QTextCursor.End)
                QApplication.processEvents() # update gui
                logging.info(output)

                with open("{0}".format(file), "r") as gpx_file: # check if file contain track, if not passing on it
                    gpxCheckTrack = gpxpy.parse(gpx_file)

                    for Check_track in gpxCheckTrack.tracks:
                        segment_no = len(Check_track.segments)

                    if len(gpxCheckTrack.tracks) == 0 : 
                        output = "\nwarning! {0} contain {1} tracks! and {2} waypoint(s) and {3} route(s) and {4} segment(s).\n".format(cleanFile,len(gpxCheckTrack.tracks),len(gpxCheckTrack.waypoints),len(gpxCheckTrack.routes),segment_no)
                        self.textbox5.setStyleSheet("QPlainTextEdit {border: 5px solid red;}")
                        warning = 1
                        continue
                    else:
                        output = "\n{0} contain {1} track(s) and {2} waypoint(s) and {3} route(s) and {4} segment(s).\n".format(cleanFile,len(gpxCheckTrack.tracks),len(gpxCheckTrack.waypoints),len(gpxCheckTrack.routes),segment_no)
    #                 print(output)
                    self.textbox5.insertPlainText(output)
                    self.textbox5.moveCursor(QTextCursor.End)
                    QApplication.processEvents() # update gui
             #       speddingfile.write(output)
                    logging.info(output)

                if segment_no > 1 :
                    output = ("\nWARNING!, file {0} contain {1} segments, should not have more then 1 segment, results may be corrupted!\n".format(file,segment_no))
      #              print(output)
       #             speddingfile.write(output)
                    warning = 1
                    self.textbox5.insertPlainText(output)
                    self.textbox5.setStyleSheet("QPlainTextEdit {border: 5px solid red;}")
                    self.textbox5.moveCursor(QTextCursor.End)
                    QApplication.processEvents() # update gui
                    logging.info(output)

                feature_group = folium.FeatureGroup(name=cleanFile)
                my_map=self.SConvertAndSpeed(file,my_map,color[c],line_points,cwd,merge_segments,cleanFile,feature_group)

                for i in range(0, restrictedZones):

                    restricted_start = pointsCheck[(i*3)].split(',') # lat,lon
                    if (pointsCheck[(i*3)]).count('.') >= 4 : # lat/long is in minutes/seconds
                        restricted_start[0] = self.convertDecimal(restricted_start[0])
                        restricted_start[1] = self.convertDecimal(restricted_start[1])
                    else :
                        restricted_start[0] = float(restricted_start[0])
                        restricted_start[1] = float(restricted_start[1])
                    
                    restricted_finish = pointsCheck[(i*3)+1].split(',') # lat,lon
                    if (pointsCheck[(i*3)+1]).count('.') >= 4 : # lat/long is in minutes/seconds
                        restricted_finish[0] = self.convertDecimal(restricted_finish[0])
                        restricted_finish[1] = self.convertDecimal(restricted_finish[1])
                    else:
                        restricted_finish[0] = float(restricted_finish[0])
                        restricted_finish[1] = float(restricted_finish[1])

                    restricted_speed = float(pointsCheck[(i*3)+2]) # kph

            #           print(str(restricted_start[0])+"\n")
            #           print(str(restricted_start[1])+"\n")
            #           print(str(restricted_finish[0])+"\n")
            #           print(str(restricted_finish[1])+"\n")
            #           print(str(restricted_speed)+"\n")

                    zone = self.SFindClosest(i,cwd,file,restricted_start,restricted_finish,restricted_speed,cleanFile,speeding_feature_group,distance_from_point_allowed,graceZone) # number of restricted zone
                    self.OutputSpedding(int(zone[0])+1,int(zone[1])-1,zone[2],cwd,file,cleanFile,restricted_start,restricted_finish,graceZone,showAllRestrictedPoints,line_points,feature_group) # to be safe: +1,-1 is to start checking 1 point inside the zone from start and end
                    if reverse == 1 :
                        self.OutputSpedding(zone[1]+1,zone[0]-1,zone[2],cwd,file,cleanFile,restricted_start,restricted_finish,graceZone,showAllRestrictedPoints,line_points,feature_group)
                    feature_group.add_to(my_map)

                    if i == restrictedZones :
                        output = ("\n{0} Top Speed: {1} kph on point {2}\n".format(cleanFile,zone[3],zone[4]))
                #           print(output)
                 #       speddingfile.write(output)
                        self.textbox5.insertPlainText(output)
                        self.textbox5.moveCursor(QTextCursor.End)
                        QApplication.processEvents() # update gui
                        logging.info(output)

                os.remove("{1}/zzz_{0}.csv".format(file,cwd))
                if c < 15 :
                    c = c + 1
                else:
                    c = 0

            speeding_feature_group.add_to(my_map)
            url = ('https://tnuatiming.com/android-chrome-36x36.png')
            FloatImage(url, bottom=2, left=96).add_to(my_map)
            # my_map.add_child(MeasureControl())
            # folium.LatLngPopup().add_to(my_map)
            my_map.add_child(folium.LayerControl())
            my_map.fit_bounds(my_map.get_bounds())
            with open("SpeedingMap.html", "w"): pass # clear the txt file
            my_map.save("SpeedingMap.html")
    #        print("a.ok")
     #       speddingfile.write("a.ok\n")
            self.textbox5.insertPlainText("a.ok\n")
            self.textbox5.moveCursor(QTextCursor.End)
            self.textbox5.setStyleSheet("QPlainTextEdit {background-color:green; color:white; margin:20px;}")
            if warning == 1:
                self.textbox5.setStyleSheet("QPlainTextEdit {background-color:green; color:white; margin:20px; border: 5px solid red;}")
            QApplication.processEvents() # update gui
            logging.info("a.ok\n")

            filename = "SpeedingMap.html"
     #       buttonReply = QMessageBox.question(self, 'finished message', "saved results to {0}\n\nShow results in web browser?".format(os.path.realpath(filename)), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
      #      if buttonReply == QMessageBox.Yes:
     #           webbrowser.open('file://' + os.path.realpath(filename))

            output = ("\nsaved graphic results to {0}\n\nsaved text results to {1}\n".format(os.path.realpath(filename),os.path.realpath(logFile)))
            self.textbox5.insertPlainText(output)
            self.textbox5.moveCursor(QTextCursor.End)
            QApplication.processEvents() # update gui
            logging.info(output)
            self.progressBar.setValue( 100 )

      #      self.web.setWindowTitle("Speeding Results")
            self.web.load(QUrl().fromLocalFile(os.path.realpath(filename)))
            self.tabs.setCurrentIndex(2) # jump to Results tab
            self.web.show()
        else:
    #           print('\nworong arguments, please use:\n\npython rally_speeding_folder.py start_lat,start_long finish_lat,finish_long restricted_speed\n\nEx: python rally_speeding_folder.py 30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70\n')
            output = ("\nworong arguments, please use:\n\nstart_lat,start_long finish_lat,finish_long restricted_speed\n\nEx: 30.195176,35.04978 30.1749997,35.0642141 40 30.0310113,34.933191 29.978476,34.934311 70\n")
            self.textbox5.setStyleSheet("QPlainTextEdit {background-color:red; color:white; margin:20px;}")
            self.textbox5.insertPlainText(output)
            QApplication.processEvents() # update gui
    #        speddingfile.write(output)
            logging.info(output)

    #    speddingfile.close()





    def SfoliumMap(self,file):
        '''
        foliumpoints = [] # for folium
        with open("{0}".format(file), "r") as gpx_file: 
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment in track.segments:
                    for point_no, point in enumerate(segment.points):
                        foliumpoints.append(tuple([point.latitude, point.longitude]))
        if len(foliumpoints) > 0 :
            ave_lat = sum(p[0] for p in foliumpoints)/len(foliumpoints)
            ave_lon = sum(p[1] for p in foliumpoints)/len(foliumpoints)
            # Load map centred on average coordinates
            #Map tileset to use. Can choose from this list of built-in tiles:
            #            - "OpenStreetMap"
            #            - "Stamen Terrain", "Stamen Toner", "Stamen Watercolor"
            #            - "CartoDB positron", "CartoDB dark_matter"
            #            - "Mapbox Bright", "Mapbox Control Room" (Limited zoom)
            #            - "Cloudmade" (Must pass API key)
            #            - "Mapbox" (Must pass API key)
        else:
            ave_lat = 35.0
            ave_lon = 30.0
        '''
        my_map = folium.Map(location=[35.0, 30.0], tiles='',attr='',  zoom_start=12, control_scale=True, prefer_canvas=True)
    #    folium.TileLayer(tiles='http://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',attr='DigitalGlobe', name='World Imagery', max_zoom=17).add_to(my_map)
    #    folium.TileLayer(tiles='https://israelhiking.osm.org.il/Hebrew/Tiles/{z}/{x}/{y}.png',attr='israelhiking.osm.org.il', name='Hebrew Base Map', max_zoom=16).add_to(my_map)
    #    folium.TileLayer(tiles='https://israelhiking.osm.org.il/OverlayTiles/{z}/{x}/{y}.png',attr='israelhiking.osm.org.il', name='Hiking Trails Overlay').add_to(my_map)
    #    folium.TileLayer(tiles='https://israelhiking.osm.org.il/Hebrew/mtbTiles/{z}/{x}/{y}.png',attr='israelhiking.osm.org.il', name='MTB Hebrew Base Map', max_zoom=16).add_to(my_map)
    #    folium.TileLayer(tiles='https://israelhiking.osm.org.il/OverlayMTB/{z}/{x}/{y}.png',attr='israelhiking.osm.org.il', name='MTB Trails Overlay').add_to(my_map)
    #    folium.TileLayer(tiles='https://tile.opentopomap.org/{z}/{x}/{y}.png',attr='OpenTopoMap', name='OpenTopoMap', max_zoom=18).add_to(my_map)
        folium.TileLayer(tiles='OpenStreetMap',attr='OpenStreetMap', name='OpenStreetMap').add_to(my_map)

        return my_map


    def SConvertAndSpeed (self,file,my_map,color,line_points,cwd,merge_segments,cleanFile,feature_group):

        point_no_csv = 0
        with open("{1}/zzz_{0}.csv".format(file,cwd), "w"): pass # clear the csv file

        with open("{0}".format(file), "r") as gpx_file, open("{1}/zzz_{0}.csv".format(file,cwd), "a") as gpxfile: 

        #gpx_file = open('z20171214-111736.gpx', 'r')
            latitude = [] # for matplotlib
            longitude = [] # for matplotlib
            foliumpoints = [] # for folium

            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment_no, segment in enumerate(track.segments):
                    for point_no, point in enumerate(segment.points):
                        # calculate the speed
                        if point.speed != None:
                            speed = round((point.speed)*3.6,2) #convert to kph rounded to 2 decimal
    #                    elif point_no > 0 and point_no < len(segment.points)-1  :
    #                        speed1 = point.speed_between(segment.points[point_no - 1])
    #                        speed2 = point.speed_between(segment.points[point_no + 1])
    #                        if (speed1 is None) or (speed2 is None) :
    #                            pass
    #                        else:
    #                           speed = round(((speed1+speed2)/2)*3.6,2) #speed im kph rounded to 2 decimal
                        else :
    #                        speed = 0.0
                            speed = segment.get_speed(point_no)
                            if speed != None:
                                speed = round(speed*3.6,2) #convert to kph rounded to 2 decimal
                        if point_no == 0 and point.speed == None :
                            speed = 0.0
                                            
                        if merge_segments != 1 :
                            point_no_csv = point_no
                            
                        if line_points == "points" :
                            folium.Circle(location=(point.latitude,point.longitude),radius=5,stroke=False,fill="true",color="{}".format(color),fill_color="{}".format(color), tooltip="{0}<br>speed: {1} kph<br>{4}<br>{2} , {3}<br>point no. {5}".format(cleanFile,speed,point.latitude,point.longitude,point.time,point_no_csv+1),fill_opacity=0.8).add_to(feature_group)
                                
                        gpxfile.write('{0},{1},{2},{3},{4}\n'.format(point_no_csv, point.latitude, point.longitude, speed, point.time))
                    
                        if line_points == "line" :
                            latitude.append( point.latitude )
                            longitude.append( point.longitude )
                            foliumpoints.append(tuple([point.latitude, point.longitude]))
                        
                        point_no_csv = point_no_csv + 1


        if line_points == "line" :
            folium.vector_layers.PolyLine(foliumpoints, color="{}".format(color),tooltip="{}".format(cleanFile), weight=3, opacity=1).add_to(feature_group)
        '''
        for waypoint in gpx.waypoints:
            folium.Marker(location=(waypoint.latitude,waypoint.longitude),icon=folium.Icon(color='blue', icon='check', prefix='fa'), popup="waypoint {0}<br>{1} , {2}".format(waypoint.name,waypoint.latitude,waypoint.longitude)).add_to(feature_group)
        '''
        is_waypoints = "no"
        for waypoint_no, waypoint in enumerate(gpx.waypoints):
            if waypoint_no != None :
                is_waypoints = "yes"
        if  is_waypoints == "yes" :          
            output = ("\nWARNING!, file {0} contain {1} waypoints, results may be corrupted!\n".format(file,waypoint_no))
     #       print(output)
      #      speddingfile.write(output)
            warning = 1
            self.textbox5.insertPlainText(output)
            self.textbox5.setStyleSheet("QPlainTextEdit {border: 5px solid red;}")
            self.textbox5.moveCursor(QTextCursor.End)
            QApplication.processEvents() # update gui
            logging.info(output)

        return my_map



    def SFindClosest(self,i,cwd,file,restricted_start,restricted_finish,restricted_speed,cleanFile,speeding_feature_group,distance_from_point_allowed,graceZone):
        
        closest_to_start = None
        closest_to_start_meters = 100000000000000000000.
        closest_to_finish = None
        closest_to_finish_meters = 100000000000000000000.

        topspeed = 0
            
        reader = csv.reader(open("{1}/zzz_{0}.csv".format(file,cwd)), delimiter=',')
        for row in reader:

            if float(row[3]) > float(topspeed) :
                topspeed = row[3]
                topspeed_point = row[0]

            start_meters = self.great_circle(restricted_start, (float(row[1]),float(row[2])))
            finish_meters = self.great_circle(restricted_finish, (float(row[1]),float(row[2])))

            # determine if point closest to start or finish
            if start_meters < closest_to_start_meters  :
                closest_to_start = row[0]
                closest_to_start_meters = round(start_meters,2)
            if finish_meters < closest_to_finish_meters  :
                closest_to_finish = row[0]
                closest_to_finish_meters = round(finish_meters,2)

        if closest_to_start == None :
            output = ("\nWARNING!, file {0} may not contain valid track, please check before running the script again, Exiting...\n".format(file))
            print(output)
            global warning
            warning = 1
            self.textbox5.insertPlainText(output)
            self.textbox5.setStyleSheet("QPlainTextEdit {border: 5px solid red;}")
            self.textbox5.moveCursor(QTextCursor.End)
            QApplication.processEvents() # update gui
     #       speddingfile.write(output)
            logging.info(output)
            return App()

        output = ("\nRestricted Zone {4} ({5} kph):\nClosest to start: Point {0} at {1} meters, Closest to finish: Point {2} at {3} meters.\n\n".format(closest_to_start, closest_to_start_meters, closest_to_finish, closest_to_finish_meters,i+1,restricted_speed))
   #     print(output)
     #   speddingfile.write(output)
        self.textbox5.insertPlainText(output)
        self.textbox5.moveCursor(QTextCursor.End)
        QApplication.processEvents() # update gui
        logging.info(output)
            
        folium.Marker(location=(restricted_start[0],restricted_start[1]),icon=folium.Icon(color='red', icon='exclamation', prefix='fa'), tooltip="restricted zone {0} start<br>speed limit <b>{1} kph</b><br>{2} , {3}".format(i+1,restricted_speed,round(restricted_start[0],6),round(restricted_start[1],6))).add_to(speeding_feature_group)
        folium.Marker(location=(restricted_finish[0],restricted_finish[1]),icon=folium.Icon(color='green', icon='check', prefix='fa'), tooltip="restricted zone {0} end<br>speed limit <b>{1} kph</b><br>{2} , {3}".format(i+1,restricted_speed,round(restricted_finish[0],6),round(restricted_finish[1],6))).add_to(speeding_feature_group)

        folium.Circle(location=(restricted_start[0],restricted_start[1]),radius=distance_from_point_allowed, weight=1,color="gray", tooltip="allowed {0} meters from point".format(distance_from_point_allowed),opacity=0.2).add_to(speeding_feature_group)
        folium.Circle(location=(restricted_finish[0],restricted_finish[1]),radius=distance_from_point_allowed, weight=1,color="gray", tooltip="allowed {0} meters from point".format(distance_from_point_allowed),opacity=0.2).add_to(speeding_feature_group)
        # grace zone marking
        folium.Circle(location=(restricted_start[0],restricted_start[1]),radius=graceZone, weight=1,color="lightgray", tooltip="grace zone: {0}  meters".format(graceZone),opacity=0.2).add_to(speeding_feature_group)
        folium.Circle(location=(restricted_finish[0],restricted_finish[1]),radius=graceZone, weight=1,color="lightgray", tooltip="grace zone: {0}  meters".format(graceZone),opacity=0.2).add_to(speeding_feature_group)

        return (closest_to_start,closest_to_finish,restricted_speed,topspeed,topspeed_point)
        
        
    def OutputSpedding(self,closest_to_start,closest_to_finish,restricted_speed,cwd,file,cleanFile,restricted_start,restricted_finish,graceZone,showAllRestrictedPoints,line_points,feature_group):
        sz = 0
        reader = csv.reader(open("{1}/zzz_{0}.csv".format(file,cwd)), delimiter=',')
        for row in reader:
            
            row[1] = round(float(row[1]),6)
            row[2] = round(float(row[2]),6)
            distToStart = round(self.great_circle(restricted_start, (row[1],row[2])),2)
            distToFinish = round(self.great_circle(restricted_finish, (row[1],row[2])),2)
            
            if ((int(row[0]) >= int(closest_to_start)) and (int(row[0]) <= int(closest_to_finish)) and (distToStart > graceZone) and (distToFinish > graceZone)):
                if (float(row[3]) >= int(restricted_speed)) :
                    output = ("SPEEDING!!! at point {0}, location: ({1},{2}), speed: {3} kph.\n".format(row[0],row[1],row[2],row[3]))
    #                print(output)
     #               speddingfile.write(output)
                    self.textbox5.insertPlainText(output)
                    self.textbox5.moveCursor(QTextCursor.End)
                    QApplication.processEvents() # update gui
                    logging.info(output)

                    folium.Marker(location=(row[1],row[2]),icon=folium.Icon(color='black', icon='camera', prefix='fa'), tooltip="{0}<br>speed: <b>{1} kph</b><br>{4}<br>{2} , {3}".format(cleanFile,row[3],row[1],row[2],row[4])).add_to(feature_group)
                elif ((showAllRestrictedPoints == 1) and (line_points == "line")):
                    folium.Circle(location=(row[1],row[2]),radius=3,stroke=False,fill="true",color="#000000", tooltip="{0}<br>speed: <b>{1} kph</b><br>{4}<br>{2} , {3}".format(cleanFile,row[3],row[1],row[2],row[4]),fill_opacity=1).add_to(feature_group)

                    
            # marking the track restricted zone start/finish points for speeding calculation
            if ((sz == 0) and (int(row[0]) >= int(closest_to_start)) and (distToStart > graceZone)) :
                folium.Circle(location=(row[1],row[2]),radius=5,stroke=False,fill="true",color="black",fill_color="black", tooltip="{0} entering restitricted zone<br>speed: <b>{1} kph</b><br>distance: {2} meters".format(cleanFile,row[3],distToStart),fill_opacity=1).add_to(feature_group)
                sz = 1

            if ((int(row[0]) <= int(closest_to_finish)) and (distToFinish > graceZone)) :
                fzlat = row[1]
                fzlon = row[2]
                fzspeed = row[3]
                fzdist = distToFinish
        folium.Circle(location=(fzlat,fzlon),radius=5,stroke=False,fill="true",color="black",fill_color="black", tooltip="{0} exiting restitricted zone<br>speed: <b>{1} kph</b><br>distance: {2} meters".format(cleanFile,fzspeed,fzdist),fill_opacity=1).add_to(feature_group)





    @Slot()
    def marshal(self):
        self.progressBar.setValue( 0 )
        cwd = os.getcwd()
     #   now = datetime.datetime.now() 
        logFile = "marshaling_results.txt"
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filename=os.path.realpath(logFile), filemode='w', format='%(message)s', level=logging.INFO)
#        logging.basicConfig(filename='marshaling_results_{0}.txt'.format(now.strftime("%Y%m%d_%H%M%S")), filemode='w', format='%(message)s', level=logging.INFO)

        self.textbox5.setStyleSheet("QPlainTextEdit {border: 2px solid gray; background-color:white; color:black; margin:20px;}")
        self.textbox5.clear()
    #    self.textbox5.insertPlainText("checking...\n\n")
        QApplication.processEvents() # update gui
        global warning
        warning = 0
        if not self.textbox.text():
            self.textbox5.clear()
            self.textbox5.setStyleSheet("QPlainTextEdit {background-color:red; color:white; margin:20px;}")
            self.textbox5.insertPlainText("ERROR: \nno marshaling point(s) to check! \nplease enter valid point(s)")
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

        pointsCheck = textboxValue.split()
        MarshalPoints = (len(pointsCheck))
   #     arguments = MarshalPoints + 1

   #     print("MarshalPoints "+str(MarshalPoints))
        checkArguments = 0
        if int(MarshalPoints) < 1: # check if we have at least 1 Marshal Point
            checkArguments = 1

        distance_to_marshal_allowed = int(textboxValue1)
        distance_to_waypoint_allowed = int(textboxValue2)
        line_points = self.comboBox.currentText()
        showWaypoints = textboxValue3 # 1 to show waypoints
        showWaypointsLine = textboxValue4 # 1 to show waypoints line
        if showWaypointsLine == 1 :
            showWaypoints = 1
        merge_segments = textboxValue5 # merege segments


        '''
        showWaypoints = 1 # "1" to show waypoints
        showWaypointsLine = 0 # "1" to show waypoints line
        distance_to_marshal_allowed = 80
        distance_to_waypoint_allowed = 100 # ring for display only

        line_points = "line" # display "line" or "points", points is very slow.
        '''
        #['red', 'blue', 'green', 'purple', 'orange', 'darkred','lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue','darkpurple', 'white', 'pink', 'lightblue', 'lightgreen','gray', 'black', 'lightgray']

        color = ['#FF0000', '#008000', '#0000FF', '#FFFF00', '#00FF00', '#FF00FF', '#00FFFF', '#800000', '#008080', '#800080', '#000080', '#808000', '#FFA500', '#A52A2A', '#0000A0', '#FFFFFF', '#000000', ]
        c = 0




        if line_points != "line" and line_points != "points":
            line_points = "line"

   #     with open("{0}/marshaling_results.txt".format(cwd), "w"): pass # clear the txt file

    #    with open("{0}/marshaling_results.txt".format(cwd), "a") as marshalfile:

#            MarshalPoints= int(len(sys.argv)-2)

        output = ("File generated on {2}.\n\nThere are {0} Marshal Point(s).\nOut of range set to {1} meters.\n\n".format(MarshalPoints,distance_to_marshal_allowed,QDateTime.currentDateTime().toString(Qt.ISODate)))
#         print("\n{}".format(output))
 #       marshalfile.write(output)
        self.textbox5.insertPlainText(output)
        self.textbox5.moveCursor(QTextCursor.End)
        QApplication.processEvents() # update gui
        logging.info(output)


        for x in range(0, MarshalPoints):
            output = ("Marshal point {0}: {1}\n".format((x+1), (pointsCheck)[x]))
    #           print((pointsCheck)[x])
    #          print (output)
     #       marshalfile.write(output)
            self.textbox5.insertPlainText(output)
            self.textbox5.moveCursor(QTextCursor.End)
            QApplication.processEvents() # update gui
            logging.info(output)

            if ("," not in (pointsCheck)[x]): # check pointsCheck has "," 
                checkArguments = 1

            marshalpoint = ((pointsCheck)[x]).split(',')

        #      print("checkArguments "+str(checkArguments))

        output = ("\nchecking folder: {0}\n".format(cwd))
    #    marshalfile.write(output)
        self.textbox5.insertPlainText(output)
        self.textbox5.moveCursor(QTextCursor.End)
        QApplication.processEvents() # update gui
        logging.info(output)
#        print(output)

#           if isinstance(MarshalPoints, int) :
        if (checkArguments == 0):

            if (glob.glob("*.gpx")) :
                my_map=self.foliumMap(glob.glob("*.gpx")[0])
                marshals_feature_group = folium.FeatureGroup(name="Marshal(s)")

            else:
                output = ("\n\nNo gpx file(s)!\n")
     #           marshalfile.write(output)
        #           print(output)
                self.textbox5.insertPlainText(output)
                self.textbox5.moveCursor(QTextCursor.End)
                self.textbox5.setStyleSheet("QPlainTextEdit {background-color:red; color:white; margin:20px;}")
                QApplication.processEvents() # update gui
                logging.info(output)
                return App()

            # for progressBar
            n = len(glob.glob("*.gpx"))
            n = 100/n
            v = 0

            for file in glob.glob("*.gpx"):
                        
                self.progressBar.setValue(int(v))
                v =  n + v

                cleanFile = os.path.splitext(file)[0]                
                        
                output = ("\n\nChecking file: {}".format(cleanFile))
      #          marshalfile.write(output)
                self.textbox5.insertPlainText(output)
                self.textbox5.moveCursor(QTextCursor.End)
                QApplication.processEvents() # update gui
                logging.info(output)

                with open("{0}".format(file), "r") as gpx_file: # check if file contain track, if not passing on it
                    gpxCheckTrack = gpxpy.parse(gpx_file)

                    for Check_track in gpxCheckTrack.tracks:
                        segment_no = len(Check_track.segments)

                    if len(gpxCheckTrack.tracks) == 0 : 
                        output = "\nwarning! {0} contain {1} tracks! and {2} waypoint(s) and {3} route(s) and {4} segment(s).\n".format(cleanFile,len(gpxCheckTrack.tracks),len(gpxCheckTrack.waypoints),len(gpxCheckTrack.routes),segment_no)
                        self.textbox5.setStyleSheet("QPlainTextEdit {border: 5px solid red;}")
                        warning = 1
                #        continue
                    else:
                        output = ("\n{0} contain {1} track(s) and {2} waypoint(s) and {3} route(s) and {4} segment(s).\n".format(cleanFile,len(gpxCheckTrack.tracks),len(gpxCheckTrack.waypoints),len(gpxCheckTrack.routes),segment_no))
    #                 print(output)
                    self.textbox5.insertPlainText(output)
                    self.textbox5.moveCursor(QTextCursor.End)
                    QApplication.processEvents() # update gui
       #             marshalfile.write(output)
                    logging.info(output)

                if segment_no > 1 :
                    output = ("\nWARNING!, file {0} contain {1} segments, should not have more then 1 segment, results may be corrupted!\n\n".format(file,segment_no))
         #           print(output)
                    warning = 1
          #          marshalfile.write(output)
                    self.textbox5.insertPlainText(output)
                    self.textbox5.setStyleSheet("QPlainTextEdit {border: 5px solid red;}")
                    self.textbox5.moveCursor(QTextCursor.End)
                    QApplication.processEvents() # update gui
                    logging.info(output)


        #          print(cleanFile)
                feature_group = folium.FeatureGroup(name=cleanFile)
                my_map=self.ConvertAndSpeed(file,my_map,color[c],line_points,cwd,merge_segments,cleanFile,feature_group,showWaypointsLine,showWaypoints,distance_to_waypoint_allowed)
                

                for x in range(0, MarshalPoints):
                    marshalpoint = ((pointsCheck)[x]).split(',')


                    if ((pointsCheck)[x]).count('.') >= 4 : # lat/long is in minutes/seconds
                        marshal_lat = self.convertDecimal(marshalpoint[0])
                        marshal_long = self.convertDecimal(marshalpoint[1])
                    else :
                        marshal_lat = float(marshalpoint[0])
                        marshal_long = float(marshalpoint[1])
                        
                    marshal = self.FindClosestSingle([marshal_lat,marshal_long],cwd,file)

                    # add marshal marker to web map
                    folium.Marker(location=(marshal_lat,marshal_long),icon=folium.Icon(color='blue', icon='male', prefix="fa"), tooltip="Marshal {0}<br>{1} , {2}".format(x+1,round(marshal_lat,6),round(marshal_long,6))).add_to(marshals_feature_group)
                    
                    folium.Circle(location=(marshal_lat,marshal_long),radius=distance_to_marshal_allowed, weight=1,color="gray", tooltip="allowed {0} meters from marshal {1}".format(distance_to_marshal_allowed,x+1),opacity=0.2).add_to(marshals_feature_group)

                    self.OutputMarshal(x+1,marshal[0],marshal[1],distance_to_marshal_allowed,cwd,file,cleanFile,feature_group)
                    feature_group.add_to(my_map)

                os.remove("{1}/zzz_{0}.csv".format(file,cwd))
                if c < 15 :
                    c = c + 1
                else:
                    c = 0
                        
            marshals_feature_group.add_to(my_map)
            url = ('https://tnuatiming.com/android-chrome-36x36.png')
            FloatImage(url, bottom=2, left=96).add_to(my_map)
            # my_map.add_child(MeasureControl())
            # folium.LatLngPopup().add_to(my_map)
            my_map.add_child(folium.LayerControl())
            my_map.fit_bounds(my_map.get_bounds())
            with open("TrackingMap.html", "w"): pass # clear the txt file
            my_map.save("TrackingMap.html")

            output = ("\na.ok\n")
    #         print(output)
    #        marshalfile.write(output)
            self.textbox5.insertPlainText(output)
            self.textbox5.moveCursor(QTextCursor.End)
            self.textbox5.setStyleSheet("QPlainTextEdit {background-color:green; color:white; margin:20px;}")
            if warning == 1:
                self.textbox5.setStyleSheet("QPlainTextEdit {background-color:green; color:white; margin:20px; border: 5px solid red;}")
            QApplication.processEvents() # update gui
            logging.info(output)

            filename = "TrackingMap.html"
#            buttonReply = QMessageBox.question(self, 'finished message', "saved results to {0}\n\nShow results in web browser?".format(os.path.realpath(filename)), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#            if buttonReply == QMessageBox.Yes:
#                webbrowser.open('file://' + os.path.realpath(filename))

            output = ("\nsaved graphic results to {0}\n\nsaved text results to {1}\n".format(os.path.realpath(filename),os.path.realpath(logFile)))
            self.textbox5.insertPlainText(output)
            self.textbox5.moveCursor(QTextCursor.End)
            QApplication.processEvents() # update gui
            logging.info(output)
            self.progressBar.setValue( 100 )

     #       self.web.setWindowTitle("Marshaling Results")
            self.web.load(QUrl().fromLocalFile(os.path.realpath(filename)))
            self.tabs.setCurrentIndex(2) # jump to Results tab
            self.web.show()

        else:
            output = ("\nworong arguments, please use:\n\n marshal1_lat,marshal1_long marshal2_lat,marshal2_long \n\nEx: 30.195176,35.04978 30.1749997,35.0642141 30.0310113,34.933191 29.978476,34.934311\n")
        #      print(output)
      #      marshalfile.write(output)
            self.textbox5.setStyleSheet("QPlainTextEdit {background-color:red; color:white; margin:20px;}")
            self.textbox5.insertPlainText(output)
            QApplication.processEvents() # update gui
            logging.info(output)

    #    marshalfile.close()


 

    def foliumMap(self,file):
        foliumpoints = [] # for folium
        foliumWptpoints = [] # for folium
        with open("{0}".format(file), "r") as gpx_file: 
            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment in track.segments:
                    for point_no, point in enumerate(segment.points):
                        foliumpoints.append(tuple([point.latitude, point.longitude]))
            '''
            for waypoint in gpx.waypoints:
                foliumWptpoints.append(tuple([waypoint.latitude, waypoint.longitude]))
            '''
        '''
        if len(foliumpoints) > 0 :
            ave_lat = sum(p[0] for p in foliumpoints)/len(foliumpoints)
            ave_lon = sum(p[1] for p in foliumpoints)/len(foliumpoints)
            # Load map centred on average coordinates
            #Map tileset to use. Can choose from this list of built-in tiles:
            #            - "OpenStreetMap"
            #            - "Stamen Terrain", "Stamen Toner", "Stamen Watercolor"
            #            - "CartoDB positron", "CartoDB dark_matter"
            #            - "Mapbox Bright", "Mapbox Control Room" (Limited zoom)
            #            - "Cloudmade" (Must pass API key)
            #            - "Mapbox" (Must pass API key)
        elif len(foliumWptpoints) > 0 :
            ave_lat = sum(p[0] for p in foliumWptpoints)/len(foliumWptpoints)
            ave_lon = sum(p[1] for p in foliumWptpoints)/len(foliumWptpoints)
        else:
            ave_lat = 35.0
            ave_lon = 30.0
        '''
        my_map = folium.Map(location=[35.0, 30.0], tiles='',attr='',  zoom_start=12, control_scale=True, prefer_canvas=True)
    #    folium.TileLayer(tiles='http://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',attr='DigitalGlobe', name='World Imagery', max_zoom=17).add_to(my_map)
    #    folium.TileLayer(tiles='https://israelhiking.osm.org.il/Hebrew/Tiles/{z}/{x}/{y}.png',attr='israelhiking.osm.org.il', name='Hebrew Base Map', max_zoom=16).add_to(my_map)
    #    folium.TileLayer(tiles='https://israelhiking.osm.org.il/OverlayTiles/{z}/{x}/{y}.png',attr='israelhiking.osm.org.il', name='Hiking Trails Overlay').add_to(my_map)
    #    folium.TileLayer(tiles='https://israelhiking.osm.org.il/Hebrew/mtbTiles/{z}/{x}/{y}.png',attr='israelhiking.osm.org.il', name='MTB Hebrew Base Map', max_zoom=16).add_to(my_map)
    #    folium.TileLayer(tiles='https://israelhiking.osm.org.il/OverlayMTB/{z}/{x}/{y}.png',attr='israelhiking.osm.org.il', name='MTB Trails Overlay').add_to(my_map)
    #    folium.TileLayer(tiles='https://tile.opentopomap.org/{z}/{x}/{y}.png',attr='OpenTopoMap', name='OpenTopoMap', max_zoom=18).add_to(my_map)
        folium.TileLayer(tiles='OpenStreetMap',attr='OpenStreetMap', name='OpenStreetMap').add_to(my_map)

        return my_map


    def ConvertAndSpeed (self,file,my_map,color,line_points,cwd,merge_segments,cleanFile,feature_group,showWaypointsLine,showWaypoints,distance_to_waypoint_allowed):
        
        point_no_csv = 0

        with open("{1}/zzz_{0}.csv".format(file,cwd), "w"): pass # clear the csv file

        with open("{0}".format(file), "r") as gpx_file, open("{1}/zzz_{0}.csv".format(file,cwd), "a") as gpxfile: 

        #gpx_file = open('z20171214-111736.gpx', 'r')
    #        latitude = [] # for matplotlib
    #        longitude = [] # for matplotlib
    #        wptlatitude = [] # for matplotlib
    #        wptlongitude = [] # for matplotlib
            foliumpoints = [] # for folium
            foliumWPTpoints = [] # for folium

            gpx = gpxpy.parse(gpx_file)
            for track in gpx.tracks:
                for segment_no, segment in enumerate(track.segments):
                    for point_no, point in enumerate(segment.points):
                        # calculate the speed
                        if point.speed != None:
                            speed = round((point.speed)*3.6,2) #convert to kph rounded to 2 decimal
    #                    elif point_no > 0 and point_no < len(segment.points)-1  :
    #                        speed1 = point.speed_between(segment.points[point_no - 1])
    #                        speed2 = point.speed_between(segment.points[point_no + 1])
    #                        if (speed1 is None) or (speed2 is None) :
    #                            pass
    #                        else:
    #                           speed = round(((speed1+speed2)/2)*3.6,2) #speed im kph rounded to 2 decimal
                        else :
    #                        speed = 0.0
                            speed = segment.get_speed(point_no)
                            if speed != None:
                                speed = round(speed*3.6,2) #convert to kph rounded to 2 decimal

                        if merge_segments != 1 :
                            point_no_csv = point_no

                        if line_points == "points" :
                            folium.Circle(location=(point.latitude,point.longitude),radius=5,stroke=False,fill="true",color="{}".format(color),fill_color="{}".format(color), tooltip="{0}<br>speed: {1} kph<br>{4}<br>{2} , {3}<br>point no. {5}".format(cleanFile,speed,point.latitude,point.longitude,point.time,point_no_csv+1),fill_opacity=0.8).add_to(feature_group)
                                
                        gpxfile.write('{0},{1},{2},{3},{4}\n'.format(point_no_csv, point.latitude, point.longitude, speed, point.time))
                        '''
                        latitude.append( point.latitude )
                        longitude.append( point.longitude )
                        '''
                        foliumpoints.append(tuple([point.latitude, point.longitude]))

                        point_no_csv = point_no_csv + 1

        if line_points == "line" :

            folium.vector_layers.PolyLine(foliumpoints, color="{}".format(color),tooltip="{}".format(cleanFile), weight=3, opacity=1).add_to(feature_group)

        is_waypoints = "no"
        for waypoint_no, waypoint in enumerate(gpx.waypoints):
            if waypoint_no != None :
                is_waypoints = "yes"
            if showWaypoints == 1 :
                if waypoint.name == None :
                    waypoint.name = waypoint_no + 1
                folium.Marker(location=(waypoint.latitude,waypoint.longitude),icon=folium.Icon(color='lightgray', icon='check', prefix='fa'), tooltip="waypoint {0}<br>{1} , {2}".format(waypoint.name,round(waypoint.latitude,6),round(waypoint.longitude,6))).add_to(feature_group)
                folium.Circle(location=(waypoint.latitude,waypoint.longitude),radius=distance_to_waypoint_allowed, weight=1,color="gray", tooltip="allowed {0} meters from waypoint".format(distance_to_waypoint_allowed),opacity=0.2).add_to(feature_group)

                if showWaypointsLine == 1 :
                    foliumWPTpoints.append(tuple([waypoint.latitude, waypoint.longitude]))
        
        if showWaypointsLine == 1 :
            folium.vector_layers.PolyLine(foliumWPTpoints, color="lightgray",tooltip="waypoint track", weight=3, opacity=1).add_to(feature_group)
        if  is_waypoints == "yes" :          
            output = ("\nWARNING!, file {0} contain {1} waypoint(s), results may be corrupted!\n\n".format(file,waypoint_no+1))
            warning = 1
       #     print(output)
       #     marshalfile.write(output)
            self.textbox5.insertPlainText(output)
            self.textbox5.moveCursor(QTextCursor.End)
            self.textbox5.setStyleSheet("QPlainTextEdit {border: 5px solid red;}")
            QApplication.processEvents() # update gui
            logging.info(output)

        return my_map


    def FindClosestSingle(self,marshal_point,cwd,file):
        #marshal_point = i.split(',') # lat,lon
        marshal_point[0] = float(marshal_point[0])
        marshal_point[1] = float(marshal_point[1])
        
        closest_to_marshal_point = None
        closest_to_marshal_point_meters = 100000000000000000000.

        reader = csv.reader(open("{1}/zzz_{0}.csv".format(file,cwd)), delimiter=',')
        for row in reader:

            start_meters = self.great_circle(marshal_point, (float(row[1]),float(row[2])))

            # determine if point closest to marshal
            if start_meters < closest_to_marshal_point_meters  :
                closest_to_marshal_point = row[0]
                closest_to_marshal_point_meters = round(start_meters,2)

        return (closest_to_marshal_point,closest_to_marshal_point_meters)

    
    def OutputMarshal(self,x,closest_to_marshal_point,closest_to_marshal_point_meters,out_of_range,cwd,file,cleanFile,feature_group):
            

        reader = csv.reader(open("{1}/zzz_{0}.csv".format(file,cwd)), delimiter=',')
        for row in reader:
                if (int(row[0]) == int(closest_to_marshal_point)) :
                    if int(closest_to_marshal_point_meters) > int(out_of_range) :
                        output = ("Passed Marshal {0} on {1} at distance of {2} meters and speed of {3} kph. OUT OF RANGE\n".format(x, row[4],int(closest_to_marshal_point_meters), row[3]))
                    else :
                        output = ("Passed Marshal {0} on {1} at distance of {2} meters and speed of {3} kph.\n".format(x, row[4],int(closest_to_marshal_point_meters), row[3]))
          #          print(output)
           #         marshalfile.write(output)
                    self.textbox5.insertPlainText(output)
                    self.textbox5.moveCursor(QTextCursor.End)
                    QApplication.processEvents() # update gui
                    logging.info(output)

                    if int(closest_to_marshal_point_meters) < int(out_of_range) :
                        folium.Circle(location=(float(row[1]),float(row[2])),radius=5,stroke=False,fill="true",color="black",fill_color="black", tooltip="{0}<br>passed {1} meters from marshal {2}".format(cleanFile,closest_to_marshal_point_meters,x),fill_opacity=1).add_to(feature_group)
                    else :                
                        folium.Marker(location=(float(row[1]),float(row[2])),icon=folium.Icon(color='red', icon='info', prefix="fa"), tooltip="{0}<br>passed {1} meters from marshal {2}<br>OUT OF RANGE!".format(cleanFile,closest_to_marshal_point_meters,x)).add_to(feature_group)




    def distance_vincenty(self, point1, point2): # deprecated
        """
        Vincenty's formula (inverse method) to calculate the distance (in
        kilometers or miles) between two points on the surface of a spheroid
        """
        # WGS 84
        a = 6378137  # meters
        f = 1 / 298.257223563
        b = 6356752.314245  # meters; b = (1 - f)a

        MILES_PER_KILOMETER = 0.621371

        MAX_ITERATIONS = 200
        CONVERGENCE_THRESHOLD = 1e-12  # .000,000,000,001

        # short-circuit coincident points
        if point1[0] == point2[0] and point1[1] == point2[1]:
            return 0.0

        U1 = math.atan((1 - f) * math.tan(math.radians(point1[0])))
        U2 = math.atan((1 - f) * math.tan(math.radians(point2[0])))
        L = math.radians(point2[1] - point1[1])
        Lambda = L

        sinU1 = math.sin(U1)
        cosU1 = math.cos(U1)
        sinU2 = math.sin(U2)
        cosU2 = math.cos(U2)

        for iteration in range(MAX_ITERATIONS):
            sinLambda = math.sin(Lambda)
            cosLambda = math.cos(Lambda)
            sinSigma = math.sqrt((cosU2 * sinLambda) ** 2 +
                                (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
            if sinSigma == 0:
                return 0.0  # coincident points
            cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
            sigma = math.atan2(sinSigma, cosSigma)
            sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
            cosSqAlpha = 1 - sinAlpha ** 2
            try:
                cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
            except ZeroDivisionError:
                cos2SigmaM = 0
            C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
            LambdaPrev = Lambda
            Lambda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma *
                                                (cos2SigmaM + C * cosSigma *
                                                    (-1 + 2 * cos2SigmaM ** 2)))
            if abs(Lambda - LambdaPrev) < CONVERGENCE_THRESHOLD:
                break  # successful convergence
        else:
            return None  # failure to converge

        uSq = cosSqAlpha * (a ** 2 - b ** 2) / (b ** 2)
        A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
        B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
        deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma *
                    (-1 + 2 * cos2SigmaM ** 2) - B / 6 * cos2SigmaM *
                    (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)))
        s = b * A * (sigma - deltaSigma)

    #    s /= 1000  # meters to kilometers
        return round(s, 6)



    def great_circle(self, point1, point2): # replace vincenty
        EARTH_RADIUS = 6371009 # WGS 84 in meters

        lat1, lng1 = math.radians(point1[0]), math.radians(point1[1])
        lat2, lng2 = math.radians(point2[0]), math.radians(point2[1])

        sin_lat1, cos_lat1 = math.sin(lat1), math.cos(lat1)
        sin_lat2, cos_lat2 = math.sin(lat2), math.cos(lat2)

        delta_lng = lng2 - lng1
        cos_delta_lng, sin_delta_lng = math.cos(delta_lng), math.sin(delta_lng)

        d = math.atan2(math.sqrt((cos_lat2 * sin_delta_lng) ** 2 +
                        (cos_lat1 * sin_lat2 -
                        sin_lat1 * cos_lat2 * cos_delta_lng) ** 2),
                    sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_delta_lng)

        return round((EARTH_RADIUS * d), 6)

    def convertDecimal(self,tude):
    # converter only work for N,E and not in string # FIXED: S, W is negative
        a = tude.split('.',3)
        dd = abs(float(a[0])) + (float(a[1]))/60 + (float(a[2]))/3600
        if float(a[0]) < 0:  
            dd = dd * -1.0  
        return dd




    def selectFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            os.chdir(folder_path)
        #    print(folder_path)
#            self.textbox0.clear()
            self.textbox0.setText(folder_path)
    #        return folder_path        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
