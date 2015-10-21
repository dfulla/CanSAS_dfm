import tables
import os
import sys


def print_h5_structure(h5):

    if os.path.isfile(h5):
        h5file = tables.open_file(h5, driver="H5FD_CORE")
        print h5file
        h5file.close()
    
    else:
        print "Could not locate file %s"%h5
        
if __name__ == '__main__':

    if len(sys.argv) == 1:
        h5 = raw_input("Write file to read:")
        if os.path.isfile(h5):
            print_h5_structure(h5)
        else:
            print "file %s not found"
    
    if len(sys.argv) == 2:
        h5 = sys.argv[1]
        if os.path.isfile(h5):
            print_h5_structure(h5)
        else:
            print "file %s not found"
