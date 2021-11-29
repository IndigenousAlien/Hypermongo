#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import re
import os

#Purpose: Uses pyplot and PyQt5 GUI to improve SM plots.
#Author: Jacky Tran @Allegheny College
#Version: 1.4
#Date: 11/28/2021

#-----------------------------------------------------------------------------------------------#
# Reads energy#.sph + massAndMore.out, computes and graphs time versus plots                    #
# New Features:                                                                                 #
#              - Allows user to read the old massAndMore.out files in addition to new ones      #
#              - list widget in Mass window now updates depending on the header column of       #
#                the massAndMore.out file. More functions were added to help this process.      #
# Future ideas:                                                                                 #
#              - None for now                                                                   #
#-----------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------#
# Below here contains the functions which read output files and creates plots with MatPlot #
#------------------------------------------------------------------------------------------#

def checkNum(name1): #Checks if the string contains a number
    """This function takes a string and checks to see if it contains a number,
    then it returns True or False.
    """
    return any(i.isdigit() for i in name1)

def newName(ylabel, numCol): #Changes the names of yplots to add subscripts if it contains a number
    """This function takes a string and changes it to add a subscript
    for the massAndMore.out file, only if it contains a number. i.e m1 or x2...
    """
    for i in range(0,numCol):
        tempName = ylabel[i]
        if checkNum(tempName) == True:
            changeName = re.split("(\d+)", tempName) #the re.split splits a string if a number is found.
            if len(changeName) == 3:
                tempName = "$" + changeName[0] +"_{" + changeName[1] + "}$" + changeName[2]
            else:
                tempName = "$" + changeName[0] +"_{" + changeName[1] + "}$"
        ylabel[i] = tempName
    return ylabel 

def hmx(fileNum, stepsize, checkedBox):
    """Reads energy[i].sph file and creates four energy vs. time graphs:
    virial, potential, kinetic, total energy.
    """
    t=[]
    epot=[]
    ekin=[]
    eint=[]
    etot=[]
    j = 0
    file = "energy" + str(fileNum) + ".sph"
    if stepsize <1:
        stepsize = 1
        print("Warning: Stepsize cannot be less than 1, set to default value of 1.")
    with open(file) as nrg:
        for line in nrg:
            if j%stepsize == 0:
                row = line.split()
                t.append(float(row[0]))
                epot.append(float(row[1]))
                ekin.append(float(row[2]))
                eint.append(float(row[3]))
                etot.append(float(row[4]))
            j += 1
    print("Reading lines 1 to", j, "in steps of", stepsize, "\n")

    ylabel = ['U','W','T','E'] #Sets labels for y-axis of each graph
    yplot = [t,eint,epot,ekin,etot] #Tells which energy to plot points for y-axis
    numCol = 4
    grph(ylabel, yplot, file, numCol, checkedBox)
    return

def newColNum(oldNum):
    """Fixes old spacing issue in mass&More.out for the titles"""
    if oldNum < 11:
        return oldNum #no change
    elif oldNum == 11:
        newNum = oldNum + 1 #add one to column num
        return newNum
    elif oldNum in (12,13):
        newNum = oldNum + 2 #add two to column num
        return newNum
    elif oldNum in (14,15,16):
        newNum = oldNum + 3 #add three to column num
        return newNum

