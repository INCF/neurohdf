Proposed Hierarchical Layout
============================
**Version 0.1**

A HDF5 file consist of a tree with group and dataset nodes. Each node can have attributes as key-value pairs.
Please refer to the `h5py documentation <>`_ for an introduction to the concepts and manipulation of HDF5 files.

In the following, we describe the way data is structured and laid-out as a NeuroHDF file using h5py. We make here
a proposal for a basic layout and core attributes, that can be customized.

First, we create a writable NeuroHDF file::

    import h5py
    myfile = h5py.File('firstfile.neurohdf')

Define global metadata pertaining to the purpose and content of the dataset::

    myfile.attrs["title"] = "A generic title"
    myfile.attrs["description"] = "A generic prose description of the content and purpose of the dataset"
    myfile.attrs["species"] = "The biological organism this dataset is representing in binomial form"
    myfile.attrs["creator"] = "The creator of the dataset including email"
    myfile.attrs["collaborators"] = "The collaborators related to the creation of the dataset"
    myfile.attrs["references"] = "Citation or URL reference for this dataset"

You need to be very clear about the type of data you want to store.

We represent the concept of a `3D spatial reference frame <>`_ in NeuroHDF as a *Region* HDF group node.

* *x*: first spatial direction
* *y*: second spatial direction
* *z*: third spatial direction

Each *Region* is spatially embedded with an affine transformation from its parent coordinate system to its coordinate system.
Because the root *Region* in the hierarchy has no parent *Region*, the parent coordinate system is defined by convention
as a Left-Hand-Coordinate system, where the first spatial direction is to the right (*x*), the second spatial direction
is upwards (*y*) and the third spatial direction is forward (*z*).

This means that the root *Region* node in the NeuroHDF hierarchy contains an affine transformation that might
reorder the convention root coordinate system.

Example: From NeuroHDF root-convention coordinate system "Right-Anterior-Superior" (RAS) coordinate systems.
In RAS coordinate systems, the meaning of the first spatial direction is "positive values go to the right",
second spatial direction is "positive values go forward", and third spatial direction is "positive values go upward".
"Superior" can also mean "Dorsal", for instance in humans when you look to the sky, but this must not be the case.
Thus, its is necessary the detach the meaning or interpretation of the three, ordered spatial axes, and define
what it means to move in positive or in negative direction of e.g. the first spatial direction etc. For instance,
moving to the right for positive values, moving to the left for negative values, such as in the RAS coordinate system
or in the root-convention coordinate system. We encode this fact as a 3-tuple (an ordered list with three elements) of 2-tuples
containing string elements. The first element of the 2-tuple denotes the positive direction, the second the negative.
For instance, in the RAS coordinate system, we encode the meaning of the spatial direction (axes)
as: ( ("Right","Left"), ("Anterior","Posterior"), ("Superior", "Inferior") )
This gives us a good understanding of what the direction within a given *Region* mean. Note that this semantics
applies to the coordinate axes AFTER the affine transformation from its parent coordinate system.
Similarly, for the root-convention coordinate system, the meaning of the axes are:
( ("Right","Left"), ("Upwards","Downwards"), ("Forwards", "Backwards") )

We need the Spatial Ontology IDs: http://obofoundry.org/cgi-bin/detail.cgi?id=spatial

