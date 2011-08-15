NeuroHDF documentation
======================

`"What if all neuroscientific datasets were stored in an HDF5 data container by a shared convention among
instrumentation manufacturers, software tool developers, and scientists?"`

Neuroscientists have to manage and integrate data from anatomy, physiology, behavior and simulation data
on multiple spatial and temporal scales and across modalities, individuals and species. Large amounts of data are
to be produced in the coming decades - and a viable solution is sought to deal with this data deluge.

On the most basic level, measured and simulated data can be divided into the **sequence of recorded symbols** (usually
numbers in binary representation), and **metadata** - information about the structure of the binary data, and data
provenance such as instrumentation and simulation parameters (usually as strings). Basically all file formats
represent a variation on this theme, defining the layout of the binary data stream and a selection of
metadata attributes deemed relevant for a particular application-domain or interest group.

When it comes to exchange of data, between scientists or software tools, a common practice is to use text files when
no importers/exporters/converters for the required file formats are available. For large datasets, this approach
is bound to fail and some sort of binary format that allows random access of the data is required. Furthermore,
all the metadata originally available should be preserved. In many domains, XML is increasingly used to define standards
for interoperability, but it suffers from the same problem for large datasets as text files.

The aim of NeuroHDF is **NOT** to create yet another file format. Its goals are

 * to provide a recommendation on how to hierarchically represent spatio-temporal datasets with an underlying
   regular or irregular geometry, and map them to a spatial reference system
 * to propose a convention on how to express metadata for generic datasets using JSON
 * to investigate options to combine already existing XML schemas into NeuroHDF
 * to settle on a small sets of metadata fields for a variety of application domains

Feel free to fork the `GitHub NeuroHDF repository <https://github.com/unidesigner/neurohdf>`_ to contribute.

Contents:

.. toctree::
   :maxdepth: 1

   datatypes
   hierarchy
   region
   cookbook_spatiotempo
   cookbook_generic
   evaluatehdf
   references
   contact
