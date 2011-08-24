Evaluation of HDF5
==================

Main HDF Group page
http://www.hdfgroup.org/

Supported Libraries
-------------------

Python libraries
^^^^^^^^^^^^^^^^
http://code.google.com/p/h5py/
http://www.pytables.org/moin

Java libraries
^^^^^^^^^^^^^^
http://www.ral.ucar.edu/~steves/nujan.html
https://wiki-bsse.ethz.ch/display/JHDF5

Matlab
^^^^^^
http://www.mathworks.com/help/techdoc/ref/hdf5.html

R bindings
^^^^^^^^^^
https://r-forge.r-project.org/projects/h5r/

.NET
^^^^
http://www.hdfgroup.org/projects/hdf.net/


Advantages of using HDF5
------------------------

* Compact binary data storage, extensible metadata
* Fast random and parallel access, efficient, scalable
* Widely used in High Performance Computing
* Open source and cross-platform
* `HDF5-Fast Query <http://vis.lbl.gov/Events/SC05/HDF5FastQuery/index.html>`_ and `paper <http://www.osti.gov/bridge/purl.cover.jsp?purl=/881620-2uP7So/>`_

Possible limitations of HDF5
----------------------------

* Difficulty to store variable-length string properties.
* Deleting a dataset does not free the space on disk. Requires rewriting the file.
* `Delete or update a dataset in HDF5? <http://stackoverflow.com/questions/447854/delete-or-update-a-dataset-in-hdf5>`_
* `Evaluating HDF5: What limitations/features does HDF5 provide for modelling data? <http://stackoverflow.com/questions/547195/evaluating-hdf5-what-limitations-features-does-hdf5-provide-for-modelling-data/547240#547240>`_
