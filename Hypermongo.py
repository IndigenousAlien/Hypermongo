#!/usr/bin/env python3

from typing import List
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import re
import os

#Purpose: Uses pyplot and PyQt5 GUI to improve SM plots.
#Author: All rights reserved by Jacky Tran, jtran9148@gmail.com
#Version: 2.9.2
#Date: 11/15/2022

#------------------------------------------------------------------------------------------------#
# Reads energy#.sph + massAndMore.out + anyfile, computes and graphs time versus plots           #
#                                                                                                #
# New Features:                                                                                  #
#              - Graphs now properly display scientific notation on the top-right corner         #
#              - Can plot any file you choose that has tablature data format                     #
#              - Can plot any 1 x-column you wish, vs. up to 6 y-columns at once                 #
#              - Can make scatter plots with adjustable point sizes                              #
#              - 3-Dimensional plots with an extra z-axis list.                                  #
#              - Can also read col.sph files but doesn't match with parent.sph currently         #
#              - Added new trendline option with degree of polynomial fitting.                   #
#              - Legends added to each subplot, first degree polynomial displays linear equation.#
# Changes&Bugs:                                                                                  #
#              - Removed x-axis numbers for all other subplots except the bottom-most plot when  #
#                using the shareax checked box                                                   #
#              - Updated informational text to explain the new functions                         #
#              - Changed massAndMore and energy plots to use the same user-input file.           #
#              - Changed file number checking, numbering of columns, and counting columns        #
# Future ideas:                                                                                  #
#              - Implement additional output file reader for MESA simulations                    #
#              - User customization for graphs instead of default look (seaborn?)                #
#              - Complete col.sph plots with simultaneous plots of parent.sph                    #
#              - Look into importing pandas to read and store data instead of while and for loops#
#              - Add keypress function for 'Enter' key to speed up making plots                  #
#------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------#
# Below here are the two classes made for the GUI of Hypermongo #
#---------------------------------------------------------------#

class Ui_MainWindow(object): # Creates a class object for the main window of Hypermongo

    def openWindow(self):  # Opens second window for energy/mass&more plots
        self.window = QtWidgets.QDialog()
        global FILENAME
        if self.radioButton.isChecked():
            FILENAME = 'energy.sph'
        elif self.radioButton_2.isChecked(): # Creates error window for mass&more.out when button is selected
            FILENAME = "massAndMore.out"
            if not os.path.isfile("massAndMore.out"): # Gives error message if 'massAndMore.out' is not in the current directory
                self.show_popupM()
                return
        elif self.radioButton_3.isChecked():
            FILENAME = self.lineEdit.text()
            if not os.path.isfile(FILENAME): # Gives error message if 'massAndMore.out' is not in the current directory
                self.show_popupUser(FILENAME)
                return
        elif self.radioButton_4.isChecked():
            FILENAME = "col.sph"
        self.ui = Ui_Dialog_User()
        self.ui.setupUi(self.window)
        self.window.show() 
        return

    def show_popupM(self): #Gives user warning popup for massAndMore.out if not found in current directory
        msg = QMessageBox()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        msg.setWindowTitle("Hold on there, Jethro!")
        msg.setText("\nError: massAndMore.out could not be found in the directory.\n")
        msg.setInformativeText("Make sure your file is in your current directory before proceeding!\n")
        msg.setDetailedText(f"Your current directory path is: \n" + "_"*43 + "\n" + str(os.getcwd()))
        msg.setIcon(QMessageBox.Warning)
        msg.setFont(font)
        showMessage = msg.exec_()
        return

    def show_popupUser(self, file): #Gives user warning popup for user-specified file if not found in current directory
        msg = QMessageBox()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        msg.setWindowTitle("Hold on there, Jethro!")
        if file == "":
            msg.setText(f"\nError: No file name was specified!")
            msg.setInformativeText("Make sure to add your desired file name to the text line!\n")
        else:
            msg.setText(f"\nError: {file} could not be found in the directory.\n")
            msg.setInformativeText("Make sure your file is in your current directory before proceeding!\n")
            msg.setDetailedText(f"Your current directory path is: \n" + "_"*39 + "\n" + str(os.getcwd()))
        msg.setIcon(QMessageBox.Warning)
        msg.setFont(font)
        showMessage = msg.exec_()
        return

    def changeDir(self): #Changes current directory to new directory.
        _translate = QtCore.QCoreApplication.translate
        newPath = str(QFileDialog.getExistingDirectory(None, "Select Directory")) #Opens new window asking to select directory, sets it as a string.
        if newPath != '': 
            os.chdir(newPath) #Changes current directory text to the string received from the new selected path
            self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">" + str(os.getcwd()) + "</span></p></body></html>"))
        return

    def setupUi(self, MainWindow): #Creates widgets and buttons on the main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 1000)
        font = QtGui.QFont()
        font.setPointSize(16)
        MainWindow.setFont(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        #set up radio btn 1 - energy.sph plots
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setMaximumWidth(400)
        self.gridLayout.addWidget(self.radioButton, 3, 0, 1, 1)

        #Set up radio btn 2 - Mass&More plots
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.setMaximumWidth(400)
        self.gridLayout.addWidget(self.radioButton_2, 3, 1, 1, 1)

        #Set up radio btn 3 - user-specified file
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.setMaximumWidth(400)
        self.gridLayout.addWidget(self.radioButton_3, 3, 2, 1, 1)

        #Set up radio btn 4 - col.sph file
        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_4.setMaximumWidth(400)
        self.gridLayout.addWidget(self.radioButton_4, 3, 3, 1, 1)

        #Set up line edit bar for user to input name of a file they wish to read and plot.
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 5, 0, 1, 3)

        #Set up txtbrwsr 1 - Info on program
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 2, 0, 1, 0)

        #Set up txtbrwsr 2 - Current directory info
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_2.setMaximumHeight(85)
        self.gridLayout.addWidget(self.textBrowser_2, 1, 0, 1, 0)

        #Set up pshbtn 1 - Next button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openWindow)
        self.pushButton.setMaximumWidth(150)
        self.gridLayout.addWidget(self.pushButton, 5, 3, 1, 1)

        #set up tlbtn - Access directory folders
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.changeDir)
        self.gridLayout.addWidget(self.toolButton, 0, 4, 1, 1)

        #Set up label - "Current Directory" label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        #Set up label_2 - "Input the file name below" label
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 739, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.exit)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        return

    def exit(self, MainWindow): #Closes the main window and quits out of Hypermongo when "Exit" is triggered
        return sys.exit()

    def retranslateUi(self, MainWindow): #Translates default text into more useful information in the main window.
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hypermongo"))
        self.radioButton.setText(_translate("MainWindow", "energy.sph    "))
        self.radioButton_2.setText(_translate("MainWindow", "massAndMore.out     "))
        self.radioButton_3.setText(_translate("MainWindow", "User-specified file     "))
        self.radioButton_4.setText(_translate("MainWindow", "col.sph"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:20pt; font-weight:600;\"\n>Welcome to Hypermongo! </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">________________________________________________________</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt200;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">This python program is a designed read and create plots for any table formatted data files. The first row of your data file must contain the names of the columns separated by spaces. Every row following is reserved for numbers only.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Start by selecting a file you wish to plot, then press the &quot;Next&quot; button. You may choose one of the default options or select your own file by select the user-specified button and typing the name of the file below.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Make sure you are in the correct directory where your file(s) are located.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">You can change your directory by pressing the &quot;...&quot; button.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">If you have any questions, suggestions, or bugs to report, you can contact me with my information below. Have fun!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Author: Jacky Tran @Allegheny College 2022</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Email: jtran9148@gmail.com</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Next"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; fo200nt-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">" + str(os.getcwd()) + "</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Current Directory:"))
        self.label_2.setText(_translate("MainWindow", "Enter the file name below:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Exit the program"))
        self.actionExit.setShortcut(_translate("MainWindow", "Esc"))
        return

