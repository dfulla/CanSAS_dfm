# -*- coding: utf-8 -*-

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

#SASroot
#  SASentry       
#    SASdata
#      @name=“D2O_100pc"
#      @Q_indices=1,2
#      @I_axes=“M,Q,Q”
#      @M_indices=0
#      I: float[2,128,128]
#      Qx: float[128,128]
#      Qy: float[128,128]
#      Qz: float[128,128]
#      M: float[2]

#example files:
#exp_files1 = ["D2O_100pc_2D_0.051kG.ABS","D2O_100pc_2D_15_5kG.ABS"]
#exp_files2 = ["H2O_100pc_2D_0.051kG.ABS","H2O_100pc_2D_15.5kG.ABS"]

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
		self.sasentry.create_dataset(title, (), data=title)

	#def createData(self, name, name_sample, qi, ii, m, mi=None, attributes=None):
        def createData(self, name, qi, ii, m, mi=None, attributes=None):
		self.sasdata = self.sasentry.create_group(name)
                #self.sasdata.attrs["name"] = name_sample
		self.sasdata.attrs["Q_indices"] = qi
		self.sasdata.attrs["I_axes"] = ii
                self.sasdata.attrs["M_indices"] = m
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
                                
                                
def get_magnetic_fields(exp_files):
        
    magnetic_field_files = []
    for sample in exp_files:
                magnetic_field =  sample.split('2D_')[1].split('kG.ABS')[0]
                if '_' in magnetic_field:
                        magnetic_field = magnetic_field.replace('_','.')
                magnetic_field_files.append(float(magnetic_field))
                
    return magnetic_field_files

def get_name_sample(exp_files):
    name_sample = []
    for i,sample in enumerate(exp_files):
        name_sample.append(sample.split('_2D')[0])
    
    if all(x == name_sample[0] for x in name_sample):
        return name_sample[0]
    else:    
        print name_sample      
        print 'Names of the two files are not coincident'

        
def get_columns(file_data):
  
    try:
      Qx, Qy, I, err_I, Qz, SigmaQ_parall, SigmaQ_perp, fSubS = np.loadtxt(file_data,unpack=True, skiprows = 19,dtype=[('Qx','<f8'),('Qy','<f8'),('I(Qx,Qy)','<f8'),('err(I)','<f8'),('Qz','<f8'),('SigmaQ_parall','<f8'),('SigmaQ_perp','<f8'),('fSubS(beam stop shadow)','<f8')])
      Qx = np.reshape(Qx,(128,128))
      Qy = np.reshape(Qy,(128,128))
      Qz = np.reshape(Qz,(128,128))
      I  = np.reshape(I ,(128,128))

      return Qx, Qy, I, err_I, Qz, SigmaQ_parall, SigmaQ_perp, fSubS

    except:
      print "Could not extract data columns from %s. Check that the heather has 19 rows"%file_data
   

class ConvertCansas(ExampleFile):
   def write(self, exp_files):

           print 'Files beeing read: %s'%str(exp_files)
           self.createFile() 
           self.createEntry("sasentry01")
           sample_name = get_name_sample(exp_files)
           #self.createTitle(sample_name)
           self.createData("sasdata01", [1,2], ["M", "Q", "Q"], [0,]) # without sample name
           #self.createData("sasdata01", sample_name, [1,2], ["M", "Q", "Q"], [0,])
           file_i = exp_files[0]
           Qx,Qy,Qz = get_columns(file_i)[0],get_columns(file_i)[1],get_columns(file_i)[4]
           M = np.array(get_magnetic_fields(exp_files))  
           I_2 =[]
           
           for i,sample in enumerate(exp_files):
                   I_2.append(get_columns(exp_files[i])[2])

           intensities_array = np.empty([2,128,128])
           intensities_array[0] = I_2[0]
           intensities_array[1] = I_2[1]
	   self.createDataSet("Qx", Qx, {"units": "1/A"})
	   self.createDataSet("Qy", Qy, {"units": "1/A"})
           self.createDataSet("Qz", Qz, {"units": "1/A"})
           self.createDataSet("M",  M,  {"units":  "kG"})
           self.createDataSet("I", intensities_array, {"units": "1/cm"})
	   self.closeFile()
        
def main(exp_files):
    name_sample = get_name_sample(exp_files)
    ConvertCansas("%s.hdf5"%name_sample).write(exp_files)
    if os.path.isfile("%s.hdf5"%name_sample):
            print 'File: %s.hdf5 created'%name_sample
            
if __name__ == "__main__":

    if len(sys.argv) == 1:

        print "Files available:"
        files_available = []
        
        for i,filenames in enumerate(os.listdir(os.getcwd())):    
            if filenames.endswith(".ABS"):
                files_available.append(filenames)
        if len(files_available) == 4:
                    print '%s %s'%(files_available[0],files_available[1])
                    print '%s %s'%(files_available[2],files_available[3])
        else:
                print files_available

        exp_files = raw_input('Choose two files to read (e.g. D2O_100pc_2D_0.051kG.ABS D2O_100pc_2D_15_5kG.ABS):\n')
        
        if exp_files.split(' ') > 1:
              try:  
                      print exp_files
                      file1 = exp_files.split(' ')[0]
                      file2 = exp_files.split(' ')[1]
                      exp_files = ['%s'%file1,'%s'%file2]
                      main(exp_files)
              except:
                      print 'Unable to process %s. Use the following structure: D2O_100pc_2D_0.051kG.ABS D2O_100pc_2D_15_5kG.ABS'%exp_files
                      
        else:
              print 'Unable to process %s. Use the following structure: D2O_100pc_2D_0.051kG.ABS D2O_100pc_2D_15_5kG.ABS'%exp_files

    if len(sys.argv) == 2:
            print 'Running an example with file combination D2O_100pc_2D_0.051kG.ABS D2O_100pc_2D_15_5kG.ABS'
            main(['D2O_100pc_2D_0.051kG.ABS','D2O_100pc_2D_15_5kG.ABS'])
        
    if len(sys.argv) == 3:
        exp_files = ['%s'%str(sys.argv[1]),'%s'%(str(sys.argv[2]))]
        if os.path.isfile(exp_files[0]) == True:
            if os.path.isfile(exp_files[1]) == True:
                main(exp_files)    
   
        else:
            print "Files not found"

      
