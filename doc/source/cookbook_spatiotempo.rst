.. _spatiotempo:

Cookbook - Spatio-Temporal datasets
===================================

This page introduces NeuroHDF convention for the hierarchical layout of spatio-temporal datasets (datasets
with underlying geometry) that can be an element of a *Region*. A description of the usage of HDF5 Groups
and Dataset nodes is given.

.. note::
   For metadata attributes, 0-indexed is the convention (Python convention).
   Matlab uses 1-indexed convention, so the indices need to be incremented by one in Matlab.

Regular datasets
----------------

N-dimensional contiguous, homogeneous dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A data block with at least one spatial dimension. It may have temporal dimensions. There are usually
additional dimensions (trials, channels, subjects etc.). All information about the axes are stored in
the JSON header.

Examples:

* Microscopy where measurement sensors are on a regular grid
* 2D pixel-based slices

The affine represents the transformation from voxel space to the *Region* space.
If 3 spatial axes exist, it has shape (4,4) for translations, rotations, zooms, shears.
for 2 spatial axes, it would be shape (3,3). The zooms define the spatial resolution.
Individual components `can be extracted <https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/affines.py>`_.

The *axes_semantics* refers to the output of the affine transformation. The spatial axes
should be aligned with the corresponding spatial axes of the *Region*.

Open Questions:

* When rotation occurs in the affine transformation, the semantics of pre/post transformation could be changed.
  Otherwise, with only scaling and translation, they are expected to stay invariant

NeuroHDF node::

    Group["Regular data block"]

        Dataset["data"] -> nd array
        .attrs["affine"] -> 2d array, shape (4,4) for 3 spatial axes
        .attrs["axes_semantics"] = {
            0 : {"name" : "t",
                 "unit" : {"name": "millisecond", "OBO" : "UO:0000028"},
                 "sampling frequency" : 256,
                 "kind" : "temporal" },
            1 : {"name" : "x",
                 "unit" : {"name": "meter", "OBO" : "UO:0000008"},
                 "kind" : "spatial" },
            2 : {"name" : "y",
                 "unit" : {"name": "meter", "OBO" : "UO:0000008"},
                 "kind" : "spatial" },
            3 : {"name" : "z",
                 "unit" : {"name": "meter", "OBO" : "UO:0000008"},
                 "kind" : "spatial" },
            4 : {"name" : "r",
                 "desc" : "Red channel measurement"},
            5 : {"name" : "g" },
            6 : {"name" : "b" },
            7 : {"name" : "trial" }
        }


Irregular datasets
------------------

3D skeletons / microcircuitry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Irregular spatial data, namely N vertices with spatial location, but no temporal data.
Properties such as label data exists on the vertices and connectivity.
We stack multiple skeletons (tree topologies) with N vertices with spatial location and M connections.

Examples:

* Cellular morphologies (skeletonized)
* Skeletonized reconstructions from electron microscopy, e.g. with `CATMAID <https://github.com/acardona/CATMAID>`_

Open Questions:

* Is the *spatial location* unit's defined after application of the affine transformation?
  Or are the axes semantics in this case refering to the array axes?

