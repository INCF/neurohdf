.. _metadata:

Metadata
========

The topic of storing complex metadata associated with the binary data is
involved, and a variety of proposals have been made based on XML or databases.

In the current proposal for NeuroHDF, we refrain from these metadata issues,
and propose to include only a minimal set of metadata fields such as axes
labels and units in a NeuroHDF file.

The development of domain-specific object models can be decoupled from the,
storage of binary data arrays. Such object models can be implemented as an
XML specification or a database schema, and references to data arrays, stored
e.g. in a NeuroHDF file on the file system, can be applied. With this
separation of concerns, individual research communities can come up with
a shared object model of their domain, and standardize formats for data exchange.

By using HDF5 with the NeuroHDF convention as standard format to store
array data, various research task such as large data storage and fast access
for analysis, visualization, modeling or simulation are simplified
through the existence of I/O libraries in all major programming languages
and platforms. Researchers could select the best tool for the task at hand
existing in any software environment.