import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
import os
#Purpose: Uses pyplot to improve SM energy-time plots.
#Author: Jacky Tran @Allegheny College
#Version: 0.9
#Date: 7/11/2021

#variables: t,epot,ekin,eint,etot
#read energy0.sph and have it compute and graph energy plots
#Currently can plot data from "energy(x).sph" and "massAndMore.out" files
#New Features: 
#              - Implemented second data list, "massAndMore.out" which Hypermongo can 
#                set up to 3 different data lists vs. time.
#              - Added Multicursor function to keep track of all x-values on all subplots.
#              - Changed graphing function to use dictionary function to create variables.
#              - Optimized "grph" function using a list to reduce "if" statements.
# Future ideas: 
#              - Fully integrated GUI for easier use.
#              - Have Gonzales/Physics/other computers run Hypermongo.
#              - Allow free plotting of any data column vs. column.
#              - Dynamic visualization of data.
#              - Add units to the plots.
#              - Add way to display multiple figure windows at once
#                i.e have both massAndMore.out and energy.sph plotted.
print("\nThis is a working python version of SM. Start by")
print("entering the energy.sph file number and the step size.\n")
gtype = ""



def hmx(gtype, fileNum, stepsize):
    """Reads energy[i].sph file and creates four energy vs. time graphs:
    virial, potential, kinetic, total energy.
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

    ylabel = ['U','W','T','E'] #Sets labels for y-axis of each graph
    yplot = [t,eint,epot,ekin,etot] #Tells which energy to plot points for y-axis
    global numCol
    numCol = 4
    grph(ylabel, yplot)
    return

def hmxl (one, file, two, three):
    """Reads massAndMore.out file and allows user to create up to 3 plots of data vs. time
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
    grph(ylabel, yplot)
    return

def grph(ylabel, yplot):
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
    plt.subplots_adjust(hspace = 0.5)
    plt.subplots_adjust(top = 0.95)
    plt.subplots_adjust(bottom = 0.1)
    plt.subplots_adjust(right = 0.9)
    plt.subplots_adjust(left = 0.175)
    multi = MultiCursor(fig.canvas, (ax_list), color = 'r', lw = 1) #Variations of MultiCursor functions to show red line on subplots on x-axis
    plt.show()
    return

while (gtype != "yes"):
    try: #This exists to prevent code from breaking when user inputs unexpected values.
        gtype = input("Enter the graph type. Enter 'o' for options or 'close' to exit.\n")
        if gtype == 'close':
            gtype = 'yes'
        elif gtype == 'o':
            print('\nGraph Type Options:\nv - Graph of energy.sph\nm - Graph of massAndMore.out\nclose - quit program\n')
        elif gtype == 'v':
            fileNum, stepsize = [str(i) for i in input('file number (0 is default) followed by the step size\n').split()]
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