NeuroHDF node::

    Group["3D Skeletons"]

        Group["vertices"]
            Dataset["data"] : array, shape (N,3) with spatial location
            .attrs["affine"] : 2d array, shape (4,4)
            .attrs["axes_semantics"] = {
                0 : {"name":"entities"},
                1 : {"name":"spatial location",
                     "column": {
                        0 : { "name" : "x", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                        1 : { "name" : "y", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                        2 : { "name" : "z", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                     } } }

            Group["properties"]
                Dataset["type"] array, shape (N,1)
                .attrs["semantics"] = {
                    1 : {"name" : "skeleton node"},
                    2 : {"name" : "connector  node"}
                }

            Group["connectivity"]
                Dataset["data"] array, shape (M,2)
                -> stores the connectivity between vertices in 0-indexed (global topology) array
                .attrs["semantics"] = {
                    0 : {"name":"entities"},
                    1 : {"name":"connections",
                         "column" : {
                            0 : {"name" : "from"},
                            1 : {"name" : "to"},
                         },
                         "directed" : False
                        }
                }
                Group["properties"]
                    Dataset["type"] array, shape (M,1)
                    .attrs["semantics"] = {
                        1 : {"name" : "axonal arbor"},
                        2 : {"name" : "dendritic arbor"},
                        3 : {"name" : "cell body"},
                        4 : {"name" : "spine"},
                        5 : {"name" : "presynaptic to"},
                        6 : {"name" : "postsynaptic to"},
                    }
                    Dataset["id"] array, shape (M,1)


Example code to create the dataset node::

    import numpy as np
    import json
    import h5py
    myfile = h5py.File('ff.h5')

    dset = myfile.create_group("3D Skeletons")
    vert = dset.create_group("vertices")

    vert.create_dataset("data", data=np.random.random((10,3)))

    vert.create_group("properties")
    vert["properties"].create_dataset("labels", data=np.random.random_integers(1,3,(10,)))
    vert["properties"]["labels"].attrs["semantics"] = json.dumps({
        1 : {"name" : "axonal arbor"},
        2 : {"name" : "dendritic arbor"},
        3 : {"name" : "cell body"} })

    vert.create_group("grouping")
    vert["grouping"].create_dataset("index", data=np.array([[200,0,4],[300,5,9]]))

    con = vert.create_group("connectivity")
    con.create_dataset("data", data=np.array(range(10)))

    myfile.close()


.. ... with changing vertices location
.. ```````````````````````````````````
.. The vertices location changes over time, but not the number of vertices. The connectivity stays the same.

.. ... with changing vertices location and number
.. ``````````````````````````````````````````````
.. The number of vertices as well as the location changes over time. The connectivity has to be defined for each time frame as well.

.. ... with changing connectivity properties
.. `````````````````````````````````````````
.. The number of vertices and location is constant, the number of connections is constant, but the connectivity properties
.. change over time.

Set of 3D triangular surfaces
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NeuroHDF node::

    Group["3D Surfaces"]

        Group["vertices"]
            Dataset["data"] : array, shape (N,3) with spatial location
            .attrs["affine"] : 2d array, shape (4,4)
            .attrs["axes_semantics"] = {
                0 : {"name":"entities"},
                1 : {"name":"spatial location",
                     "column": {
                        0 : { "name" : "x", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                        1 : { "name" : "y", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                        2 : { "name" : "z", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                     } } }

            Group["properties"]
                Dataset["type"] : array, shape (N,1)
                .attrs["semantics"] = {
                    1 : {"name" : "axonal arbor"},
                    2 : {"name" : "dendritic arbor"},
                    3 : {"name" : "cell body"}
                }
                Dataset["id"] : array, shape (N,1)
                
            Group["connectivity"]
                Dataset["data"] : array, shape (M,3)
                -> global topology of triangular faces. find local topology by subtracting min()
                .attrs["semantics"] = {
                    0 : {"name": "entities" },
                    1 : {"name": "triangular faces", "directed" : False }
                }
                Group["properties"]
                    Dataset["type"] : array, shape (M,1)
                    Dataset["id"] : array, shape (M,1)

..
    Set of 2D contours embedded in 3D space
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    Open Questions:

    * Store 2D or 3D vertices?
    * If 3D, 3rd column would be the slice index (e.g. as int). the affine would transform to physical space
    * How to store connectivity? polygonlines vs. individual lines.
    * need to store contours with holes?
    * individual contours as group vs. set of contours making up a structure with id.


    Dynamic datasets
    ----------------

    When the time evolution does not change the dimensionality of the dataset, add time as another dimension to
    the data array. If it does change, introduce scaffolding timepoint group nodes for each time step.
    For variably distanced time steps, it is up to the user/developer to store an property array with the
    time points vs. creating a timepoint scaffold for each timestep with the appropriate metadata information
    about the occurrences. In the scaffolding case, it is suggested to define an identity map between the dimensions
    adjoining the different time points, best with an increasing integer id. Mixing of both types of representation
    should be possible.

    Storing my regular grid of data points

    NeuroHDF node::

        Group <SpatioTemporalOrigo>: Metadata: rotation&scale + offset (identity)
            Group <Grid/regular>: Metadata: affine transformation
                Dataset <data>

                Group <timeslices>
                    Dataset <t0>
                    Dataset <t1>
                    ...

                or

                Group <slice_t0>
                    Dataset <data>
                Group <slice_t1>
                    Dataset <data>
                ....

    A distinction has to be made between the spatial datastructure that changes over time
    vs. the fields defined over the fixed spatial datastructures that change over time.
