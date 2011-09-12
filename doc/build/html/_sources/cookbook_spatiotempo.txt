.. _spatiotempo:

Cookbook - Spatio-Temporal datasets
===================================

This page introduces NeuroHDF convention for the hierarchical layout of spatio-temporal datasets (datasets
with underlying geometry) that are subnodes of a *Region*. The spatial coordinates are referenced relative
to the coordinate system defined by the region.

.. note::
   For metadata attributes, 0-indexed is the convention (Python convention), different from
   1-indexed based conventions (e.g. in Matlab).

Regular datasets
----------------

N-dimensional contiguous, homogeneous dataset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A data block with at least one spatial dimension. It may have temporal dimensions. There are usually
additional dimensions (trials, channels, subjects etc.). All information about the axes are stored
as metadata.


The affine represents the transformation from voxel space to the *Region* space.
If 3 spatial axes exist, it has shape (4,4) for translations, rotations, zooms, shears.
for 2 spatial axes, the affine has shape (3,3). The zooms define the spatial resolution.
Individual components `can be extracted <https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/affines.py>`_.

The *axes_info* refers to the output of the affine transformation. The spatial axes (kind: spatial)
should be aligned with the corresponding spatial axes of the *Region*. They should be be ordered, i.e.
the first spatial axes of the *Region* corresponds to the axis with index 1 in our case.

Open Questions:

* When rotation occurs in the affine transformation, the semantics of pre/post transformation could be changed.
  Otherwise, with only scaling and translation, they are expected to stay invariant.

NeuroHDF node::

    Group["My regular dataset"]

        Group["metadata"]
        .attrs["type"] = "XML" (or JSON, ...)
        .attrs["schemaNamespace"] : Schema XML namespace identifier
        .attrs["schemaLocation"] : URL to XSD file
            Dataset["data"] : byte array, shape (N,1) storing the XML document

        Dataset["data"] : nd array
        .attrs["affine"] : 2d array, shape (4,4) for 3 spatial axes
        .attrs["axes_info"] = {
            0 : {"name" : "t",
                 "unit" : {"name": "millisecond", "ref" : "http://purl.obolibrary.org/obo/UO_0000028"},
                 "sampling frequency" : 256,
                 "kind" : "temporal" },
            1 : {"name" : "x",
                 "unit" : {"name": "meter", "ref" : "http://purl.obolibrary.org/obo/UO_0000008"},
                 "kind" : "spatial" },
            2 : {"name" : "y",
                 "unit" : {"name": "meter", "ref" : "http://purl.obolibrary.org/obo/UO_0000008"},
                 "kind" : "spatial" },
            3 : {"name" : "z",
                 "unit" : {"name": "meter", "ref" : "http://purl.obolibrary.org/obo/UO_0000008"},
                 "kind" : "spatial" },
            4 : {"name" : "r",
                 "desc" : "Red channel measurement"},
            5 : {"name" : "g",
                 "desc" : "Green channel measurement"},
            6 : {"name" : "b",
                 "desc" : "Blue channel measurement"},
            7 : {"name" : "trial"}
        }


Irregular datasets
------------------

3D skeletons / microcircuitry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Examples:

* Cellular morphologies (skeletonized)
* Skeletonized reconstructions from electron microscopy, e.g. with `CATMAID <https://github.com/acardona/CATMAID>`_

NeuroHDF node::

    Group["3D Skeletons"]

        Group["vertices"]
            Dataset["data"] : array, shape (N,3) with spatial location
            .attrs["axes_info"] = {
                0 : {"name":"entities"},
                1 : {"name":"spatial location",
                     "label": {
                        0 : { "name" : "x", "unit" : {"name": "meter", "ref" : "http://purl.obolibrary.org/obo/UO_0000008"} },
                        1 : { "name" : "y", "unit" : {"name": "meter", "ref" : "http://purl.obolibrary.org/obo/UO_0000008"} },
                        2 : { "name" : "z", "unit" : {"name": "meter", "ref" : "http://purl.obolibrary.org/obo/UO_0000008"} },
                     } } }

            Group["properties"]
                Dataset["type"] array, shape (N,1)
                .attrs["value"] = {
                    1 : {"name" : "skeleton node"},
                    2 : {"name" : "connector node"}
                }

            Group["connectivity"]
                Dataset["data"] array, shape (M,2)
                -> stores the connectivity between vertices in 0-indexed (global topology) array
                .attrs["axes_info"] = {
                    0 : {"name":"entities"},
                    1 : {"name":"connections",
                         "label" : {
                            0 : {"name" : "from"},
                            1 : {"name" : "to"},
                         }
                        }
                }
                Group["properties"]
                    Dataset["type"] array, shape (M,1)
                    .attrs["value"] = {
                        1 : {"name" : "axonal arbor"},
                        2 : {"name" : "dendritic arbor"},
                        3 : {"name" : "cell body"},
                        4 : {"name" : "spine"},
                        5 : {"name" : "presynaptic to"},
                        6 : {"name" : "postsynaptic to"},
                    }
                    Dataset["id"] array, shape (M,1)


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
            .attrs["axes_info"] = {
                0 : {"name":"points"},
                1 : {"name":"spatial location",
                     "labels": {
                        0 : { "name" : "x", "unit" : {"name": "meter", "ref" : "http://purl.obolibrary.org/obo/UO_0000008"} },
                        1 : { "name" : "y", "unit" : {"name": "meter", "ref" : "http://purl.obolibrary.org/obo/UO_0000008"} },
                        2 : { "name" : "z", "unit" : {"name": "meter", "ref" : "http://purl.obolibrary.org/obo/UO_0000008"} },
                     } } }

            Group["properties"]
                Dataset["type"] : array, shape (N,1)
                .attrs["value"] = {
                    1 : {"name" : "axonal arbor"},
                    2 : {"name" : "dendritic arbor"},
                    3 : {"name" : "cell body"}
                }
                Dataset["id"] : array, shape (N,1)
                
            Group["connectivity"]
                Dataset["data"] : array, shape (M,3)
                -> global topology of triangular faces. find local topology by subtracting min()
                .attrs["axes_info"] = {
                    0 : {"name": "entities" },
                    1 : {"name": "triangular faces" }
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
