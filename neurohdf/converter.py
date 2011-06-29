import numpy

import nibabel
import h5py

def test_nifti_to_neurohdf():
    a = nibabel.load('/home/stephan/dev/LTS5/cffdata/Volumes/sample.nii.gz')
    hf = h5py.File('/tmp/test.neurohdf')
    nifti_to_neurohdf(hf, a, 'test')
    
def nifti_to_neurohdf(h5file, niftifile, name):
    """ Add Nifti file to NeuroHDF container

    Parameters
    ----------
    h5file : file-pointer
    niftifile : Nifti file
    name : str
        Name of the dataset node in the NeuroHDF file

    """
    h5file.create_dataset(name, data=niftifile.get_data())
    hdr = niftifile.get_header()
    for k,v in hdr.items():
        h5file.attrs[k] = v
    h5file.attrs['affine'] = niftifile.get_affine()
