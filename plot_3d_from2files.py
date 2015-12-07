import plot_3d_sas as p
import open_h5 as oh
import numpy as np
import matplotlib.pyplot as plt
import sys


def plot_3d_2datasets(h5File):


    dict = oh.main(h5File)

    x_data = dict.get('entry01')
    x = np.reshape(x_data.get('Qx'),16384,)
    y = np.reshape(x_data.get('Qy'),16384,)
    z = x_data.get('I')
    I_file1 = np.reshape(z[0],16384,)
    I_file2 = np.reshape(z[1],16384,)
    
    p.plot3d_from_array(x,y,I_file1,I_file2)




if __name__ == '__main__':

    if len(sys.argv) == 1:
        #plot_3d_2datasets('D2O_100pc.hdf5')
        plot_3d_2datasets('D2O_100pc_two_entries.hdf5')
    if len(sys.argv) == 2:
        if sys.argv[1].find('.h5') != -1 or sys.argv[1].find('.hdf5') != -1:
            plot_3d_2datasets(sys.argv[1])
        else:
            print 'Non valid file extention (%s). Should be .h5 or .hdf5'%sys.argv[1]


        