class Ui_Dialog_User(Ui_MainWindow): #Defines class creating dialog window for user specified file
    
    def readFile(self):
        """Reads user-specified file and allows user to create up to 6 plots of data vs. time. Can also read third axis for 3-d plots
        """
        # Instantiating objects
        global FILENAME
        stepsize: int = self.spinBox.value() # These variables are tied to the values the user inputs into the spinbox widget on the GUI window.
        scatsize: int = self.spinBox2.value()
        fileNum: int = self.spinBox3.value()
        polyDeg: int = self.spinBox4.value()

        share_ax: bool = self.checkBox.isChecked() # True/False for shared-x axis turned on
        is_scatter: bool = self.checkBox2.isChecked() # True/False for Scatter plots turned on
        is_3D: bool = self.checkBox3.isChecked() # True/False for 3-D plots turned on
        is_trendline: bool = self.checkBox4.isChecked()
        legend: bool = self.checkBox5.isChecked()
        onePlot: bool = self.checkBox6.isChecked()

        ### Note: If you wish to read in a specific file that includes a numbering system to differentiate the files (i.e. energy#.sph or col####.sph),
        ### you can write your exception as an if-statement below in a similar fashion. Make sure that you tie it to the fileNum variable.

        if "energy.sph" in FILENAME:
            new_filename = f'energy{str(fileNum)}.sph' # Renames the FILENAME for energy.sph to the specific filenumber.
            if os.path.isfile(new_filename) == False: # If the user tries to read a energy.sph file with a number that doesn't exist in the directory, display an error message.
                self.show_popupE(new_filename)
                return 
        elif "col.sph" in FILENAME:
            if fileNum > 999: # These series of if statements determines what to rename the col.sph file to the specific file the user wants to read, with the 'File Number' spinbox.
                new_filename = f'col{str(fileNum)}.sph'
            elif fileNum > 99:
                new_filename = f'col0{str(fileNum)}.sph'
            elif fileNum > 9:
                new_filename = f'col00{str(fileNum)}.sph'
            else:
                new_filename = f'col000{str(fileNum)}.sph'
            if os.path.isfile(new_filename) == False: # If the user tries to read a col.sph file with a number that doesn't exist in the directory, display an error message.
                self.show_popupE(new_filename)
                return
        else:
            new_filename = FILENAME

        text_list_x: list = self.listWidget.selectedItems() # Stores objects of items selected in listWidgets
        text_list_y: list = self.listWidget2.selectedItems()
        text_list_z: list = self.listWidget3.selectedItems()
        xObjects: list = [] # Used to store column number for selected listWidget items.
        yObjects: list = []
        zObjects: list = []

        # This searches the selected object(s) in listWidget for the first number in the string. Used to determine selected column number.
        # it also appends the name of the column into the respective x, y, or z list columns.
        for i in list(text_list_x):  
            xObjects.append(int(re.search(r'\d+', i.text()).group())-1)
        for i in list(text_list_y):
            yObjects.append(int(re.search(r'\d+', i.text()).group())-1)
        for i in list(text_list_z):
            zObjects.append(int(re.search(r'\d+', i.text()).group())-1)

        numCol = len(yObjects) # This is the number of selected y-columns user wants to read. For 2-D Plots only.
        if numCol < 1 or numCol > 6 or len(text_list_x) > 1: # Checks whether the number of selected columns is not in the proper range (1-6). Gives error popup then stops.
            self.show_popupOutOfBounds()
            return
        if is_3D and (len(xObjects) < 1 or len(xObjects) > 1 or len(yObjects) < 1 or len(yObjects) > 1 or len(zObjects) < 1 or len(zObjects) > 1): #shows error when 3-D plot is selected and number or selected axis is not the required amount.
            self.show_popupOutOfBounds3D()
            return

        # Instantiating more variables to hold the actual data from the x, y and z columns.    
        xcol: list[float] = [] # These lists store the float values of the data file.
        ycol1: list[float] = []
        ycol2: list[float] = []
        ycol3: list[float] = []
        ycol4: list[float] = []
        ycol5: list[float] = []
        ycol6: list[float] = []
        j: int = 0 # This is used to compare with the modulus of the stepsize so that data is appended based on the stepsize.
        x: int = 0 # Just a simple variable used to determine when to append data to the names lists vs. appending data to the float lists.
        energy_or_col: bool = False 
        if ("energy.sph" in FILENAME) or ("col.sph" in FILENAME):
            energy_or_col = True

        # This checks if 3-D graph is checked and plots with the threeDGrph function.
        if is_3D:
            if energy_or_col:
                x = 1
            xlabel: list = self.subscriptName([self.setName()[xObjects[0]]], 1) # Creates new list that holds the axis labels of columns. Name is changed with subscriptName().
            ylabel: list = self.subscriptName([self.setName()[yObjects[0]]], 1)
            zlabel: list = self.subscriptName([self.setName()[zObjects[0]]], 1)
            threeDlabels: list = [xlabel[0], ylabel[0], zlabel[0]] # Combines all axis labels into one list.
            with open(new_filename) as Data:
                for line in Data: # Reads every row in file data
                    if x == 1:
                        if j % stepsize == 0:
                            row = line.split() # Splits current row into a list with items separated by empty spaces
                            try: # These consecutive try;except methods are used to capture errors where the number of data in the selected columns are mismatched. Ex: column 1 has 5 rows of data but column 2 has only 4.
                                xcol.append(float(row[xObjects[0]].replace('D', 'E'))) # Holds x column data
                            except IndexError:
                                self.show_popupMismatch()
                                return
                            try:
                                ycol1.append(float(row[yObjects[0]].replace('D', 'E'))) # Holds y column data
                            except IndexError:
                                self.show_popupMismatch()
                                return
                            try:
                                ycol2.append(float(row[zObjects[0]].replace('D', 'E'))) # Holds z column data
                            except IndexError:
                                self.show_popupMismatch()
                                return
                        j += 1
                    x = 1
            threeDplots = [xcol, ycol1, ycol2] # Holds x, y, and z data lists
            threeDGrph(threeDplots, threeDlabels, is_scatter, new_filename, scatsize) # Calls to 3-D graphing function at the bottom of the code.
            return 

        # This is for 2-D plots only.    
        with open(new_filename) as Data:
            for line in Data: # Reads every row in file data
                if x == 0: # This first if statement is just to append the names in the first row of the file.
                    row = line.split()
                    xlabel: str = self.setName()[xObjects[0]] # Takes the selected list in to create a string name.
                    ylabel1: str = self.setName()[yObjects[0]]
                    ylabel2: str = ''
                    ylabel3: str = '' #Instantiate name(2-6) variables then change them below if needed.
                    ylabel4: str = ''
                    ylabel5: str = ''
                    ylabel6: str = ''
                    if numCol > 1: # Checks the number of selected columns in the y-column and changes ylabels accordingingly
                        ylabel2 = self.setName()[yObjects[1]]
                    if numCol > 2:
                        ylabel3 = self.setName()[yObjects[2]]
                    if numCol > 3:
                        ylabel4 = self.setName()[yObjects[3]]
                    if numCol > 4:
                        ylabel5 = self.setName()[yObjects[4]]
                    if numCol > 5:
                        ylabel6 = self.setName()[yObjects[5]]
                    x = 1
                if x == 1 and energy_or_col: # This second if statement appends the data in every row after the first row, with a stepsize.
                    if j % stepsize == 0:
                        row: list = line.split() # Splits current row into a list with items separated by empty spaces
                        try: # These consecutive try;except methods are used to capture errors where the number of data in the selected columns are mismatched. Ex: column 1 has 5 rows of data but column 2 has only 4.
                            xcol.append(float(row[xObjects[0]].replace('D', 'E'))) # The replace() is used to check the string if it contains a 'D' and converts to 'E' which can then be converted to a proper float.
                        except IndexError:
                            self.show_popupMismatch()
                            return
                        try:
                            ycol1.append(float(row[yObjects[0]].replace('D', 'E')))
                        except IndexError:
                            self.show_popupMismatch()
                            return
                        if numCol > 1:
                            try:
                                ycol2.append(float(row[yObjects[1]].replace('D', 'E')))
                            except IndexError:
                                self.show_popupMismatch()
                                return
                        if numCol > 2:
                            try:
                                ycol3.append(float(row[yObjects[2]].replace('D', 'E')))
                            except IndexError:
                                self.show_popupMismatch()
                                return
                        if numCol > 3:
                            try:
                                ycol4.append(float(row[yObjects[3]].replace('D', 'E')))
                            except IndexError:
                                self.show_popupMismatch()
                                return
                        if numCol > 4:
                            try:
                                ycol5.append(float(row[yObjects[4]].replace('D', 'E')))
                            except IndexError:
                                self.show_popupMismatch()
                                return
                        if numCol > 5:
                            try:
                                ycol6.append(float(row[yObjects[5]].replace('D', 'E')))
                            except IndentationError:
                                self.show_popupMismatch()
                                return
                    j += 1
                energy_or_col = True
        labels: list = [xlabel, ylabel1, ylabel2, ylabel3, ylabel4, ylabel5, ylabel6] # Combines all axis labels into one list
        labels = self.subscriptName(labels, numCol+1) # Renames axis labels to add subscripts to the labels if a number is found. Calls subscriptName()
        yplot: list = [xcol, ycol1, ycol2, ycol3, ycol4, ycol5, ycol6] # Combines all data columns into one list
        if onePlot:
            onePlot2D(labels, yplot, new_filename, numCol, share_ax, is_scatter, scatsize, is_trendline, polyDeg, legend) # Calls the onePlot2D function at the bottom of the code
        else:
            grph(labels, yplot, new_filename, numCol, share_ax, is_scatter, scatsize, is_trendline, polyDeg, legend) # Calls the 2-D graph function at the bottom of the code
        return

    def subscriptName(self, ylabel: List[str], numCol: int) -> List[str]: #Changes the names of yplots to add subscripts if it contains a number. Returns new list with subcripted names.
        """This function takes a string and changes it to add a subscript
        for the massAndMore.out file, only if it contains a number. i.e m1 or x2...
        """
        for i in range(0, numCol):
            if any(i.isdigit() for i in ylabel[i]) == True:
                changeName: List[str] = re.split("(\d+)", ylabel[i]) #the re.split splits a string if a number is found.
                if len(changeName) == 3:
                    ylabel[i] = "$" + changeName[0] +"_{" + changeName[1] + "}$" + changeName[2]
                else:
                    ylabel[i] = "$" + changeName[0] +"_{" + changeName[1] + "}$"
        return ylabel 

    def countCol(self): # Counts the number of header columns in the file, separated by spaces in a single line.
        """Counts the number of header columns in user file"""
        numCol = len(self.setName())
        return numCol

    def setName(self) -> List[str]: # This function returns a list of all the header names in the user file.
        """Returns a list of names for the list widget in Ui_Dialog_User class."""
        global FILENAME
        if "energy.sph" in FILENAME: # Column headers for the energy.sph file
            return ['time', 'W', 'T', 'U', 'E', 'S', 'J']
        elif "col.sph" in FILENAME: # Column headers for the col.sph file
            return ['radius',
                    'pressure',
                    'density',
                    'temperature', 
                    'mean_molecular_weight', 
                    'mass',
                    'smoothing_length',
                    'neighbor_number',
                    'gravitational_acceleration',
                    'hydrodynamical_acceleration',
                    'x',
                    'y',
                    'z',
                    'specific_potential_energy',
                    'specific_internal_energy',
                    'velocity_squared'
                    ]       
        else: # Reads the first line in the file and uses it as the column headers
            with open(FILENAME) as mor:
                for line in mor:
                    row = line.split() # splits the first row into different columns separated by spaces in between characters
                    return row     
    
    def setupUi(self, Dialog): #Sets up Dialog GUI window for all plots.
        Dialog.setObjectName("Dialog")
        Dialog.resize(1250, 700)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        #Set up pshbtn - "Create Plot"; links to readFile()
        self.pushButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.gridLayout.addWidget(self.pushButton, 4, 5, 1, 1)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.readFile) #connects button press to 'readFile' function

        #Set up spnbx - stepsize input for user-specified file
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox.setFont(font)
        self.gridLayout.addWidget(self.spinBox, 2, 0, 1, 1)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setRange(1, 999999)

        #Set up spnbx2 - Size of scatter plot points
        self.spinBox2 = QtWidgets.QSpinBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox2.setFont(font)
        self.gridLayout.addWidget(self.spinBox2, 3, 0, 1, 1)
        self.spinBox2.setMinimumWidth(100)
        self.spinBox2.setObjectName("spinBox2")
        self.spinBox2.setRange(1, 100)

        #Set up spnbx3 - Determines filenumber for energy.sph and col.sph 
        self.spinBox3 = QtWidgets.QSpinBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox3.setFont(font)
        self.gridLayout.addWidget(self.spinBox3, 2, 2, 1, 1)
        self.spinBox3.setMaximumWidth(200)
        self.spinBox3.setObjectName("spinBox3")
        self.spinBox3.setRange(0, 999999)

        #Set up spnbx4 - Determines trendline type (1 for linear regression, 2 for quadratic, 3 for) 
        self.spinBox4 = QtWidgets.QSpinBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.spinBox4.setFont(font)
        self.gridLayout.addWidget(self.spinBox4, 3, 2, 1, 1)
        self.spinBox4.setMaximumWidth(200)
        self.spinBox4.setObjectName("spinBox4")
        self.spinBox4.setRange(1, 30)

        #Set up lbl - "Stepsize"
        self.label = QtWidgets.QLabel(Dialog)
        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        #Set up lbl2 - "X-Axis"
        self.label2 = QtWidgets.QLabel(Dialog)
        self.gridLayout.addWidget(self.label2, 0, 3, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label2.setFont(font)
        self.label2.setObjectName("label2")

        #Set up lbl3 - "Y-Axis"
        self.label3 = QtWidgets.QLabel(Dialog)
        self.gridLayout.addWidget(self.label3, 0, 4, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label3.setFont(font)
        self.label3.setObjectName("label3")

        #Set up lbl4 - "Scatter size"
        self.label4 = QtWidgets.QLabel(Dialog)
        self.gridLayout.addWidget(self.label4, 3, 1, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label4.setFont(font)
        self.label4.setObjectName("label4")

        #Set up lbl5 - "Z-axis column"
        self.label5 = QtWidgets.QLabel(Dialog)
        self.gridLayout.addWidget(self.label5, 0, 5, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label5.setFont(font)
        self.label5.setObjectName("label5")

        #Set up lbl6 - "File Number"
        self.label6 = QtWidgets.QLabel(Dialog)
        self.gridLayout.addWidget(self.label6, 2, 3, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label6.setFont(font)
        self.label6.setObjectName("label6")

        #Set up lbl6 - "Trend type"
        self.label7 = QtWidgets.QLabel(Dialog)
        self.gridLayout.addWidget(self.label7, 3, 3, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label7.setFont(font)
        self.label7.setObjectName("label7")

        #Set up list - list of columns in user-specified file for x-axis
        self.listWidget = QtWidgets.QListWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setMaximumWidth(250)
        for i in range(self.countCol()): #Creates items to list widget.
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 1, 3, 1, 1)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        #Set up list2 - list of columns in user-specified file for y-axis
        self.listWidget2 = QtWidgets.QListWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.listWidget2.setFont(font)
        self.listWidget2.setObjectName("listWidget2")
        self.listWidget2.setMaximumWidth(250)
        for i in range(self.countCol()): #Creates items to list widget.
            item2 = QtWidgets.QListWidgetItem()
            self.listWidget2.addItem(item2)
        self.gridLayout.addWidget(self.listWidget2, 1, 4, 1, 1)
        self.listWidget2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        #Set up list3 - list of columns in user-specified file for z-axis - 3-D Plots only!
        self.listWidget3 = QtWidgets.QListWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.listWidget3.setFont(font)
        self.listWidget3.setObjectName("listWidget3")
        self.listWidget3.setMaximumWidth(250)
        for i in range(self.countCol()): # Creates items to list widget. Items are then retranslated in the retranslateUi() further below.
            item3 = QtWidgets.QListWidgetItem()
            self.listWidget3.addItem(item3)
        self.gridLayout.addWidget(self.listWidget3, 1, 5, 1, 1)
        self.listWidget3.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        #Set up txtbrwsr - Info for how to use window
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 2, 3)
        self.textBrowser.setObjectName("textBrowser")
    
        #Set up chkbox - Enables sharing axis for plots.
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 4, 3, 1, 1)

        #Set up chkbox2 - Change between line plots to scatter plots.
        self.checkBox2 = QtWidgets.QCheckBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox2.setFont(font)
        self.checkBox2.setObjectName("checkBox2")
        self.gridLayout.addWidget(self.checkBox2, 3, 4, 1, 1)

        #Set up chkbox3 - Change between 2-D to 3-D plots.
        self.checkBox3 = QtWidgets.QCheckBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox3.setFont(font)
        self.checkBox3.setObjectName("checkBox3")
        self.gridLayout.addWidget(self.checkBox3, 2, 5, 1, 1)

        #Set up chkbox4 - Add trendline to subplots.
        self.checkBox4 = QtWidgets.QCheckBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox4.setFont(font)
        self.checkBox4.setObjectName("checkBox4")
        self.gridLayout.addWidget(self.checkBox4, 3, 5, 1, 1)

        #Set up chkbox5 - Add legends to subplots.
        self.checkBox5 = QtWidgets.QCheckBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox5.setFont(font)
        self.checkBox5.setObjectName("checkBox5")
        self.gridLayout.addWidget(self.checkBox5, 4, 4, 1, 1)

        #Set up chkbox6 - Fit all y-columns into one plot
        self.checkBox6 = QtWidgets.QCheckBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox6.setFont(font)
        self.checkBox6.setObjectName("checkBox6")
        self.gridLayout.addWidget(self.checkBox6, 2, 4, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        return

    def show_popupOutOfBounds(self): #Gives user warning popup of multiple selected columns exceeds six or none is selected.
        """Creates and shows an error popup if number of selected columns is not in the correct range (1-4)"""
        msg = QMessageBox()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        msg.setWindowTitle("Hold on there, Jethro!")
        msg.setText("\nError: Column has not been selected OR the number of columns selected has been exceeded.\n")
        msg.setInformativeText("Please reselect your desired columns - Max is four.\n")
        msg.setIcon(QMessageBox.Warning)
        msg.setFont(font)
        showMessage = msg.exec_()
        return

    def show_popupOutOfBounds3D(self): #Gives user warning popup of multiple selected columns in x, y, and z axis is > 1 or none .
        """Creates and shows an error popup if number of selected columns is not in the correct range (1-4)"""
        msg = QMessageBox()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        msg.setWindowTitle("Hold on there, Jethro!")
        msg.setText("\nError: Column has not been selected OR the number of columns selected has been exceeded.\n")
        msg.setInformativeText("Please reselect your desired columns - Only one for each axis!\n")
        msg.setIcon(QMessageBox.Warning)
        msg.setFont(font)
        showMessage = msg.exec_()
        return

    def show_popupE(self, new_filename: str = ''): #Gives user warning popup for fileNumber not found
        """Creates and shows an error popup if file number of the file name is not found in the directory"""
        msg = QMessageBox()
        msg.setWindowTitle("Hold on there, Jethro!")
        msg.setText(f"\nError: {new_filename} could not be found in the directory.\n")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        msg.setInformativeText("Make sure your file is in your current directory before creating the plot!")
        msg.setDetailedText(f"Your current directory path is: \n" + "_"*44 + "\n" + str(os.getcwd()))
        msg.setIcon(QMessageBox.Warning)
        msg.setFont(font)
        showMessage = msg.exec_() # Shows the popup error message window
        return

    def show_popupMismatch(self): #Gives user warning popup for mismatched data lengths in selected columns
        """Gives user warning popup for mismatched data lengths in selected columns"""
        msg = QMessageBox()
        msg.setWindowTitle("Hold on there, Jethro!")
        msg.setText("\nError: One or more of your selected columns do not share the same amount of data values!\n")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        msg.setInformativeText("Check your data file to make sure every column has the same length!")
        msg.setIcon(QMessageBox.Warning)
        msg.setFont(font)
        showMessage = msg.exec_()
        return

    def show_popupRegression(self):
        msg = QMessageBox()
        msg.setWindowTitle("Hold on there, Jethro!")
        msg.setText("\nError: The selected polynomial degree for your trendline did converge with one or more your selected data!\n")
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        msg.setInformativeText("Try choosing a smaller poly degree value and try again.")
        msg.setIcon(QMessageBox.Warning)
        msg.setFont(font)
        showMessage = msg.exec_()
        return 

    def retranslateUi(self, Dialog): # Retranslates various buttons, items in list, and labels from the empty default
        global FILENAME
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", f"Hypermongo - {FILENAME}"))
        self.pushButton.setText(_translate("Dialog", "Create Plot"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        for i in range(self.countCol()):
            item = self.listWidget.item(i)
            item.setText(_translate("Dialog", f"{i+1}. {self.setName()[i]}"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        __sortingEnabled2 = self.listWidget2.isSortingEnabled()
        self.listWidget2.setSortingEnabled(False)
        for i in range(self.countCol()):
            item2 = self.listWidget2.item(i)
            item2.setText(_translate("Dialog", f"{i+1}. {self.setName()[i]}"))
        self.listWidget2.setSortingEnabled(__sortingEnabled2)
        __sortingEnabled3 = self.listWidget3.isSortingEnabled()
        self.listWidget3.setSortingEnabled(False)
        for i in range(self.countCol()):
            item3 = self.listWidget3.item(i)
            item3.setText(_translate("Dialog", f"{i+1}. {self.setName()[i]}"))
        self.listWidget3.setSortingEnabled(__sortingEnabled3)
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Hypermongo</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">_____________________</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">You may select one x-axis column and up to a maximum of </span><span style=\" font-size:16pt; font-weight:600;\">six</span><span style=\" font-size:16pt;\"> y-axis columns on the right. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Select multiple items by holding Ctrl then clicking on the items, or holding down the mouse button and dragging.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Stepsize</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Enter the stepsize of the plot. This tells how many lines of data to skip and plot.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Higher numbers yield faster plotting speeds at the expense of accuracy.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Minimum number is &quot;1&quot;</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Share x-ax</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Checking this box will enable all plots to reduce the space in between plots and share the same x-axis. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">with no whitespace in between.</span></p></body></html>"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Scatter</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Checking this box enables scatter plot mode over the default line plot. The size of data points is adjustable with the Scatter size box. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">3-D Plots</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Checking 3-D plots box allows you to create a single 3-D plot by selecting only one item from each axis column. Compatible with the Scatter options.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">File number</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">This is only used for energy.sph files. Allows user to change which numbered energy file to read: Default is 0 for energy0.sph.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Trendline & Poly Degree</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">When the Trendline box is selected, each subplot will display dashed line based on the least squares fit of the data. A poly(nomial) degree of 1 is for linear regressions, degree of 2 is quadratic, and so on.</span></p>\n"))

        self.label.setText(_translate("Dialog", "Stepsize"))
        self.label2.setText(_translate("Dialog", " X-axis column"))
        self.label3.setText(_translate("Dialog", " Y-axis column"))
        self.label4.setText(_translate("Dialog", "Scatter size  "))
        self.label5.setText(_translate("Dialog", " Z-axis column"))
        self.label6.setText(_translate("Dialog", "File Number"))
        self.label7.setText(_translate("Dialog", "Poly Degree"))
        self.checkBox.setText(_translate("Dialog", "Share x-ax     "))
        self.checkBox2.setText(_translate("Dialog", "Scatter   "))
        self.checkBox3.setText(_translate("Dialog", "3-D plot   "))
        self.checkBox4.setText(_translate("Dialog", "Trendline"))
        self.checkBox5.setText(_translate("Dialog", "Legend"))
        self.checkBox6.setText(_translate("Dialog", "Single plot"))
        return

#-------------------------------------------------------------------------------#
# This contains the graphing functions which creates and shows a plot w/ pyplot #
#-------------------------------------------------------------------------------#

def grph(labels, yplot, file, numCol, share_ax: bool = False, is_scatter: bool = False, scatsize: int = 1, is_trendline: bool = False, polyDeg: int = 1, legend: bool = False): #Takes list of y axis labels, values from data file, file name, number of columns selected, and whether shared axis is selected. Creates and shows plot.
    """Universal graphing function for both data files. Takes labels and data from
       respective functions creates up to 6 data versus time plots.
    """
    plt.ion()
    fig = plt.figure(figsize=(12,9))
    plt.style.use('default')
    plt.rcParams['axes.linewidth'] = 1.5
    fig.canvas.manager.set_window_title("HM: " + str(file)) # Changes the plot title for the plot window itself.
    ax_dict = {} #Declares a dictionary variable for looping the creation of axis subplots
    ax1 = plt.subplot(numCol,1,1)
    if is_scatter:
        ax1.scatter(yplot[0], yplot[1], s = scatsize, label = f'{labels[1]}') # sets up first subplot as a scatter plot 
    else:
        ax1.plot(yplot[0], yplot[1], label = f'{labels[1]}') # Sets up first subplot as a line plot
    if is_trendline: # Adds trendline to first subplot when true
        try:
            y = np.poly1d(np.polyfit(yplot[0], yplot[1], polyDeg))
            if polyDeg == 1: # For linear regressions (poly degree of 1) displays a linear equation for the legend
                m = (y(yplot[0])[1]-y(yplot[0])[0])/(yplot[0][1]-yplot[0][0]) # solve for the slope of linear regression
                b = y(yplot[0])[0] - m*yplot[0][0] # solve for the y-intercept for the linear regression
                m_trunc = format(m, '.4g') # rounds up to 4 significant figures. the '.#g' tells to float to stay in either exponential or regular form.
                b_trunc = format(b, '.4g')
                ax1.plot(yplot[0], y(yplot[0]), "r--", label = f'y= {m_trunc}x + {b_trunc}')
            # takes data and creates the y axis for poly fit.
            # plots trendline to the subplot
            else:
                ax1.plot(yplot[0], y(yplot[0]), "r--", label = f'Degree {polyDeg}')
        except:
            Ui_Dialog_User.show_popupRegression(Ui_Dialog_User)
            return
    if legend: # Creates legend for first subplot
        ax1.legend(loc='upper right') 
    ax1.set_ylabel(labels[1]+'\n', fontsize = 16)
    ax1.yaxis.get_offset_text().set_x(1.005) # This changes the location of the exponential multiplier (if it exists) to the top-right of the subplot.
    if share_ax:
        plt.setp(ax1.get_xticklabels(), visible=False) # turns off axis label for the first subplot
    plt.grid(True, which = 'both')
    ax_list = [ax1]
    for i in range(1, numCol):
        ax_dict["ax%s" %(i+1)] = plt.subplot(numCol,1,i+1, sharex = ax1) # Uses a dictionary loop trick to create new ax variables depending on how many y-axis columns were chosen, instead of declaring variables beforehand. 
        if is_scatter:
            ax_dict["ax%s" %(i+1)].scatter(yplot[0], yplot[i+1], s = scatsize, label = f'{labels[i+1]}') # Sets up scatter plot with point size 's'
        else:
            ax_dict["ax%s" %(i+1)].plot(yplot[0], yplot[i+1], label = f'{labels[i+1]}')# Sets up line plot
        if is_trendline: # Adds trendline to other subplots when true
            try: # for linear regressions, y = mx + b
                y = np.poly1d(np.polyfit(yplot[0], yplot[i+1], polyDeg)) # takes data and calculates linear regression
                if polyDeg == 1:
                    m = (y(yplot[0])[1]-y(yplot[0])[0])/(yplot[0][1]-yplot[0][0]) # solve for the slope of linear regression
                    b = y(yplot[0])[0] - m*yplot[0][0]
                    m_trunc = format(m, '.4g')
                    b_trunc = format(b, '.4g')
                    ax_dict["ax%s" %(i+1)].plot(yplot[0], y(yplot[0]), "r--", label = f'y= {m_trunc}x + {b_trunc}')
                else:
                    ax_dict["ax%s" %(i+1)].plot(yplot[0], y(yplot[0]), "r--", label = f'Degree {polyDeg}') # plots trendline to the subplot
            except:
                Ui_Dialog_User.show_popupRegression(Ui_Dialog_User)
                return
        ax_dict["ax%s" %(i+1)].set_ylabel(labels[i+1]+'\n', fontsize = 16)
        plt.grid(True, which = 'both')
        if legend: # Creates legends for all subsequent subplots
            ax_dict["ax%s" %(i+1)].legend(loc='upper right') 
        ax_dict["ax%s" %(i+1)].yaxis.get_offset_text().set_x(1.005) # This changes the location of the exponential multiplier (if it exists) to the top-right of the subplot.
        ax_list.append(ax_dict["ax%s" %(i+1)]) # Appends dictionary axis to list
        if share_ax and i < numCol-1:
            plt.setp(ax_dict["ax%s" %(i+1)].get_xticklabels(), visible = False) # turns off numbered x-labels for all other subplots if share_ax is true. 
    plt.xlabel(labels[0], fontsize = 16) # Labels the x-axis with respect to entry in the first column and first row of the file
    if share_ax: # This adjusts the space in between the subplots to 0 if share_ax is true, otherwise the minimum distance is 0.20.
        plt.subplots_adjust(hspace = 0)
    else:
        plt.subplots_adjust(hspace = 0.20)
    plt.subplots_adjust(top = 0.97) # Adjustments to the placement of the subplots to better utilize the whitespace
    plt.subplots_adjust(bottom = 0.07)
    Ui_MainWindow.multi = MultiCursor(fig.canvas, (ax_list), color = 'r', lw = 1) # MultiCursor function to show vertical red line on all subplots with the mouse.
    return plt.show()

def onePlot2D(labels, yplot, file, numCol, share_ax: bool = False, is_scatter: bool = False, scatsize: int = 1, is_trendline: bool = False, polyDeg: int = 1, legend: bool = False): # Condenses all chosen y-columns into one plot
    plt.ion()
    fig = plt.figure(figsize=(12,9))
    plt.style.use('default')
    plt.rcParams['axes.linewidth'] = 1.5
    fig.canvas.manager.set_window_title("HM: " + str(file)) # Changes the plot title for the plot window itself.
    #ax = plt.plot()
    if is_scatter:
        plt.scatter(yplot[0], yplot[1], s = scatsize, label = f'{labels[1]}') # sets up first subplot as a scatter plot 
    else:
        plt.plot(yplot[0], yplot[1], label = f'{labels[1]}') # Sets up first subplot as a line plot
    if is_trendline: # Adds trendline to first subplot when true
        try:
            y = np.poly1d(np.polyfit(yplot[0], yplot[1], polyDeg))
            if polyDeg == 1: # For linear regressions (poly degree of 1) displays a linear equation for the legend
                m = (y(yplot[0])[1]-y(yplot[0])[0])/(yplot[0][1]-yplot[0][0]) # solve for the slope of linear regression
                b = y(yplot[0])[0] - m*yplot[0][0] # solve for the y-intercept for the linear regression
                m_trunc = format(m, '.4g') # rounds up to 4 significant figures. the '.#g' tells to float to stay in either exponential or regular form.
                b_trunc = format(b, '.4g')
                plt.plot(yplot[0], y(yplot[0]), "r--", label = f'y= {m_trunc}x + {b_trunc}')
            # takes data and creates the y axis for poly fit.
            # plots trendline to the subplot
            else:
                plt.plot(yplot[0], y(yplot[0]), "r--", label = f'Degree {polyDeg}')
        except:
            Ui_Dialog_User.show_popupRegression(Ui_Dialog_User)
            return
    
    #plt.set_ylabel(labels[1]+'\n', fontsize = 16)
    
    plt.grid(True, which = 'both')
    for i in range(1, numCol):
        if is_scatter:
            plt.scatter(yplot[0], yplot[i+1], s = scatsize, label = f'{labels[i+1]}') # Sets up scatter plot with point size 's'
        else:
            plt.plot(yplot[0], yplot[i+1], label = f'{labels[i+1]}')# Sets up line plot
        if is_trendline: # Adds trendline to other subplots when true
            try: # for linear regressions, y = mx + b
                y = np.poly1d(np.polyfit(yplot[0], yplot[i+1], polyDeg)) # takes data and calculates linear regression
                if polyDeg == 1:
                    m = (y(yplot[0])[1]-y(yplot[0])[0])/(yplot[0][1]-yplot[0][0]) # solve for the slope of linear regression
                    b = y(yplot[0])[0] - m*yplot[0][0]
                    m_trunc = format(m, '.4g')
                    b_trunc = format(b, '.4g')
                    plt.plot(yplot[0], y(yplot[0]), "r--", label = f'y= {m_trunc}x + {b_trunc}')
                else:
                    plt.plot(yplot[0], y(yplot[0]), "r--", label = f'Degree {polyDeg}') # plots trendline to the subplot
            except:
                Ui_Dialog_User.show_popupRegression(Ui_Dialog_User)
                return
        #ax1.set_ylabel(labels[i+1]+'\n', fontsize = 16)
        plt.grid(True, which = 'both')
        #plt.yaxis.get_offset_text().set_x(1.005) # This changes the location of the exponential multiplier (if it exists) to the top-right of the subplot.
    plt.xlabel(labels[0], fontsize = 16) # Labels the x-axis with respect to entry in the first column and first row of the file
    if legend: # Creates legend for first subplot
        plt.legend(loc='upper right') 
    if share_ax: # This adjusts the space in between the subplots to 0 if share_ax is true, otherwise the minimum distance is 0.20.
        plt.subplots_adjust(hspace = 0)
    else:
        plt.subplots_adjust(hspace = 0.20)
    plt.subplots_adjust(top = 0.97) # Adjustments to the placement of the subplots to better utilize the whitespace
    plt.subplots_adjust(bottom = 0.07)
    #Ui_MainWindow.multi = MultiCursor(fig.canvas, plt, color = 'r', lw = 1) # MultiCursor function to show vertical red line on all subplots with the mouse.
    return plt.show()

def threeDGrph(threeDplots: list = [], threeDlabels: list = [], is_scatter: bool = False, file: str = '', scatsize: int = 0): # 3-D Graphing functions
    plt.ion()
    fig = plt.figure(figsize=(10,10))
    plt.style.use('default') # Changes the visual style of the plot
    plt.rcParams['axes.linewidth'] = 1.5
    #plt.rcParams["figure.autolayout"] = True
    fig.canvas.manager.set_window_title("HM: " + str(file)) # Problem here with tight_layout fix later but not that important right now.
    ax = Axes3D(fig) # creates a 3D figure plot object
    if is_scatter: # Scatter plot with variable point sizes as 's', and changes the color of points based on z-axis ('c' and cmap)
        ax.scatter3D(threeDplots[0], threeDplots[1], threeDplots[2], c = threeDplots[2], cmap = 'cividis', s = scatsize)
    else: # Normal 3D line plot with default red line color
        ax.plot3D(threeDplots[0], threeDplots[1], threeDplots[2], 'red')
    ax.set_box_aspect(aspect = (1, 1, 1))#new aspect ratio 1:1
    ax.set_xlabel(threeDlabels[0], fontsize = 18) # Labels the x, y, and z axis.
    ax.set_ylabel(threeDlabels[1], fontsize = 18)
    ax.set_zlabel(threeDlabels[2], fontsize = 18)
    plt.show()

# Add your own graphing functions here if you wish to set up your own custom graphing 

#-----------------------------------------------#
# Initializes the Mainwindow GUI for Hypermongo #
#-----------------------------------------------#

if __name__ == "__main__": #This program is meant to be run as a script
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())