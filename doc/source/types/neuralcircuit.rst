.. _neuralcircuit:

Multi-compartment neural circuitry
==================================

The SWC format became the quasi-standard for the description of single neuronal
cell morphology reconstructions. For the description of larger neural circuits
with many neurons and their synaptic connectivity, a new and efficient data format
is needed. NeuroHDF describes a multi-compartmental neural circuit, similar to
SWC, with points in 3D space (vertices) and their connectivity. Attributes
like vertex (skeleton node, connector, root) or edge (presynaptic_to, postsynaptic_to)
type or radius are expressed as arrays corresponding to the vertices or edges.

You can use Hdfview to inspect an `example NeuroHDF file <https://github.com/NeuralEnsemble/libNeuroML/blob/master/hdf5Examples/neurohdf_microcircuit.hdf>`_. The software
tool CATMAID for neural circuit reconstruction exports microcircuits in this
format. Another emerging standard is `libNeuroML <https://github.com/NeuralEnsemble/libNeuroML>`_.

Useful for neuroscience data types
----------------------------------
* Single cell morphology
* Neural circuit reconstructions

Tool supporting this specification
----------------------------------

* `CATMAID <http://catmaid.org/>`_ exports neural circuit reconstructions in NeuroHDF

.. Example generation
   ------------------

.. raw:: html
