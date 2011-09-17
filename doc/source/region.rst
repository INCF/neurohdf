.. _region:

The Region
----------

We represent the unifying concept of a 3D spatial reference frame in NeuroHDF as a *Region*. A Region is the container
for spatio-temporal datasets and is mapped to a HDF Group node with Region-based metadata.

NeuroHDF node for a Region::

    Group["My Region Name"]
    .attrs["type"] = "Region"

    Group["transform"] : specifies a complex transformation data type
    --or--
    .attrs["affine"] -> array, shape (4,4) for affine transformation matrix
    .attrs["origin_info"] = {
        "name" : "anterior commisure",
        "ref" : "UMLSCUI:C0152335"
    }
    .attrs["axes_info"] = {
        0 : { "positive" : {"name" : "right", "ref" : "http://purl.obolibrary.org/obo/BSPO_0000007"},
              "negative" : {"name" : "left", "ref" : "http://purl.obolibrary.org/obo/BSPO_0000000"}
            },
        1 : { "positive" : {"name" : "anterior", "ref" : "http://purl.obolibrary.org/obo/BSPO_0000055"},
              "negative" : {"name" : "posterior", "ref" : "http://purl.obolibrary.org/obo/BSPO_0000025"}
            },
        2 : { "positive" : {"name" : "dorsal", "ref" : "http://purl.obolibrary.org/obo/BSPO_0000063"},
              "negative" : {"name" : "ventral", "ref" : "http://purl.obolibrary.org/obo/BSPO_0000068"}
            }
    }
    .attrs["axes_units"] = {
        0 : {"name" : "x", "unit" : {"name": "mm", "ref" : "http://purl.obolibrary.org/obo/UO_0000016"} },
        1 : {"name" : "y", "unit" : {"name": "mm", "ref" : "http://purl.obolibrary.org/obo/UO_0000016"} },
        2 : {"name" : "z", "unit" : {"name": "mm", "ref" : "http://purl.obolibrary.org/obo/UO_0000016"} },
    }

    # now, the datasets ...

        Group["My regular dataset"] ...
        Group["3D Skeletons"] ...
        ...

A *Region* contains spatio-temporal datasets that are spatially transformed relative to the local coordinate system
defined by the *Region*.

The datasets are either regular or irregular:

.. image:: _static/region.png

We need to establish a basic convention for a global coordinate system, defining the axes order,
naming convention and orientation, to be able to interpret the affine transformation associated with each Region:

* first spatial direction, usually named *x*
* second spatial direction, usually named *y*
* third spatial direction, usually named *z*

Each Region is spatially embedded with an affine transformation from its parent coordinate system to its own (local)
coordinate system. Because the root Region in the hierarchy has no parent Region, the parent coordinate system is
defined by convention as a Left-Hand-Coordinate system, where the first spatial direction is to the right (x),
the second spatial direction is upwards (y) and the third spatial direction is forward (z). We call this global
coordinate system root coordinate system in the following.

The root Region node in the NeuroHDF hierarchy contains an affine transformation that might reorder
the convention root coordinate system. Note that the semantics given to the coordinate axes (their label) applied
to the coordinate axes AFTER the affine transformation from its parent coordinate system.

We use the `OBO Spatial Ontology <http://obofoundry.org/cgi-bin/detail.cgi?id=spatial>`_ as identifiers to complement
the human-readable string identifiers denoting axes interpretation.

The affine transformation not only specifies the orientation of the axes, but also the location of origin. This corresponds
to the translation (the translational part of the affine) of the origin from the root-convention coordinate system to the Region
origin. Similarly, we want to know the interpretation of the location of the origin in the Region coordinate system, such as
the anatomically identified
location in a template atlas. Often, particular neuroanatomical landmarks are used to define the origin. Optimally, they
should be very stable and recognizable across individuals. For instance, in the Waxholm space, origin is defined at
`Bregma <http://en.wikipedia.org/wiki/Bregm>`_
which is the anatomical point on the skull at which the coronal suture is intersected perpendicularly by the sagittal suture.

Furthermore, the metric unit for unity of each spatial direction is defined. We use the
`OBO Units of measurements Ontology <http://www.obofoundry.org/cgi-bin/detail.cgi?id=unit>`_
where "milimeter" is identified with "UO:0000016".

An optional metadata field specifies an axis-aligned bounding box by two points, where the axes are aligned to the
axes of the *Region* coordinate system. This basically defines the maximal spatial extent of the *Region*, but it
is not guaranteed to be correct. As we will see, *Regions* can contain other Regions, but also datasets. These
datasets can change over time, thus changing in its spatial configuration over time. The bounding-box would then
either denote the maximum bounding box at the first time frame, or alternatively be the maximum bounding box
across all time frames.

Individual components of the affine transformation `can be extracted <https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/affines.py>`_.

See section :ref:`spatiotempo`  for details on the dataset representation.