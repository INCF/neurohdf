NeuroHDF documentation
======================

Neuroscientists need to manage and integrate data from anatomy, physiology, behavior and simulation data
on multiple spatial and temporal scales and across modalities, individuals and species. Large amounts of data with
complex data types are to be produced in the coming decades - and viable solutions for databasing, data sharing and
interoperability of software tools `are needed <http://incf.org/programs>`_.

"`Hierarchical Data Format (HDF5) <http://www.hdfgroup.org/HDF5/>`_ is a data model, library, and file format for storing and managing data.
It supports an unlimited variety of datatypes, and is designed for flexible and efficient I/O and for high volume and complex data."

NeuroHDF is an effort to combine the flexibility and efficiency of HDF5 for neuroscience data and metadata storage
and management. It is **not** yet another file format. In particular, the aims are to:

 * provide a recommendation on how to hierarchically represent spatio-temporal datasets with an underlying
   regular or irregular geometry, map them to a spatial reference system and define metadata
 * integrate existing domain-specific XML schemas with HDF5
 * propose a convention on how to express array metadata using `JSON <http://www.json.org/>`_ and
   identifiers from `Open Biological and Biomedical Ontologies <http://obofoundry.org/>`_
 * define an API for at least Python, Matlab and Java languages

See homepage for more information: http://www.neurohdf.org/