def hmxl (stepsize, numCol, one, two, three, four, checkedBox):
    """Reads massAndMore.out file and allows user to create up to 4 plots of data vs. time
    """
    t = []
    col1 = []
    col2 = []
    col3 = []
    col4 = []
    j = 0
    x = 0
    file = "massAndMore.out"
    with open(file) as mor:
        for line in mor:
            if x == 0:
                name1 = Ui_Dialog_mass.setName(Ui_Dialog_mass)[one]
                name2 = Ui_Dialog_mass.setName(Ui_Dialog_mass)[two]
                name3 = Ui_Dialog_mass.setName(Ui_Dialog_mass)[three]
                name4 = Ui_Dialog_mass.setName(Ui_Dialog_mass)[four]
                x = 1 # prevents names being overwritten and only else-statement below is read in for-loop.
            else:
                if j%stepsize == 0:
                    row = line.split()
                    t.append(float(row[0].replace('D', 'E')))
                    col1.append(float(row[one]))
                    if numCol > 1:
                        col2.append(float(row[two]))
                    if numCol > 2:
                        col3.append(float(row[three]))
                    if numCol > 3:
                        col4.append(float(row[four]))
                j += 1
    print("Reading lines 1 to", j, "in steps of", stepsize, "\n")
    ylabel = [name1, name2, name3, name4]
    ylabel = newName(ylabel, numCol)
    yplot = [t, col1, col2, col3, col4]
    grph(ylabel, yplot, file, numCol, checkedBox)
    return

def grph(ylabel, yplot, file, numCol, checkedBox):
    """Universal graphing function for both data files. Takes labels and data from
       respective functions creates up to 4 data versus time plots.
    """
    fig = plt.figure()
    fig.canvas.set_window_title("HM: " + str(file))
    ax_dict = {} #Declares a dictionary variable for looping the creation of axis subplots
    ax1 = plt.subplot(numCol,1,1)
    ax1.plot(yplot[0], yplot[1])
    ax1.set_ylabel(ylabel[0], fontsize = 12)
    plt.grid(True, which = 'both')
    ax_list = [ax1]
    for i in range(1, numCol):
        ax_dict["ax%s" %(i+1)] = plt.subplot(numCol,1,i+1, sharex = ax1) #Uses dictionary to loop and create new variables
        ax_dict["ax%s" %(i+1)].plot(yplot[0], yplot[i+1])
        ax_dict["ax%s" %(i+1)].set_ylabel(ylabel[i], fontsize = 12)
        plt.grid(True, which = 'both')
        ax_list.append(ax_dict["ax%s" %(i+1)]) #Appends dictionary axis to list
    plt.xlabel('time', fontsize = 12)
    if  checkedBox == True: # Checks whether the "share x-ax" check boxes in energy/mass window is selected
        plt.subplots_adjust(hspace = 0)
    else:
        plt.subplots_adjust(hspace = 0.5)
    plt.subplots_adjust(top = 0.95)
    plt.subplots_adjust(bottom = 0.1)
    plt.subplots_adjust(right = 0.9)
    plt.subplots_adjust(left = 0.175)
    Ui_MainWindow.multi = MultiCursor(fig.canvas, (ax_list), color = 'r', lw = 1) #Variations of MultiCursor functions to show red line on subplots on x-axis
    plt.show()
    return

#----------------------------------------------------#
# Everything below here is for the GUI of Hypermongo #
#----------------------------------------------------#

