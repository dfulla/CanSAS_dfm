import tables
import os

if os.path.isfile("H2O_100pc_2D_0.051kG.ABS.hdf5"):
    h5file = tables.open_file("H2O_100pc_2D_0.051kG.ABS.hdf5", driver="H5FD_CORE")
    print h5file
    
else:
  print "Could not locate file H2O_100pc_2D_0.051kG.ABS.hdf5"