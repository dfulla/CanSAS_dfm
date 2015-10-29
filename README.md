# CanSAS_dfm
#

<p> Files (python): </p>

1. **SAS_CanSAS.py**
  1. Extracts Qx,Qy and I(Qx,Qy) from two files.
  2. Extracts metadata from the name of the two files (magnetic field value).
  2. Creates an h5 file. Inputs attributes (qi, indexes, name_of_sample etc).
  3. Inputs the data from the two files into the h5 file following the CanSAS format.
  4. Closes the h5 file which is then ready to be read. 
2. **open_tables.py**
  1. Opens an h5 (or hdf5) file and prints the structure (groups, datasets, size of arrays, etc).
3. **open_h5.py**
  1. Opens an h5 (or hdf5) file and returns a dictionary with the data contained in the file.
4. **whats_in_dic.py**
  1. Prints the contain of the dictionary returned from the open_h5.py.
5. **plot_3d_sas.py**
  1. 3D plot of I(Qx,Qz) vs Qx,Qz from one *.ABS file
  2. Includes another method to plot both files simultaneously for comparison.
6. **plot_3d_from2files.py**
  1. Makes 2 plots in 3D from the 2 intensity arrays from the h5 file.


How to run the scripts
---

1. **SAS_CanSAS.py**
  1. option 1:
    1. python SAS_CanSAS.py
    2. the program prints the files .ABS files available
    3. user may copy/paste a combination of two files
    4. h5 file is created with data from the .ABS files
  2. option 2:
    1. python SAS_CanSAS.py file1.ABS file2.ABS
    2. file1 and file2 need to belong to the same sample. It will be verified.
    3. h5 file is created with data from the .ABS files
2. **open_tables.py**
   1. option 1:
     1. python open_tables
     2. Displays the h5 and/or hdf5 files available
     3. User copy/pastes one file
     4. Prints the structure of the h5 file (groups, datasets, array dimensions etc)
   2. option 2:
     1. python file.h5
     2. prints the structure of the h5 file (groups, datasets, array dimensions etc)
3. **open_h5.py**
   1. option 1:
     1. python open_h5.py
     2. user gets files available from the program
     3. user select one file
     4. program creates a dictionary
   2. option 2:
     1. python open_h5.py file.h5
     2. program creates a dictionary
     
   
