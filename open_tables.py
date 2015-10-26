import tables
import os
import sys


# to develop:
# extract values of attributes



def print_h5_structure(h5):

    if os.path.isfile(h5):
        h5file = tables.open_file(h5, driver="H5FD_CORE")
        print h5file
        h5file.close()
    
    else:
        print "Could not locate file %s"%h5


def get_last_file():
    
    import subprocess
    last_file = subprocess.Popen(["ls","-ltr"], stdout = subprocess.PIPE)
    last_file = last_file.communicate()[0].split('\n')[-2].split(' ')[-1]
    if '.hdf5' in last_file:
        return last_file
    else:
        #print last_file
        return ''
    
        
if __name__ == '__main__':

    if len(sys.argv) == 1:

        print "Files available:"
        for i,filenames in enumerate(os.listdir(os.getcwd())):
            
            if filenames.endswith(".hdf5"):
                print filenames
            if filenames.endswith('.h5'):
                print filenames

        last_file = get_last_file()
        if '.hdf5' in last_file:
            print "Last file: %s. Press enter to read the structure"%last_file

        
        h5 = raw_input("Write file to read:")

        if h5 == '':
            
            last_file = get_last_file()
            print 'Printing structure of last modified hdf5: %s'%last_file
            print_h5_structure(last_file)
        
        if os.path.isfile(h5):
            print_h5_structure(h5)
        else:
            if h5 != '':
                print "file %s not found"%h5


            

            
    
    if len(sys.argv) == 2:
        h5 = sys.argv[1]
        if os.path.isfile(h5):
            print_h5_structure(h5)
        else:
            print "file %s not found"
