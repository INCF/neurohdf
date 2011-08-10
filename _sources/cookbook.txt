Cookbook - Spatio-Temporal datasets
===================================

This page introduces NeuroHDF convention for the hierarchical layout of spatio-temporal datasets (datasets
with underlying geometry) that can be an element of a `Region`. A description of the usage of HDF5 Groups
and Dataset nodes is given.

.. note::
   For metadata attributes, 0-indexed is by convention. In Python to index into the NumPy arrays,
   the indices do not require a transformation. For MATLAB which is 1-indexed the indices need to be incremented by one.

Regular datasets
----------------

N-dimensional contiguous, homogeneous dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A data block with at least one spatial dimension. It may have temporal dimensions. There are usually
additional dimensions (trials, channels, subjects etc.).

Examples:

* Microscopy where measurement sensors are on a regular grid
* 2D pixel-based slices

Open Questions:

* The affine transformation from "voxel" space to Region space ?
  (The scaling defines the resolution)
* When rotation occurs in the affine transformation, the semantics of pre/post transformation could be changed.
  Otherwise, with only scaling and translation, they are expected to stay invariant

NeuroHDF node::

    Group["Regular data block"]

        Dataset["data"] -> nd array
        .attrs["affine"] -> 2d array, shape (4,4) because 3 spatial axes
        .attrs["axes_selector_spatial"] = {
            0 : "x",
            1 : "y",
            2 : "z",
        }
        .attrs["axes_selector_temporal"] = {
            0 : "t"
        }
        .attrs["axes_semantics"] = {
            0 : {"name" : "t", "unit" : {"name": "millisecond", "OBO" : "UO:0000028"}, "sampling frequency" : 256 },
            1 : {"name" : "x", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
            2 : {"name" : "y", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
            3 : {"name" : "z", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
            4 : {"name" : "r", "desc" : "Red channel measurement"  },
            5 : {"name" : "g" },
            6 : {"name" : "b" },
            7 : {"name" : "trial" }
        }



Irregular datasets
------------------

3D skeleton
^^^^^^^^^^^
Contains spatial data, namely N vertices with spatial location, but no temporal data.
Properties such as label data exists on the vertices and connectivity.
We stack multiple skeletons (tree topologies) with N vertices with spatial location and M connections.

Examples:

* cellular morphologies (skeletonized)

NeuroHDF node::

    Group["3D Skeletons"]

        Group["vertices"]
        .attrs["affine"] : affine transformation, transforming the vertex locations
        location?: in supergroup, or in dataset alternatively

            Group["connectivity"]

                Group["grouping"]
                    Dataset["index"]: SkeletonID | FromIndex | ToIndex

                Group["properties"] : dataset's first dimension must be M
                    Dataset["labels"]

                Dataset["data"] -> stores the connectivity between vertices in Mx2 array 0-indexed (global topology)
                .attrs["semantics"] = {
                    0 : {"name":"entities"},
                    1 : {"name":"connections",
                         "column" : {
                            0 : {"name":"from"},
                            1 : {"name":"to"},
                         },
                         "directed" : False
                        }
                }

            Group["grouping"]
                Dataset["index"]: SkeletonID | FromIndex | ToIndex
                Group["properties"]: child dataset's first dimension must be equal to the number of first dimension of the "index" dataset
                    Dataset["statistics"]: summary statistics for each skeleton
                    .attrs[""] -> named axes, named columns

            Group["properties"]: dataset's first dimension must be N
                Dataset["labels"] -> Nx1 array of labels. JSON-encoded metadata string encodes semantics
                .attrs["semantics"] = {
                    1 : {"name" : "axonal arbor"},
                    2 : {"name" : "dendritic arbor"},
                    3 : {"name" : "cell body"}
                }

            Dataset["data"] -> stores spatial location in Nx3 array
            .attrs["array_axes/dimension_semantics"] = {
                0 : {"name":"entities"},
                1 : {"name":"spatial location",
                     "column": {
                        0 : { "name" : "x", "unit" : ??/before and/or after transform? },
                        1 : { "name" : "y", "unit" : ?? },
                        2 : { "name" : "z", "unit" : ?? },
                     } } }

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
    vert["properties"]["labels"].attrs["semantics"] = json.dumps({1 : {"name" : "axonal arbor"}, 2 : {"name" : "dendritic arbor"}, 3 : {"name" : "cell body"} })

    vert.create_group("grouping")
    vert["grouping"].create_dataset("index", data=np.array([[200,0,4],[300,5,9]]))

    con = vert.create_group("connectivity")
    con.create_dataset("data", data=np.array(range(10)))

    myfile.close()

Example code to create 3D skeleton dataset node from a set of SWC files::

    ...code...

A helper function to extract a subarray based on a given id using the index dataset of a grouping::

    def extract_array( grouping_index, dataset, value ):
        idx = grouping_index.value
        residx = np.where(idx[:,0] == value)[0]
        if len(residx) == 0:
            print("Value ID not found in group_index")
            return
        elif len(residx) > 1:
            print("Multiple value IDs foud in group_index")
            return
        else:
            validx = residx[0]
        fromidx = idx[validx, 1]
        toidx = idx[validx, 2]
        return dataset[fromidx:(toidx+1),:]

... with changing vertices location
```````````````````````````````````
The vertices location changes over time, but not the number of vertices. The connectivity stays the same.

... with changing vertices location and number
``````````````````````````````````````````````
The number of vertices as well as the location changes over time. The connectivity has to be defined for each time frame as well.

... with changing connectivity properties
`````````````````````````````````````````
The number of vertices and location is constant, the number of connections is constant, but the connectivity properties
change over time.

Set of 3D triangular surfaces
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NeuroHDF node::

    Group["3D Surfaces"]

        Group["vertices"]
        .attrs["affine"] : affine transformation, transforming the vertex locations

            Group["connectivity"]
                Group["grouping"]
                    Dataset["index"]: StructureID | FromIndex | ToIndex
                Group["properties"] : dataset's first dimension must be M
                    Dataset["labels"]
                Dataset["data"] -> global topology of triangular faces. find local topology by subtracting min()
                .attrs["semantics"] = {
                    0 : {"name": "entities" },
                    1 : {"name": "triangular faces", "directed" : False }
                }

            Group["grouping"]
                Dataset["index"]: StructureID | FromIndex | ToIndex
                Group["properties"]
                    Dataset["statistics"]: summary statistics for each surface structure

            Group["properties"]: dataset's first dimension must be N
                Dataset["labels"]
                .attrs["semantics"] = {
                    1 : {"name" : "axonal arbor"},
                    2 : {"name" : "dendritic arbor"},
                    3 : {"name" : "cell body"}
                }

            Dataset["data"]
            .attrs["array_axes/dimension_semantics"] = {
                0 : {"name":"entities"},
                1 : {"name":"spatial location",
                     "column": {
                        0 : { "name" : "x", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                        1 : { "name" : "y", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                        2 : { "name" : "z", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                     } } }

Microcircuit
^^^^^^^^^^^^
Consisting of a set of 3D skeletons, connectors and connectivity between skeletons and connectors

Examples:

* Skeletonized reconstructions from electron microscopy, e.g. with `CATMAID <https://github.com/acardona/CATMAID>`_

NeuroHDF node::

    Group["Microcircuitry"]

        Group["vertices"]

            Group["connectivity"]
                Group["grouping"] -> include pre and post connectivity in skeleton!
                    Dataset["index"]: SkeletonID | FromIndex | ToIndex
                Group["properties"]
                    Dataset["type"]
                    .attrs = {
                        1 : "parent",
                        2 : "presynaptic",
                        3 : "postsynaptic"
                    }
                Dataset["data"] -> contains parent and connector relations

            Group["grouping"] -> not include connector vertices in skeleton!
                Dataset["index"]: SkeletonID | FromIndex | ToIndex

            Group["properties"]
                Dataset["type"]
                .attrs = {
                    1 : "skeleton vertex",
                    2 : "connector vertex"
                }
                Dataset["connectortype"]
                .attrs["semantics"] = {
                    1 : {"name" : "Glutamatergic"},
                    2 : {"name" : "GABAergic"}
                }
                Dataset["id"]

            Dataset["data"] -> similar to 3D skeleton


# Common data query: For a given skeleton (ID), show all incoming/outgoing connectors.

Set of 2D contours embedded in 3D space
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open Questions:

* Store 2D or 3D vertices?
* If 3D, 3rd column would be the slice index (e.g. as int). the affine would transform to physical space
* How to store connectivity? polygonlines vs. individual lines.
* need to store contours with holes?
* individual contours as group vs. set of contours making up a structure with id.

NeuroHDF node::

    Group["Contours"]

        Group["vertices"]
        .attrs["affine"] : affine transformation, transforming the vertex locations

            Group["connectivity"]
                Group["grouping"]
                    Dataset["index"]: ContourID | FromIndex | ToIndex | StructureID
                Group["properties"] : dataset's first dimension must be M
                    Dataset["labels"]
                Dataset["data"] -> global topology of varying-length polygonlines

                .attrs["semantics"] = {
                    0 : {"name":"entities"},
                    1 : {"name":"triangular faces","directed" : False
                        }
                }

            Group["grouping"]
                Dataset["index"]: StructureID | FromIndex | ToIndex
                Group["properties"]
                    Dataset["statistics"]: summary statistics for each surface structure

            Group["properties"]: dataset's first dimension must be N
                Dataset["labels"]
                 .attrs["semantics"] = "{1 : {"name" : "axonal arbor"}, 2 : {"name" : "dendritic arbor"}, 3 : {"name" : "cell body"} }"

            Dataset["data"]
            .attrs["array_axes/dimension_semantics"] = { 0 : {"name":"entities"},
                1 : {"name":"spatial location",
                     "column": {
                        0 : { "name" : "x", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                        1 : { "name" : "y", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                        2 : { "name" : "z", "unit" : {"name": "meter", "OBO" : "UO:0000008"} },
                     } } }

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
