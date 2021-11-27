import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import re
import os

#Purpose: Uses pyplot and PyQt5 GUI to improve SM plots.
#Author: Jacky Tran @Allegheny College
#Version: 1.1
#Date: 9/7/2021

#-----------------------------------------------------------------------------------------------#
# Reads energy#.sph + massAndMore.out, computes and graphs time versus plots                    #
# New Features:                                                                                 #
#              - Implemented second data list, "massAndMore.out" which Hypermongo can           # 
#                set up to 3 different data lists vs. time.                                     #
#              - Added Multicursor function to keep track of all x-values on all subplots.      #
#              - Changed graphing function to use dictionary function to create variables.      #
#              - Optimized "grph" function using a list to reduce "if" statements.              #
#              - Fully integrated GUI added                                                     #
#              - Multiple plot windows can be created in one instance of Hypermongo running.    #
#              - Subscripts for labels of plots with numbers in them                            #
#              - Directory search bar                                                           #
#              - Add option to squish all axis together instead separating them                 #
# Future ideas:                                                                                 #
#              - Resize window and scale all widgets with window                                #
#-----------------------------------------------------------------------------------------------#

def checkNum(name1): #Checks if the string contains a number
    """This function takes a string and checks to see if it contains a number,
    then it returns True or False.
    """
    return any(i.isdigit() for i in name1)

def newName(ylabel, numCol): #Changes the names of yplots to add subscripts if it contains a number
    """This function takes a string and changes it to add a subscript
    for the massAndMore.out file, only if it contains a number. i.e m1 or x2...
    """
    changeName = re.compile("([a-zA-Z]+)([0-9]+)") #the re.compile splits a string if a number is found.
    for i in range(0,numCol):
        tempName = ylabel[i]
        if checkNum(tempName) == True:
            tempName = changeName.match(tempName).groups()
            tempName = "$" + tempName[0] + "_{" + tempName[1] + "}$"
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
    if stepsize <1:
        stepsize = 1
        print("Warning: Stepsize cannot be less than 1, set to default value of 1.")
    with open(file) as mor:
        for line in mor:
            if x == 0:
                row = line.split()
                name1 = row[one]
                name2 = row[two]
                name3 = row[three]
                name4 = row[four]
                x = 1
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

#------------------------------------------------------------------------#
# Everything below here is strictly for creating the GUI of Hypermongo   #
#------------------------------------------------------------------------#

