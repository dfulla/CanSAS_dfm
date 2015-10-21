import numpy as np
import h5py
import os
import sys
import inspect
import traceback
import time


'''
Reads and extracts data from one reduced experimental SAXS file (e.g.H2O_100pc_2D_0.051kG.ABS). 
Creates a new hdf5 file with CanSAS format (H2O_100pc_2D_0.051kG.ABS.hdf5).   
Writes the information from the experimental file to the hdf5-CanSAS format file.

CanSAS format described in:
http://www.cansas.org/formats/canSAS2012/1.0/doc/framework.html
http://www.cansas.org/formats/canSAS2012/1.0/doc/examples.html


'''

### UNDER DEVELOPMENT ###

# lacking:
# Magnetic field
# renaming
# efficiency
# correct I
# make I_axes and Q_indices dynamic
# generalize sasdata01...



#exp_files = ["D2O_100pc_2D_0.051kG.ABS","D2O_100pc_2D_15_5kG.ABS"]
exp_files = ["H2O_100pc_2D_0.051kG.ABS","H2O_100pc_2D_15.5kG.ABS"]

file_to_convert = exp_files[1]

FILE_TIMESTAMP = time.strftime("%Y-%m-%dT%H:%M:%S")
FILE_TIMESTAMP += '%+03d%02d' % (-time.timezone/60/60, abs(time.timezone/60) % 60)
FILE_PRODUCER = "canSAS"

class ExampleFile:

	def __init__(self, name, **keywords):
		self.name = name
		self.keywords = keywords

	def createFile(self):
		self.f = h5py.File(self.name, "w")
		self.f.attrs['file_name'] = self.name
		self.f.attrs['file_time'] = FILE_TIMESTAMP
		self.f.attrs['producer'] = FILE_PRODUCER

	def closeFile(self):
		self.f.close()

	def createEntry(self, name):
		self.sasentry = self.f.create_group(name)
		self.sasentry.attrs["NX_class"] = "SASentry"
		self.sasentry.attrs["version"] = "1.0"
	
	def createTitle(self, title):
		self.sasentry.create_dataset('Title', (), data=title)
	
	def createData(self, name, qi, ii, mi=None, attributes=None):
		self.sasdata = self.sasentry.create_group(name)
		self.sasdata.attrs["NX_class"] = "SASdata"
		self.sasdata.attrs["Q_indices"] = qi
		self.sasdata.attrs["I_axes"] = ii
		if mi != None:
			self.sasdata.attrs["Mask_indices"] = mi
		if attributes != None:
			for key in attributes.keys():
				self.sasdata.attrs[key] = attributes[key]

	def createDataSet(self, name, array, attributes=None):
		ds = self.sasdata.create_dataset(name, array.shape, data=array)
		if attributes != None:
			for key in attributes.keys():
				ds.attrs[key] = attributes[key]

# is this function being used?
def file_read(exp_file = file_to_convert):
    file_open = (open(exp_file).readlines())
    return exp_file,file_open


def get_magnetic_fields(exp_files):
        #shall it do it automatically?
        for sample in exp_files:
                magnetic_field =  sample.split('2D_')[1].split('kG.ABS')[0]
                if '_' in magnetic_field:
                        magnetic_field = magnetic_field.replace('_','.')
                
        magnetic_fields = [0.051,15.5] # from files

get_magnetic_fields(exp_files)
        
        
def get_columns(file_content = ""):
  
    try:
      Qx, Qy, I, err_I, Qz, SigmaQ_parall, SigmaQ_perp, fSubS = np.loadtxt(file_content,unpack=True, skiprows = 19,dtype=[('Qx','<f8'),('Qy','<f8'),('I(Qx,Qy)','<f8'),('err(I)','<f8'),('Qz','<f8'),('SigmaQ_parall','<f8'),('SigmaQ_perp','<f8'),('fSubS(beam stop shadow)','<f8')])
      Qx = np.reshape(Qx,(128,128))
      Qy = np.reshape(Qy,(128,128))
      I  = np.reshape(I ,(128,128))

      return Qx, Qy, I, err_I, Qz, SigmaQ_parall, SigmaQ_perp, fSubS

    except:
      print "Could not extract data columns from %s. Check that the heather has 19 rows"%file_content
   
def createFile(self):
    self.f = h5py.File(self.name, "w")
    self.f.attrs['file_name'] = self.name
    self.f.attrs['file_time'] = FILE_TIMESTAMP
    self.f.attrs['producer'] = FILE_PRODUCER


class ConvertCansas(ExampleFile):
   def write(self, exp_files = ["D2O_100pc_2D_0.051kG.ABS","D2O_100pc_2D_15_5kG.ABS"]):
	   self.createFile()
       
           for i,files in enumerate(exp_files):
               
                   self.createEntry("sasentry0%i"%(i+1))
	           self.createData("sasdata01","0,1,2" ,"nMAgnetic, Q, Q")
	           file_i = file_to_convert
                   Qx,Qy,I = get_columns(file_i)[0],get_columns(file_i)[1],get_columns(file_i)[2]
	           self.createDataSet("Qx", Qx, {"units": "1/A"})
	           self.createDataSet("Qy", Qy, {"units": "1/A"})
	           self.createDataSet("I", I, {"units": "1/cm"})
	   self.closeFile()
    
def main(exp_file = file_to_convert):
    ConvertCansas("%s.hdf5"%file_to_convert).write()

if __name__ == "__main__":

    main()
        

      
