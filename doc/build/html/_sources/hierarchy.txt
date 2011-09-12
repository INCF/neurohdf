Hierarchical Layout: Global Metadata
====================================

A HDF5 file consist of a tree with group and dataset nodes. Each node can have attributes as key-value pairs.
Please refer to the `h5py documentation <http://code.google.com/p/h5py/>`_ for an introduction to the concepts
and manipulation of HDF5 files.

In the following, we describe the way data is structured and laid-out as a NeuroHDF file using h5py. We make here
a proposal for a basic layout and core attributes, that can be customized.

First, we create a writable NeuroHDF file::

    import h5py
    myfile = h5py.File('firstfile.neurohdf')

We need to ensure that the NeuroHDF can be validated in some well-defined sense.
Therefore, we include metadata as XML instances derived from an XML schema, stored
as one-dimensional byte arrays.

We define a metadata subgroup from the Root node::

    Group["/"]

        Group["metadata"]
        .attrs["type"] = "XML" (or JSON, ...)
        .attrs["schemaNamespace"] : Schema XML namespace identifier
        .attrs["schemaLocation"] : URL to XSD file
            Dataset["data"] : byte array, shape (N,1) storing the XML document

For instance, we use the `Dublin Core Metadata Element <http://dublincore.org/documents/dces/>`_.
The `Datadryad project <http://datadryad.org>`_ is uses this convention for
metadata annotation.

In NeuroHDF, two classes of datasets are defined: a) spatio-temporal datasets
mapped to a spatial reference system, and b) generic datasets with data schema as metadata.

Whenever referencing `Open Biological and Biomedical Ontologies <http://obofoundry.org/>`_
terms, we use the `standardized PURL URI <http://www.obofoundry.org/id-policy.shtml>`_ to refer to concepts.

We first discuss the :ref:`region`, which is the unifying reference system for spatio-temporal datasets.