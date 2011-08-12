.. NeuroHDF documentation master file, created by
   sphinx-quickstart on Sat May 21 18:17:36 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

NeuroHDF documentation
======================

`What if all neuroscientific datasets were stored in an HDF5 data container by a shared convention among
instrumentation manufacturers, software tool developers, and scientists?`

On the most basic level, measured and simulated data can be divided into the **sequence of recorded symbols** (usually
numbers in binary representation), and **metadata** - information about the structure of the binary data, and data
provenance such as instrumentation and simulation parameters (usually as strings). Almost all file formats basically
represent a variation on this theme, basically defining the layout of the binary data stream and a selection of
metadata attributes deemed relevant from a particular perspective or interest group.

When it comes to exchange of data, between scientists or software tools, a common practice is to use text files when
no importers/exporters/converters for the required file formats are available. For large datasets, this approach
is bound to fail and some sort of binary format that allows random access of the data is required. Furthermore,
all the metadata orginally available should be preserved.

Neuroscience has to manage and integrate data from anatomy, physiology, behavior and simulation data
on multiple spatial and temporal scales and across modalities, individuals and species. Large amounts of data are
to be produced in the coming decades - and a viable solution is to use prove approaches to deal with this data deluge.

The aim of NeuroHDF is **NOT** to create yet another file format. Its goal is to propose a convention of how to express
metadata for generic datasets, settle on a small set of metadata fields for a variety of application domains,
and provide a recommendation on how to hierarchically represent spatio-temporal datasets with an underlying geometry.

Contents:

.. toctree::
   :maxdepth: 1

   datatypes
   hierarchy
   region
   cookbook
   cookbookgeneric
   evaluatehdf
   references
   contact
