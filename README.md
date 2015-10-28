# CanSAS_dfm
#

<p> Files: </p>

1. SAS_CanSAS.py
  1. Extracts Qx,Qy and I(Qx,Qy) from two files.
  2. Extracts metadata from the name of the two files (magnetic field value).
  2. Creates an h5 file. Inputs attributes (qi, indexes, name_of_sample etc).
  3. Inputs the data from the two files into the h5 file following the CanSAS format.
  4. Closes the h5 file which is then ready to be read. 
2. open_tables.py
  1. Opens an h5 (or hdf5) file and prints the structure (groups, datasets, size of arrays, etc).
3. open_h5.py
  1. Opens an h5 (or hdf5) file and returns a dictionary with the data contained in the file.
4. open_h5_class.py
5. plot_3d_sas.py
