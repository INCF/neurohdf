NeuroHDF documentation
======================

Neuroscientists need to manage and integrate data from anatomy, physiology, behavior and simulation data
on multiple spatial and temporal scales and across modalities, individuals and species. Large amounts of data with
complex data types are to be produced in the coming decades - and viable solutions for databasing, data sharing and
interoperability of software tools `are needed <http://incf.org/programs>`_.

"`Hierarchical Data Format (HDF5) <http://www.hdfgroup.org/HDF5/>`_ is a data model, library, and file format for storing and managing data.
It supports an unlimited variety of datatypes, and is designed for flexible and efficient I/O and for high volume and complex data."

NeuroHDF is an effort to combine the flexibility and efficiency of HDF5 for
neuroscience datasets through a simple object model of regular and irregular
datasets. Whenever data comes in array form, storage and I/O using HDF5 is
very efficient. But this is usually not enough to capture the rich semantic
metadata about datasets. Several approaches for metadata representation are
developed in different communities usually based on XML or databases
(relational, graph-based, document-based, key/value stores, triple stores).
Developing these domain-specific object models can be decoupled from the
pure data array storage using references.




Contents:

.. toctree::
   :maxdepth: 2
   :glob:

   examples/*

   evaluatehdf
   references
   datatypes
   oldideas
