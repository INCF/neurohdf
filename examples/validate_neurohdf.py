#!/usr/bin/env python

"""
=====================
NeuroHDF Standard
=====================

A wide variety of large datasets in neuroscience can
be organized and managed using the Hierarchical Data Format HDF5.

NeuroHDF puts forward a data layout convention on how to flexibly store
these irregular and regular datasets.

"""

"""
We need to import NumPy and H5Py
"""

import numpy as np
import h5py
from contextlib import closing

"""
The validate_neurohdf function expresses the NeuroHDF specification
programatically.
"""

def validate_neurohdf( neurohdf ):

    if not 'neurohdf_version' in neurohdf.attrs:
        raise Execption("No 'neurohdf_version' attribute specified in root node")

    a,b = neurohdf.attrs['neurohdf_version'].split('.')
    if not(int(a) >= 0 and int(b) >= 0):
        raise Exception('NeuroHDF version %s can not be validated')

    for name,group in neurohdf.iteritems():
        if not 'node_type' in group.attrs:
            raise Exception("Missing 'node_type' attribute in group '{0}'".format(name))

        if group.attrs['node_type'] == 'regular_dataset':
            if not 'dataset' in group.keys():
                raise Exception("Missing 'dataset' for regular dataset group '{0}'".format(name))

            # TODO: what are the minimal, mandatory attributes for each axis?

        elif group.attrs['node_type'] == 'irregular_dataset':
            if not 'vertices' in group.keys():
                raise Exception("Missing 'vertices' group for irregular dataset group '{0}'".format(name))
            if not 'connectivity' in group.keys():
                raise Exception("Missing 'connectivity' group for irregular dataset group'{0}'".format(name))
            # First axis dimension must be equal for all contained datasets
            for value in ['vertices', 'connectivity']:
                N=[]
                for dataset_name, dataset in group[value].iteritems():
                    N.append( dataset.value.shape[0] )
                if not len(set(N)) == 1:
                    raise Exception("First axis dimension not equal all" + \
                    " datasets in '{0}' group for irregular dataset group '{1}'".format(value, name))

        else:
            raise Exception("Wrong 'node_type' for group '{0}'".format(name))

"""
NeuroHDF can be validated
"""

with closing(h5py.File('/tmp/test.hdf', 'r')) as neurohdf:
    validate_neurohdf( neurohdf )

"""
Creating a valid NeuroHDF
-------------------------
We now create a valid NeuroHDF containing a irregular and a regular dataset
"""

neurohdf = h5py.File('/tmp/test.hdf', 'w')
neurohdf.attrs['neurohdf_version'] = '0.1'

"""
An irregular dataset has two subgroups for the vertices and
their connectivity. Each subgroup contains datasets expressing
attributes on the vertices or on their topology. The first dimension
of the respective datasets has to match.
"""

tgroup = neurohdf.create_group('MyIrregularDataset')
tgroup.attrs['node_type'] = 'irregular_dataset'
vert = tgroup.create_group("vertices")
conn = tgroup.create_group("connectivity")
vert_id = vert.create_dataset('id', data=np.array( range(1,11), dtype = np.uint8) )
vert_location = vert.create_dataset('location', data=np.random.rand( 10, 3 ) )
conn_edge = conn.create_dataset('edge', data=np.random.random_integers(1,10, (5,2) ) )
conn_id = conn.create_dataset('id', data=np.array( range(1,6), dtype = np.uint8) )

"""
A regular dataset is a pure N dimensional homogeneous array.
Metadata attributes specify information on the axes. The metadata
subgroup stores for instance axes-related metadata.
"""

rgroup = neurohdf.create_group('RegularDataset')
rgroup.attrs['node_type'] = 'regular_dataset'

# Metadata group to store e.g. axes arrays
meta = rgroup.create_group("metadata")
meta.create_dataset("sectionindex", data=np.array([5,6,7,9,10],dtype=np.uint8) )

data = rgroup.create_dataset("dataset", data=np.random.rand( 2, 5, 5, 5, 3 ) )

data.attrs['axis0__label'] = 'time'
data.attrs['axis0__desc'] = 'The first axis represent the temporal evolution'
data.attrs['axis0__unit_label'] = 'miliseconds'
data.attrs['axis0__unit_xref'] = 'PURL:UO:0000028'
data.attrs['axis0__interval'] = 0.125 # a regular spacing between elements