class Ui_MainWindow(object): #Creates a class object for the main window of Hypermongo
    def openWindow(self):  #Opens second window for energy/mass&more plots
        self.window = QtWidgets.QDialog()
        #if self.radioButton.isChecked() and os.path.isfile("energy" + str(fileNum) + ".sph") == False:
        #    self.show_popupE() #Creates window for energy.sph when button 1 is selected
        if self.radioButton.isChecked():
            self.ui = Ui_Dialog_energy()
            self.ui.setupUi(self.window)
            self.window.show()

        elif self.radioButton_2.isChecked() and os.path.isfile("massAndMore.out") == False: #Creates error window for mass&more.out when button is selected
            self.show_popupM()
        elif self.radioButton_2.isChecked() and os.path.isfile("massAndMore.out") == True:
            self.ui = Ui_Dialog_mass()
            self.ui.setupUi(self.window)
            self.window.show()
        else:
            pass
        return

    def show_popupE(self): #Gives user warning popup for fileNumber
        msg = QMessageBox()
        msg.setWindowTitle("Hold on there, Jethro!")
        msg.setText("Error: No + energy#.sph can be found in the directory.")
        msg.setInformativeText("Make sure your file is in your current directory before proceeding!")
        msg.setDetailedText(f"Your current directory path is: \n" + "_"*67 + "\n" + str(os.getcwd()))
        msg.setIcon(QMessageBox.Warning)
        showMessage = msg.exec_()
        return

    def show_popupM(self): #Gives user warning popup for fileNumber
        msg = QMessageBox()
        msg.setWindowTitle("Hold on there, Jethro!")
        msg.setText("Error: massAndMore.out could not be found in the directory.")
        msg.setInformativeText("Make sure your file is in your current directory before proceeding!")
        msg.setDetailedText(f"Your current directory path is: \n" + "_"*67 + "\n" + str(os.getcwd()))
        msg.setIcon(QMessageBox.Warning)
        showMessage = msg.exec_()
        return

    def changeDir(self): #Changes current directory to new directory.
        _translate = QtCore.QCoreApplication.translate
        newPath = str(QFileDialog.getExistingDirectory(None, "Select Directory")) #Opens new window asking to select directory, sets it as a string.
        if newPath != '': 
            os.chdir(newPath) #Changes current directory to the string received from newPath
            self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">" + str(os.getcwd()) + "</span></p></body></html>"))
        else:
            pass
        return

    def setupUi(self, MainWindow): #Creates widgets and buttons on the main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(739, 382)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        #set up radio btn 1 - Energy plots
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.gridLayout.addWidget(self.radioButton, 2, 1, 1, 2)

        #Set up radio btn 2 - Mass&More plots
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.radioButton_2, 3, 1, 1, 3)

        #Set up txtbrwsr 1 - Info on program
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 5, 1)

        #Set up txtbrwsr 2 - Current directory info
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.gridLayout.addWidget(self.textBrowser_2, 1, 1, 1, 3)

        #Set up pshbtn 1 - Next button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openWindow)
        self.gridLayout.addWidget(self.pushButton, 4, 1, 1, 1)

        #Set up pshbtn 2 - Exit button
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.exit)
        self.gridLayout.addWidget(self.pushButton_2, 4, 2, 1, 2)

        #set up tlbtn - Access directory folders
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.changeDir)
        self.gridLayout.addWidget(self.toolButton, 0, 3, 1, 1)

        #Set up lbl - "Current Directory" label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 2)


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
        sys.exit()

    def retranslateUi(self, MainWindow): #Translates default text into more useful information in the main window.
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hypermongo"))
        self.radioButton.setText(_translate("MainWindow", "energy.sph"))
        self.radioButton_2.setText(_translate("MainWindow", "massAndMore.out"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Welcome to Hypermongo! </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">_______________________</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">This python program is a designed to create plots for two output files </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">- energy#.sph &amp; massAndMore.out</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Start by selecting a file you wish to plot, then press the &quot;Next&quot; button.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Make sure you are in the correct directory where your file(s) are located.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">You can change your directory by pressing the &quot;...&quot; button.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Have fun!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Author: Jacky Tran @Allegheny College 2021</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Email: jpamtran@gmail.com</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Next"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">" + str(os.getcwd()) + "</span></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Current Directory:"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Exit the program"))
        self.actionExit.setShortcut(_translate("MainWindow", "Esc"))
        return