class Ui_MainWindow(object): #Creates a class object for the main window of Hypermongo
    def openWindow(self):  #Opens second window for energy/mass&more plots
        self.window = QtWidgets.QDialog()
        if self.radioButton.isChecked(): #Creates window for energy.sph when button 1 is selected
            self.ui = Ui_Dialog_energy()
            self.ui.setupUi(self.window)
            self.window.show()
        elif self.radioButton_2.isChecked(): #Creates window for mass&more.out when button 2 is selected
            self.ui = Ui_Dialog_mass()
            self.ui.setupUi(self.window)
            self.window.show()
        else:
            pass
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
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">" + str(os.getcwd()) + "</span></p></body></html>"))
        else:
            pass
        return

    def setupUi(self, MainWindow): #Creates widgets and buttons on the main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(432, 271)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(250, 100, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(250, 140, 181, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 201, 201))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(230, 40, 191, 51))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(230, 180, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openWindow)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 180, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.exit)

        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(390, 10, 27, 22))
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.changeDir)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 10, 141, 21))
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 610, 29))
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
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt; font-weight:600;\">Welcome to Hypermongo! </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:7.8pt;\">_______________________</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:7.8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">This python program is a designed to create plots for two output files </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- energy#.sph &amp; massAndMore.out</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Start by selecting a file you wish to plot, then press the &quot;Next&quot; button.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Make sure you are in the correct directory where your file(s) are located.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">You can change your directory by pressing the &quot;...&quot; button.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Have fun!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Author: Jacky Tran @Allegheny College 2021</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Email: jpamtran@gmail.com</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Next"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">" + str(os.getcwd()) + "</span></p></body></html>"))
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
            self.show_popup(fileNum)
        else:
            hmx(fileNum, stepsize, checkedBox)
        return

    def setupUi(self, Dialog): #Sets up objects in Dialog window
        Dialog.setObjectName("Dialog")
        Dialog.resize(382, 269)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(30, 21, 201, 231))
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(260, 20, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(260, 90, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(260, 50, 63, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setRange(0,999)
        self.spinBox_2 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_2.setGeometry(QtCore.QRect(260, 130, 81, 22))
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_2.setRange(1,99999)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(260, 220, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.callHmx)

        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(260, 180, 101, 20))
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

    def show_popup(self, fileNum): #Gives user warning popup for fileNumber
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
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
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
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Default number is &quot;1&quot;</p>\n"
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
            self.show_popup()
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

    def setupUi(self, Dialog): #Sets up Dialog window for mass&more plots.
        Dialog.setObjectName("Dialog")
        Dialog.resize(361, 267)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(250, 230, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.callHmxl) #connects button press to 'callHmxl' function

        self.spinBox = QtWidgets.QSpinBox(Dialog)
        self.spinBox.setGeometry(QtCore.QRect(30, 200, 60, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setRange(1,99999)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(100, 200, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(200, 10, 141, 201))
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget.addItem(item)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(20, 10, 161, 181))
        self.textBrowser.setObjectName("textBrowser")

        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(70, 230, 121, 31))
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

    def show_popup(self): #Gives user warning popup if energy(filenumber).sph could not be found in directory
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
        item = self.listWidget.item(0)
        item.setText(_translate("Dialog", "1. m1"))
        item = self.listWidget.item(1)
        item.setText(_translate("Dialog", "2. m2"))
        item = self.listWidget.item(2)
        item.setText(_translate("Dialog", "3. x1"))
        item = self.listWidget.item(3)
        item.setText(_translate("Dialog", "4. y1"))
        item = self.listWidget.item(4)
        item.setText(_translate("Dialog", "5. z1"))
        item = self.listWidget.item(5)
        item.setText(_translate("Dialog", "6. x2"))
        item = self.listWidget.item(6)
        item.setText(_translate("Dialog", "7. y2"))
        item = self.listWidget.item(7)
        item.setText(_translate("Dialog", "8. z2"))
        item = self.listWidget.item(8)
        item.setText(_translate("Dialog", "9. separation"))
        item = self.listWidget.item(9)
        item.setText(_translate("Dialog", "10. CE+ejecta m"))
        item = self.listWidget.item(10)
        item.setText(_translate("Dialog", "11. semimajor a"))
        item = self.listWidget.item(11)
        item.setText(_translate("Dialog", "12. eccentricity"))
        item = self.listWidget.item(12)
        item.setText(_translate("Dialog", "13. unbound m"))
        item = self.listWidget.item(13)
        item.setText(_translate("Dialog", "14. spin1"))
        item = self.listWidget.item(14)
        item.setText(_translate("Dialog", "15. spin2"))
        item = self.listWidget.item(15)
        item.setText(_translate("Dialog", "16. orb. period"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">HM - Mass&amp;More Plot</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">________________</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You may select up to a maximum of <span style=\" font-weight:600;\">four</span> (current) data columns on the right. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select multiple items by holding Ctrl then click on three items.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Stepsize</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enter the stepsize of the plot.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Higher numbers yield faster calculations but may reduce accuracy.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Default number is &quot;1&quot;</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Share x-ax</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">checking box will enable all plots to share the same x-axis </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">with no whitespace in between</p></body></html>"))
        self.label.setText(_translate("Dialog", "Stepsize"))
        self.checkBox.setText(_translate("Dialog", "Share x-ax"))
        return

if __name__ == "__main__": #Initializes the MainWindow GUI of Hypermongo. Program quits when closed
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())