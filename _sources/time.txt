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


Group <SpatioTemporalOrigo>: Metadata: rotation&scale + offset (identity)
    Group <Grid/regular>: Metadata: affine transformation
        Dataset <data>
        
        Group <timeslices>
            Dataset <t0>
            Dataset <t1>
            ...

        Group <slice_t0>
            Dataset <data>
        Group <slice_t1>
            Dataset <data>
        ....

