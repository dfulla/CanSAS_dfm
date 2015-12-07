from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

exp_files = ["D2O_100pc_2D_0.051kG.ABS","D2O_100pc_2D_15_5kG.ABS","H2O_100pc_2D_0.051kG.ABS","H2O_100pc_2D_15.5kG.ABS"]
file_content = exp_files[3]

def plot3d(file_content):

    if os.path.isfile(file_content):

	Qx, Qy, I = np.loadtxt(file_content,unpack=True, skiprows = 19,dtype=[('Qx','<f8'),('Qy','<f8'),('I(Qx,Qy)','<f8')])
	fig = plt.figure()
	ax = fig.gca(projection = '3d')
	ax.set_xlabel("Qx")
	ax.set_ylabel("Qy")
	ax.set_zlabel("I")
	ax.plot_trisurf(Qx,Qy,I,cmap=cm.jet,linewidth=0.2)
        print type(Qx)
        print type(Qy)
        print type(I)
        print Qx.shape
        print Qy.shape
        print I.shape
	plt.show()
    else:
	print "Cannot find the file %s"%file_content

def plot3d_from_array(axis_x,axis_y,I_file1,I_file2):

    fig = plt.figure(figsize =(20,10))
    plt.figsize = (12,5)
    ax = fig.add_subplot(1,2,1, projection = '3d')
    ax.set_xlabel("Qx")
    ax.set_ylabel("Qy")
    ax.set_zlabel("I(Qx,Qy)")
    ax.plot_trisurf(axis_x,axis_y,I_file1, cmap=cm.jet,linewidth=0.2)
    ay = fig.add_subplot(1,2,2, projection = '3d')
    ay.set_xlabel("Qx")
    ay.set_ylabel("Qy")
    ay.set_zlabel("I(Qx,Qy)")
    ay.plot_trisurf(axis_x,axis_y,I_file2, cmap=cm.jet,linewidth=0.2)
    plt.show()

def plot2d_from_array(axis_x, axis_y):
    plt.plot(axis_x,axis_y)
    plt.show()

def plot1d_from_array(axis_y):
    plt.plot(axis_y)
    plt.show()

def accumulative_plot(list_of_arrays_to_plot):
    for i, array in enumerate(list_of_arrays_to_plot):
        plt.plot(array)
    print '%i curves'%(i+1)
    plt.show()
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print 'plotting...wait 0.5 min...'
        
        plot3d(file_content)
        #plot2d_from_array([1,2,4,3],[2,3,4,5])
        #plot1d_from_array([1,2,4,3])
        
    print len(sys.argv)