class Ui_Dialog_energy(object): #Creates Dialog window for energy.sph plots

    def callHmx(self): #Reads spinbox values and calls hmx function
        fileNum = self.spinBox.value()
        stepsize = self.spinBox_2.value()
        checkedBox = self.checkBox.isChecked()
        if os.path.isfile("energy" + str(fileNum) + ".sph") == False:
            self.show_popupE(fileNum)
        else:
            hmx(fileNum, stepsize, checkedBox)
        return

    def setupUi(self, Dialog): #Sets up objects in Dialog window
        Dialog.setObjectName("Dialog")
        Dialog.resize(508, 400)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        #Set up txtbrwsr - Info on how to use window
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 8, 1)
        self.textBrowser.setObjectName("textBrowser")

        #Set up lbl 1 - "File Number"
        self.label = QtWidgets.QLabel(Dialog)
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        #Set up lbl 2 - "Stepsize"
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        #Set up spnbox 1 - user input for file number of energy#.sph
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBox.setFont(font)
        self.gridLayout.addWidget(self.spinBox, 1, 1, 1, 1)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setRange(0,999)

        #Set up spnbox 2 - user input for stepsize of energy#.sph
        self.spinBox_2 = QtWidgets.QSpinBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBox_2.setFont(font)
        self.gridLayout.addWidget(self.spinBox_2, 3, 1, 1, 1)
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_2.setRange(1,99999)

        #Set up pshbtn - Create plot button; links to callHmx()
        self.pushButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.gridLayout.addWidget(self.pushButton, 7, 1, 1, 1)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.callHmx)

        #Set up chkbox - Enables sharing axis of Energy plots
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.gridLayout.addWidget(self.checkBox, 5, 1, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        return

    def show_popupE(self, fileNum): #Gives user warning popup for fileNumber
        msg = QMessageBox()
        msg.setWindowTitle("Hold on there, Jethro!")
        msg.setText("Error: energy" + str(fileNum) + ".sph could not be found in the directory.")
        msg.setInformativeText("Make sure your file is in your current directory before creating the plot!")
        msg.setDetailedText(f"Your current directory path is: \n" + "_"*67 + "\n" + str(os.getcwd()))
        msg.setIcon(QMessageBox.Warning)
        showMessage = msg.exec_()
        return

    def retranslateUi(self, Dialog): #Retranslates default text on objects
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Hypermongo - Energy"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">HMX - Energy Plot</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">_____________________</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">File Number</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enter the file number of energy#.sph file.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The file number is shown as a digit on the file.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Default number is &quot;0&quot;</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Stepsize</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enter the stepsize of the plot.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Higher numbers yield faster calculations but may reduce accuracy.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Minimum number is &quot;1&quot;</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Note: </span>Setting stepsize higher than the # of line in the .sph</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">file will result in no data showing on the plot.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Share x-ax</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">checking box will enable all plots to share the same</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> x-axis with no whitespace in between</p></body></html>"))
        self.label.setText(_translate("Dialog", "File Number"))
        self.label_2.setText(_translate("Dialog", "Stepsize"))
        self.pushButton.setText(_translate("Dialog", "Create Plot"))
        self.checkBox.setText(_translate("Dialog", "Share x-ax"))
        return

class Ui_Dialog_mass(object): #Defines class creating dialog window for mass&more.out file
    
    def callHmxl(self): #Calls hmxl function after taking in spinbox and selected items in list
        text_list = self.listWidget.selectedItems()
        text = []
        stepsize = self.spinBox.value()
        checkedBox = self.checkBox.isChecked()
        for i in list(text_list):
            if i.text()[1:2] == ".":
                text.append(i.text()[0:1])
            else:
                text.append(i.text()[0:2])
        numCol = len(text)
        if os.path.isfile("massAndMore.out") == False:
            self.show_popupM()
        elif (numCol == 1):
            hmxl(stepsize, numCol, int(text[0]), 0, 0, 0, checkedBox)
        elif numCol == 2:
            hmxl(stepsize, numCol, int(text[0]), int(text[1]), 0, 0, checkedBox) 
        elif (numCol == 3):
            hmxl(stepsize, numCol, int(text[0]), int(text[1]), int(text[2]), 0, checkedBox)
        elif (numCol ==4):
            hmxl(stepsize, numCol, int(text[0]), int(text[1]), int(text[2]), int(text[3]), checkedBox)
        else:
            pass
        return

    def countCol(self):
        """Counts the number of header columns in massAndMore.out"""
        with open("massAndMore.out") as mor:
            for line in mor:
                row = len(line.split())
                if row == 21:
                    return row-4
                else: return row

    def setName(self):
        """Returns a list of names for the list widget in Ui_Dialog_mass class. Also used in hmxl()"""
        with open("massAndMore.out") as mor:
            nameList = []
            for line in mor:
                row = line.split() # splits the first row into different columns separated by spaces in between characters
                    #Note: Columns 10,11,13, and 16 in massAndMore.out have a single space separating the characters. This is resolved below.
                for x in range(Ui_Dialog_mass().countCol()):
                    if Ui_Dialog_mass().countCol() == 17:
                        if x in (10,11,13,16): #Combines two columns together for that specific row. Same for the other if-statements.
                            nameList.append(f"{row[newColNum(x)]} {row[newColNum(x)+1]}")
                        else:
                            nameList.append(row[newColNum(x)])
                    else:
                        nameList.append(row[x])
                return nameList
    
    def setupUi(self, Dialog): #Sets up Dialog window for mass&more plots.
        Dialog.setObjectName("Dialog")
        Dialog.resize(508, 400)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        #Set up pshbtn - "Create Plot"; links to callHmxl()
        self.pushButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.gridLayout.addWidget(self.pushButton, 2, 2, 1, 1)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.callHmxl) #connects button press to 'callHmxl' function

        #Set up spnbx - stepsize input for mass&more.out
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBox.setFont(font)
        self.gridLayout.addWidget(self.spinBox, 1, 0, 1, 1)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setRange(1,99999)

        #Set up lbl - "Stepsize"
        self.label = QtWidgets.QLabel(Dialog)
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        #Set up list - list of columns in mass&more.out
        self.listWidget = QtWidgets.QListWidget(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.listWidget.setFont(font)
        self.listWidget.setObjectName("listWidget")
        for i in range(self.countCol()-1): #Creates items to list widget.
            item = QtWidgets.QListWidgetItem()
            self.listWidget.addItem(item)
        self.gridLayout.addWidget(self.listWidget, 0, 2, 2, 1)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        #Set up txtbrwsr - Info for how to use window
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 2)
        self.textBrowser.setObjectName("textBrowser")
    
        #Set up chkbox - Enables sharing axis for plots.
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        return

    def show_popupM(self): #Gives user warning popup if massAndMore.out could not be found in directory
        msg = QMessageBox()
        msg.setWindowTitle("Hold on there, Jethro!")
        msg.setText("Error: massAndMore.out could not be found in the directory.")
        msg.setInformativeText("Make sure your file is in your current directory before creating the plot!")
        msg.setDetailedText(f"Your current directory path is: \n" + "_"*74 + "\n" + str(os.getcwd()))
        msg.setIcon(QMessageBox.Warning)
        showMessage = msg.exec_()
        return

    def retranslateUi(self, Dialog): #Retranslates buttons and items in list from the default
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Hypermongo - Mass&More"))
        self.pushButton.setText(_translate("Dialog", "Create Plot"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        for i in range(self.countCol()-1):
            item = self.listWidget.item(i)
            item.setText(_translate("Dialog", f"{i+1}. {self.setName()[i+1]}"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">HM - Mass&amp;More Plot</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">________________</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">You may select up to a maximum of </span><span style=\" font-size:10pt; font-weight:600;\">four</span><span style=\" font-size:10pt;\"> (current) data columns on the right. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Select multiple items by holding Ctrl then click on three items.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Stepsize</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Enter the stepsize of the plot.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Higher numbers yield faster calculations but may reduce accuracy.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Minimum number is &quot;1&quot;</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">Share x-ax</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">checking box will enable all plots to share the same x-axis </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">with no whitespace in between</span></p></body></html>"))
        self.label.setText(_translate("Dialog", "Stepsize"))
        self.checkBox.setText(_translate("Dialog", "Share x-ax"))
        return

if __name__ == "__main__": #Initializes the MainWindow GUI of Hypermongo. This program is meant to be run as a script
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())