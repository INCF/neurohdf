.. _ndarray:

N-dimensional, homogeneous arrays
=================================

By using a simple convention to describe metadata about the array axes,
basic information is available to make sensible interpretation of the array's
content.

Useful for neuroscience data types
----------------------------------

* Electron microscopy: 3D array, 3 spatial dimension after alignment
* Optical microscopy: 4D array, 3 spatial dimension and 1 channel dimension
* Labeling
* Functional MRI/PET: 4D array, with 3 spatial and 1 temporal dimension
* Structural MRI: 3D array, with 3 spatial dimensions
* Diffusion MRI: 4D array, with 3 spatial dimension and 1 dimension for gradient directions
  Contain metadata tables for b-values and b-vectors

Tool supporting this specification
----------------------------------

None so far. A `zebra fish dataset <http://vibez.informatik.uni-freiburg.de/>`_ available
as HDF5 files uses a similar specification for axes units.

Example generation
------------------

.. raw:: html

   <script src="https://gist.github.com/3006152.js"> </script>
