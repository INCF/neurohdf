Nifti1 image volume to NeuroHDF regular dataset
-----------------------------------------------

Use Python library: Nibabel::

    import nibabel
    import h5py

    a = nibabel.load('myfile.nii.gz')
    hf = h5py.File('/tmp/test.neurohdf')

    def create_neurohdf_group( h5file, regionpath, name, type = 'regular' ):
        gr = h5file[regionpath].create_group( name )
        gr.attrs['type'] = "RegularDataset"
        return gr

    regulargroup = create_neurohdf_group(hf, "/Region1", "MyFile")

    regulargroup.create_dataset( "data", data=niftifile.get_data() )
    hdr = niftifile.get_header()
    for k,v in hdr.items():
        h5file.attrs["nifti1_" + k] = v

    h5file.attrs['nifti1_affine'] = niftifile.get_affine()
    h5file.attrs['affine'] = niftifile.get_affine()


Tractographies to NeuroHDF irregular dataset
--------------------------------------------

.. Comment: It is expensive to store full connectivity for polyline strips