data.attrs['axis1__label'] = 'x axis'
data.attrs['axis1__unit_label'] = 'meter'
data.attrs['axis1__unit_xref'] = 'UO:0000008'
data.attrs['axis1__interval'] = 1.0

data.attrs['axis2__label'] = 'y axis'
data.attrs['axis2__unit_label'] = 'meter'
data.attrs['axis2__unit_xref'] = 'UO:0000008'
data.attrs['axis2__interval'] = 1.0

data.attrs['axis3__label'] = 'z axis'
data.attrs['axis3__unit_label'] = 'meter'
data.attrs['axis3__unit_xref'] = 'UO:0000008'

"""
We can also store a label for each axes index using a reference to a
dataset stored in the metadata subgroup.
"""

# data.attrs['axis3__element_array'] = REF['/metadata/sectionindex']

data.attrs['axis4__label'] = 'channel'
data.attrs['axis4__desc'] = 'E.g. the image consist of RGB channels'
data.attrs['axis4__unit_label'] = 'categorial' # ?

neurohdf.close()


"""
Application to neuroscience datasets
------------------------------------

A example gallery for storage of a variety of neuroscientific datatypes in
NeuroHDF.
"""

"""
Single neuron morphology as skeleton, i.e. as a tree embedded in 3d space.
This datatype can be represented as an irregular dataset with
properties on the vertices and connectivity, similar to the SWC standard.
"""

neurohdf = h5py.File('/tmp/test.hdf', 'w')
neurohdf.attrs['neurohdf_version'] = '0.1'

mcgroup = neurohdf.create_group("Single Neuron Morphology")
vert = mcgroup.create_group("vertices")
conn = mcgroup.create_group("connectivity")

vert.create_dataset("id", data=np.array( [100,200,300], dtype = np.uint8) )
vert.create_dataset("location", data=np.random.rand( 3, 3 ).astype(np.float32) )
vert_type=vert.create_dataset("type", data=np.array( [1,2,3], dtype = np.uint8) )
vert_type.attrs['value'] = np.array([
    ['1', 'skeleton'],
    ['2', 'skeleton root'],
    ['3', 'connector']
    ])

vert.create_dataset("confidence", data=np.array( [5,5,5], dtype = np.uint8))
vert_radius=vert.create_dataset("radius", data=np.array( [5,4,2], dtype = np.float32))
vert_radius.attrs['unit_label'] = 'um'
vert_radius.attrs['unit_xref'] = 'PURL:...' # reference to ontology for um concept

conn.create_dataset("id", data=np.array( [11,12,13], dtype = np.uint8) )
conn_type=conn.create_dataset("type", data=np.array( [1,2,3], dtype = np.uint8))
conn_type.attrs['value'] = np.array([
    ['1', 'neurite'],
    ['2', 'presynaptic'],
    ['3', 'postsynaptic']
    ])
# other values could be: axonal arbor, dendrite, spine neck, spine head, cell body
neurohdf.close()

"""
A neural circuit skeletonization contains synaptic connectors
and stacked single neuron morphologies. The grouping into neurons
is achieved using an integer property skeletonid on the connectivity.
Similarly, neurons can be grouped as belonging to particular regions.
"""

# TBD (To Be Designed)

"""
Reconstructed neuron morphologies represented as a triangular surface mesh.
Again, an irregular dataset suits our needs.
"""

neurohdf = h5py.File('/tmp/test.hdf', 'w')
neurohdf.attrs['neurohdf_version'] = '0.1'

mcgroup = neurohdf.create_group("Neuron Surface Morphology")
vert = mcgroup.create_group("vertices")
conn = mcgroup.create_group("connectivity")

vert.create_dataset("id", data=np.array( [100,200,300], dtype = np.uint8) )
vert.create_dataset("location", data=np.random.rand( 3, 3 ).astype(np.float32) )

conn.create_dataset("id", data=np.array( [11], dtype = np.uint8) )
conn.create_dataset("faces", data=np.array([[0,1,2]], dtype = np.uint8) )

neurohdf.close()

"""
Raw images stacks from microscopy are usually 3,4 or 5 dimensional
(time, x, y, z, channel). Segmentation of these images can be stored
as regular datasets with integer values. See the example for regular
datasets above.
"""

# TBD

"""
Physiological recordings are (multichannel) timeseries and can be
stored in a regular dataset.
"""

# TBD

"""
A simulation result of a multi-compartmental model consist of
morphology and simulated physiology.
"""

# TBD

"""
One can imagine a variety behavioral datasets that can be stored
using regular datasets.
"""

# TBD