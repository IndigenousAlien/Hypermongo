import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
import subprocess as sp
import numpy as np
import os
#Purpose: Uses pyplot to improve SM energy-time plots.
#Author: Jacky Tran @Allegheny College
#Version: alpha 0.5
#Date: 10/13/2020

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

    plt.figure("HM:" + str(fileNum))

    ylabel = ['U','W','T','E'] #Sets labels for y-axis of each graph
    yplot = [eint,epot,ekin,etot] #Tells which energy to plot points for y-axis
    ax1 = plt.subplot(4,1,1) #this gets called twice for U otherwise sharex doesn't work
    for i in range(0,4): #loops for each potential energy graph
        ax1 = plt.subplot(4,1,i+1, sharex=ax1)
        if gtype == "vln" and i == 2:
            plt.plot(t, np.log10(yplot[i]))   
        else:
            plt.plot(t, yplot[i])
        plt.ylabel(ylabel[i])
        plt.grid(True, which='both')

    plt.xlabel('time', fontsize = 12)
    plt.subplots_adjust(hspace = 0)
    plt.subplots_adjust(top = 0.95)
    plt.subplots_adjust(bottom = 0.125)
    plt.subplots_adjust(right = 0.9)
    plt.subplots_adjust(left = 0.175)

    #multi = MultiCursor(fig.canvas, ax1 , color = 'r', lw = 1)
    plt.show()
    return

while (gtype != "yes"):
    try: #This exists to prevent code from breaking when user inputs unexpected values.
        gtype, fileNum, stepsize = [str(i) for i in input('Enter the graph type, file number, and step size\n').split()]
        file = 'energy' + fileNum +'.sph'
        if gtype != 'close':
            if gtype != 'v' and gtype != 'vln':
                print('Error: Please input a valid command (v or vln).\n')
            elif os.path.isfile(file) == False:
                print('Error: Please check to make sure', file, 'is in your current directory.\n')
            else:
                hmx(gtype, int(fileNum), int(stepsize))
        gtype = input('\nWould you like to close the program? yes/no (Default is no)\n')
    except: # catches *all* exceptions
        print()