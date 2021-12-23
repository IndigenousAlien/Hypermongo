
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


Hypermongo is an open-source data visualization tool designed to create plots for the SPH code (written by Gaburov, Lombardi & Portegies Zwart 2010) Starsmasher -- principally Starsmasher's energy#.sph and mass&More.out files. The purpose is to utilize Python's pyplot and PyQt packages which provide a wider range of tools while viewing data plots, compared to Robert Lupton and Patricia Monger's "Supermongo". 

Currently, Hypermongo's use is limited to simple time vs. ... plots but can serve to be a more useful supplementary tool to Supermongo in such cases for its simplicity. Should there be a need to expand Hypermongo's toolset for additional output files, a brief explanation of how Hypermongo reads data will be described here: 

In it's simplest form, Hypermongo reads data files with columns separated by spaces in between values with the first row containing the name(s) of the each column of data; the format of the data should resemble something you would see in an excel spreadsheet. This code has separate functions to create lists using the column data in each row and appends them into separate lists for each column, but the code utilizes a shared graphing function which plots each column in a "time vs. ..." format. If you are creating your own data sheet for Hypermongo, I recommend placing the "time" column first as Hypermongo reads the first column as time. 

_________________________________________________________________________________________________________________________________

INSTALLATION:
You can find all neccessary files for Hypermongo at my github repository: https://github.com/IndigenousAlien/Hypermongo

If you want to simply use Hypermongo, download the respective executable file for your OS (Windows, Mac, Linux) and run the program. 

However, if you wish to view or edit the code for yourself, download the HypermongoPyQt.py file and open it with your preferred IDE for python. 
Note: if you wish to run the python file this way, you must have anaconda3 installed for your OS Hypermongo uses anaconda3 which is a package manager that includes PyQt and MatPlotLib which is essential to Hypermongo. You can install anaconda3 at: https://www.anaconda.com/products/individual

Make sure you set your IDE to have Python ## (base: conda) as the interpreter!
_________________________________________________________________________________________________________________________________

Feel free to send any questions my way at jtran9148@gmail.com
If Hypermongo is being utilized for your comp. project, please be sure to credit my code and me and to cite my paper: [paper in progress]

Best,
Jacky Tran
