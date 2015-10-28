import plot_3d_sas as p
import open_h5 as oh
import numpy as np
import matplotlib.pyplot as plt


dict = oh.main('D2O_100pc.hdf5')

x_data = dict.get('entry01')
x = np.reshape(x_data.get('Qx'),16384,)
y = np.reshape(x_data.get('Qy'),16384,)
z = x_data.get('I_array')
I_file1 = np.reshape(z[0],16384,)
I_file2 = np.reshape(z[1],16384,)

p.plot3d_from_array(x,y,I_file1,I_file2)

