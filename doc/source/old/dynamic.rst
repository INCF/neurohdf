.. _dynamic:

Dynamic datasets
================

Two approaches to extend static datasets to the temporal domain:

 * Add another dimension to the dataset array, denoting time
 * Add super-node for different time steps where datasets are contained in

Both methods have advantages and disadvantages and fit different scenarios. But
they can also be combined.

..

    Dynamic datasets
    ----------------

    When the time evolution does not change the dimensionality of the dataset, add time as another dimension to
    the data array. If it does change, introduce scaffolding timepoint group nodes for each time step.
    For variably distanced time steps, it is up to the user/developer to store an property array with the
    time points vs. creating a timepoint scaffold for each timestep with the appropriate metadata information
    about the occurrences. In the scaffolding case, it is suggested to define an identity map between the dimensions
    adjoining the different time points, best with an increasing integer id. Mixing of both types of representation
    should be possible.

    Storing my regular grid of data points

    NeuroHDF node::

        Group <SpatioTemporalOrigo>: Metadata: rotation&scale + offset (identity)
            Group <Grid/regular>: Metadata: affine transformation
                Dataset <data>

                Group <timeslices>
                    Dataset <t0>
                    Dataset <t1>
                    ...

                or

                Group <slice_t0>
                    Dataset <data>
                Group <slice_t1>
                    Dataset <data>
                ....

    A distinction has to be made between the spatial datastructure that changes over time
    vs. the fields defined over the fixed spatial datastructures that change over time.
