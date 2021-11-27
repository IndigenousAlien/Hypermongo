import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
import subprocess as sp
import numpy as np
import os
#Purpose: Uses pyplot to improve SM energy-time plots.
#Author: Jacky Tran @Allegheny College
#Version: alpha 0.85
#Date: 2/11/2021

#variables: t,epot,ekin,eint,etot
#read energy0.sph and have it compute and graph energy plots
#Currently can plot energy vs. time graphs, and can choose file number and step size
#New Features: User name is called and printed. Default values in function are set
#              to "v", 0, and 1 to draw simple energy graphs. Warning and stepsize set 
#              to default value if < 1. v and vln commands draws linear and logarithmic 
#              graphs respectively. Graph drawing optimized. Code no longer breaks when
#              user inputs unexpected values. Program asks to exit at the end of graphing.
# Future ideas: 
#              Add way to change title of graph using a command
#              Create separate file which calls functions from here instead.(add more commands)

#d = {}
#ax1 = plt.subplot(numCol,1,1)
#for i in range(0, 4):
#    d["ax%s" %i] = plt.subplot(4,1,1)
#    d["ax%s" %i].plot(yplot[0], yplot[i+1])

firstname = "finger ${USER} | head -n1 | gawk '{print $4}'"
print("\nThis is a working python version of SM. Start by")
print("entering the energy.sph file number and the step size.\n")
sp.call(firstname, shell = True)
#print(f"hello {sp.call(firstname1, shell = True)}, please give me a command\n")
#print("Hello [user], please give me a command")
gtype = ""

def hmx(gtype, fileNum, stepsize):
    """Reads energy[i].sph file and creates four energy vs. time graphs:
    virial, potential, kinetic, total Energy. Allows zooming or adjusting
    of graphs.
    """
    t=[]
    epot=[]
    ekin=[]
    eint=[]
    etot=[]
    j = 0
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

    #plt.figure("HM:" + str(fileNum))
    ylabel = ['U','W','T','E'] #Sets labels for y-axis of each graph
    yplot = [t,eint,epot,ekin,etot] #Tells which energy to plot points for y-axis
    global numCol
    numCol = 4
    grph(ylabel, yplot)
    return

def hmxl (one, file, two, three):
    """
    """
    t = []
    col1 = []
    col2 = []
    col3 = []
    j = 0
    x = 0
    stepsize = int(input('Please enter your stepsize\n'))
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
                j += 1
    print("Reading lines 1 to", j, "in steps of", stepsize, "\n")
    ylabel = [name1, name2, name3]
    yplot = [t, col1, col2, col3]
    #plt.figure(f"HM: time vs. plots")
    grph(ylabel, yplot)
    return

def grph(ylabel, yplot):
    """
    """
    if numCol == 1:
        fig, ax1 = plt.subplots(1, sharex = True)
    elif numCol == 2:
        fig, (ax1, ax2) = plt.subplots(2, sharex = True)
    elif numCol == 3:
        fig, (ax1, ax2, ax3) = plt.subplots(3, sharex = True)
    else:
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex = True) #!!!
    fig.canvas.set_window_title("HM: " + str(file))
    d = {}
    ax1 = plt.subplot(4,1,1)
    ax1.plot(yplot[0], yplot[1])
    plt.grid(True, which = 'both')
    #ax1 = plt.subplot(numCol,1,1)
    for i in range(1, numCol):
        d["ax%s" %(i+1)] = plt.subplot(4,1,i+1, sharex=ax1) #Uses dictionary to loop and create new variables
        d["ax%s" %(i+1)].plot(yplot[0], yplot[i+1])
        #plt.subplot(numCol,1,i+1, sharex = ax1)
        #plt.plot(yplot[0], yplot[i+1])
        d["ax%s" %(i+1)].set_ylabel(ylabel[i], fontsize = 12)
        plt.grid(True, which = 'both')

    plt.xlabel('time', fontsize = 12)
    plt.subplots_adjust(hspace = 0)
    plt.subplots_adjust(top = 0.95)
    plt.subplots_adjust(bottom = 0.125)
    plt.subplots_adjust(right = 0.9)
    plt.subplots_adjust(left = 0.175)
    if numCol == 1:
        multi = MultiCursor(fig.canvas, (ax1), color = 'r', lw = 1)
    elif numCol == 2:
        multi = MultiCursor(fig.canvas, (ax1, d['ax2']), color = 'r', lw = 1)
    elif numCol == 3:
        multi = MultiCursor(fig.canvas, (ax1, d['ax2'], d['ax3']), color = 'r', lw = 1)
    else:
        multi = MultiCursor(fig.canvas, (ax1, d['ax2'], d['ax3'], d['ax4']), color = 'r', lw = 1)
    plt.show()
    return

while (gtype != "yes"):
    try: #This exists to prevent code from breaking when user inputs unexpected values.
        gtype = input("Enter the graph type. Enter 'o' for options or 'close' to exit.\n")
        if gtype == 'close':
            gtype = 'yes'
        elif gtype == 'o':
            print('\nGraph Type Options:\nv - Graph of energy output\nm - Graph of massAndMore.out\nclose - quit program\n')
        elif gtype == 'v':
            fileNum, stepsize = [str(i) for i in input('file number and step size\n').split()]
            file = 'energy' + fileNum +'.sph'
            if os.path.isfile(file) == False:
                print('Error: Please check to make sure', file, 'is in your current directory.\n')
            else:
                hmx(gtype, int(fileNum), int(stepsize))
        elif gtype == 'm':
            file = 'massAndMore.out'
            if os.path.isfile(file) == False:
                print('Error: Please check to make sure', file, 'is in the current directory.\n')
            else:
                print('Enter # of which 2 columns you wish to graph:\n1 - m1\n2 - m2\n3 - x1\n4 - y1\n5 - z1')
                print('6 - x2\n7 - y2\n8 - z2\n9 - separation\n10 - CE+eject m\n11 - semimajor a\n12 - eccentricity')
                print('13 - unbound m\n14 - spin1\n15 - spin2\n16 orb. period\n')
                while gtype != 'close':
                    try:
                        numCol = int(input('Enter the number of columns you wish to use vs. time (Max 3).\n'))
                        if numCol == 3:
                            Col1, Col2, Col3 = [int(i) for i in input('Enter 3 column numbers.\n').split()]
                            hmxl(int(Col1), str(file), int(Col2), int(Col3))
                            gtype = 'close'
                        elif numCol == 2:
                            Col1, Col2= [int(i) for i in input('Enter two column numbers.\n').split()]
                            hmxl(int(Col1), str(file), int(Col2), 0)
                            gtype = 'close'
                        elif numCol == 1:
                            Col1= int(input('Enter the column number.\n'))
                            hmxl(int(Col1), str(file), 0, 0)
                            gtype = 'close'
                        else:
                            print('Error: Please enter a valid number of columns (1-3).\n')
                    except:
                        print('Error: Please enter valid columns\n')
        else:
            print('Error: Please input a valid command (v or m).\n')
            gtype = input('Would you like to close the program? yes/no (Default is no)\n')
    except: # catches *all* exceptions
        print()