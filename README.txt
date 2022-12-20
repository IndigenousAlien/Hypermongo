
                          #_____________________________________________________________________#
                          |    _   _                                                            |
                          |   | | | |                                                           |
                          |   | |_| |_   _ _ __   ___ _ __ _ __ ___   ___  _ __   __ _  ___     |
                          |   |  _  | | | | '_ \ / _ \ '__| '_ ` _ \ / _ \| '_ \ / _` |/ _ \    |
                          |   | | | | |_| | |_) |  __/ |  | | | | | | (_) | | | | (_| | (_) |   |
                          |   \_| |_/\__, | .__/ \___|_|  |_| |_| |_|\___/|_| |_|\__, |\___/    |
                          |           __/ | |                                     __/ |         |
                          |          |___/|_|                                    |___/          |
                          #_____________________________________________________________________#


Hypermongo is an open-source data visualization tool designed to create plots for the SPH code (written by Gaburov, Lombardi & Portegies Zwart 2010) Starsmasher. The purpose is to utilize Python's pyplot and PyQt packages which provide additional tools and give a simpler user interface to viewing data plots, compared to Robert Lupton and Patricia Monger's "Supermongo".

 by reading the first line of a data file as the title columns. The columns in the data file must be separated by spaces. Hypermongo design is to supplement Supermongo in such cases when a user wishes to read new data files without needing to create custom macros. 

In it's simplest form, Hypermongo reads data files with columns separated by spaces in between values with the first row containing the name(s) of the each column of data; it then auto-populates data columns in a list. There are a total of 3 lists that contain the same column titles, giving the user the ability to create x, y, and z plots in any way they wish.

_________________________________________________________________________________________________________________________________

INSTALLATION:
You can find all neccessary files for Hypermongo at my github repository: https://github.com/IndigenousAlien/Hypermongo

If you want to simply use Hypermongo, download the respective executable file for your OS (Windows, Mac, Linux) and run the program. 

However, if you wish to edit the code for yourself, a copy of the python script is included in this repository. If you have any plans to improve Hypermongo, please contact me at jtran9148@gmail.com so that I can add you as a contributor to this repository.

Note: if you wish to run the python file as a script, you must have anaconda3 installed for your OS Hypermongo uses anaconda3 which is a package manager that includes PyQt and MatPlotLib which is essential to Hypermongo. You can install anaconda3 at: https://www.anaconda.com/products/individual

Make sure you set your IDE to have Python ## (base: conda) as the interpreter!
_________________________________________________________________________________________________________________________________

Feel free to send any questions my way at jtran9148@gmail.com
If Hypermongo is being utilized for your comp. project, please be sure to credit my code and me and to cite my paper: "Modeling Tidal Disruption Encounters and Analysis with a Data Visualization Tool - Hypermongo."

Best,
Jacky Tran
