.. _metadata:

Metadata
========

..  Whenever data comes in array form, storage and I/O using HDF5 is
    very efficient. But this is usually not enough to capture the rich semantic
    metadata about datasets. Several approaches for metadata representation are
    developed in different communities usually based on XML or databases
    (relational, graph-based, document-based, key/value stores, triple stores).
    Developing these domain-specific object models can be decoupled from the
    pure data array storage using references.