The affine transformation not only specifies the orientation of the axes, but also the location of origo. This corresponds
to the translation (the translational part of the affine) of origo from the root-convention coordinate system to the *Region* origo.
Similarly, we want to denote the meaning of origo in the *Region* coordinate system. Often, particular neuroanatomical
landmarks are used to define the origo. They should optimally be very stable across individuals. For instance, in the Waxholm space,
origo is defined at "Bregma" which is the anatomical point on the skull at which the coronal suture is intersected perpendicularly
by the sagittal suture. (REF: http://en.wikipedia.org/wiki/Bregma)

Also find ontology term.

Furthermore, the metric unit for unity of each spatial direction is defined as a 3-tuple. For instance: ("mm", "mm", "mm")
The axes units are important to know the unit for the axis-aligned bounding box values. Later, each dataset defines
its own units for its object's spatial locations.

Alternatively, we use the ID of the unit ontology: "UO:0000016" instead of "mm"
http://www.obofoundry.org/cgi-bin/detail.cgi?id=unit

TODO: How does this relate to the the scaling within the affine?

An optional metadata field specifies an axis-aligned bounding box by two points, where the axes are aligned to the
axes of the *Region* coordinate system. This basically defines the maximal spatial extent of the *Region*, but it
is not guaranteed to be correct. As we will see, *Regions* can contain other Regions, but also datasets. These
datasets can change over time, thus changing in its spatial configuration over time. The bounding-box would then
either denote the maximum bounding box at the first time frame, or alternatively be the maximum bounding box
across all time frames.

Wrapped up as metadata attribute for the *Region* node::

    region = myfile.create_group("MyRegionName") # e.g. could be Waxholm-Space
    region.attrs["type"] = "Region"
    region.attrs["affine"] = np.array( [ [..], [..], [..], [0,0,0,1] ], dtype = np.float32 )
    region.attrs["AxesSemantics"] = ( ("Right","Left"), ("Anterior","Posterior"), ("Superior", "Inferior") )
    region.attrs["OrigoSemantics"] = "Bregma"
    region.attrs["AxesUnits"] = ("mm", "mm", "mm")
    region.attrs["AABB"] = np.array( [ [-10,-10,-10], [10,10,10] ], dtype = np.float32 )

A *Region* contains spatio-temporal datasets that are spatially transformed relative
to the local coordinate system defined by the *Region*. The datasets are either
Regular or Irregular:

FIGURE

Each dataset specifies an affine transformation from its embedding *Region*. The affine for Irregular
datasets is the identity when the dataset's spatial location of the vertices are already relative
to the *Region* coordinate system. In Regular datasets, the homogenous array can contain an arbitrary
number of dimensions, but it requires to have at least one spatial dimension to meaningfully be a child
of a *Region*. For the affine of a Regular dataset, only the spatial dimension of the array are relevant
for the embedding within the *Region*.

    dataset.attrs["axis_0"] = 0
    dataset.attrs["axis_1"] = 1
    dataset.attrs["axis_2"] = None

or "first_axis" and the 0-based index. (0-base is by convention. To index into the array in NumPy arrays,
this does not require a transformation. For MATLAB which is 1-base, the index needs to be incremented by one.)

Alternatively, define a convention for the axes names:
("x", "y", "time", None, "zspace", "xfrequency", ...)

Regular datasets are fields defined on a regular grid, e.g.
2D images or 3D volumes. Irregular datasets are fields defined on their vertices and/or
their connectivity. Dataset group nodes specify metadata attributes:

Irregular datasets
* The affine transformation local to the Region they are contained in, usually would be identity
* The unit strings for all axes after transformation
* An axis-aligned boundings box relative to the Region
The semantics of the field on the irregular spatio-temporal datastructure
is stored in the vertices/connectivity property node's metadata attributes.

Mapping to irregular datasets are defined for:
* 3D skeletons
* 2D contours embedded in 3D (e.g. slices)
* Microcircuitry: 3D skeletons together with M-to-N connectors with spatial location between skeletons
* Surface meshes
* Line strips (a special case of 3D skeletons, such as tractographies)

Regular datasets (Homogeneous nd-arrays)
* The affine transformation from "voxel" space to Region space ?
  (The scaling defines the resolution)
* The unit strings for all axes after transformation
* An axis-aligned boundings box relative to the Region
* The semantics of the axes (after or before transformation?)

A distinction has to be made between the spatial datastructure that changes over time
vs. the fields defined over the fixed spatial datastructures that change over time.

What is the data model and philosophy adopted for NeuroHDF?

Do you have ...

    ..data in some spatial reference frame (i.e. there exists a well-defined origo and coordinate system)?
        ..yes
            ..is the underlying spatial structure of the data regular (on a grid) or irregular (vertices/connectivity)?

            ..does one aspect of the data have temporal extension?
                ..yes
                ..no

        ..no
            ..does it have spatial structure?
                ..yes
                    Genetic Expression Profile
                ..no
                    ..do multiple timepoints exist for on aspect/does one aspect of the data have temporal extension?
                        ..yes
                            Dynamic Network/Graph
                        ..no
                            Static Network/Graph
