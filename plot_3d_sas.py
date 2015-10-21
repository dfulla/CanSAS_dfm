from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import os

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
	plt.show()
    else:
	print "Cannot find the file %s"%file_content


if __name__ == '__main__':
        plot3d(file_content)
