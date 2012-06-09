NeuroHDF documentation
======================

Neuroscientists need to manage and integrate data from anatomy, physiology, behavior and simulation data
on multiple spatial and temporal scales and across modalities, individuals and species. Large amounts of data with
complex data types are to be produced in the coming decades - and viable solutions for databasing, data sharing and
interoperability of software tools `are needed <http://incf.org/programs>`_.

"`Hierarchical Data Format (HDF5) <http://www.hdfgroup.org/HDF5/>`_ is a data model, library, and file format for storing and managing data.
It supports an unlimited variety of datatypes, and is designed for flexible and efficient I/O and for high volume and complex data."

NeuroHDF is an effort to combine the flexibility and efficiency of HDF5 for
neuroscience datasets through the specification of a simple layout for different
data types with minimal :ref:`metadata` metadata requirements.


+-----------------------+---------------------------------------------+
| .. image::            | :ref:`neuralcircuit`                        |
+-----------------------+---------------------------------------------+
| .. image:: waves.png  | :ref:`ndarray`                              |
+-----------------------+---------------------------------------------+
| .. image:: waves.png  | :ref:`multiscale`                           |
+-----------------------+---------------------------------------------+
| .. image:: peak.png   | :ref:`electrophysiology`                    |
+-----------------------+---------------------------------------------+
| .. image:: peak.png   | :ref:`surface`                              |
+-----------------------+---------------------------------------------+
| .. image:: peak.png   | :ref:`behavior`                             |
+-----------------------+---------------------------------------------+
| .. image:: peak.png   | :ref:`simulation`                           |
+-----------------------+---------------------------------------------+
| .. image:: peak.png   | :ref:`serialimages`                         |
+-----------------------+---------------------------------------------+

.. |                       | blubb                                       |

Contents:

.. toctree::
   :maxdepth: 1
   :glob:

   examples/*

   evaluatehdf
   references
   datatypes
   oldideas
