Cookbook - Generic datasets
===========================

A proposal for data structures that are not spatio-temporally mapped, such as networks,
behavioral or simulation results (:ref:`datatypes` for more).

Generic
-------

A generic dataset structure::

NeuroHDF node::

    Group["Generic dataset"]

        Group["metadata"]
        .attrs["type"] = "XML" (or JSON, ...)
        .attrs["schemaNamespace"] : Schema XML namespace identifier
        .attrs["schemaLocation"] : URL to XSD file
            Dataset["data"] : byte array, shape (N,1) storing the XML document

        Dataset["data"] : nd array data structure
         or
        Group["data"] : complex data structure


Networks
--------

The basic structure is similar to a static irregular dataset with vertices and connectivity.

NeuroHDF node::

    Group["My Network"]

        Group["vertices"]

            Dataset["data"] : array, shape (N,1) for node identifiers

            Group["properties"]:
                Dataset["group"] : array, shape (N,1) to group nodes of the network
                Dataset["color"] : array, shape (N,3) for node color in RGB

            Group["connectivity"]

                Dataset["data"] : array, shape (M,2) stores the connectivity between vertices 0-indexed
                .attrs["axes_info"] = {
                    0 : {"name":"connection"},
                    1 : {"name":"topology",
                         "label" : {
                            0 : {"name":"from"},
                            1 : {"name":"to"},
                         }
                        }
                }
                .attrs["metadata"] = {
                    "directed" : True
                }

                Group["properties"] :
                    Dataset["weight"] > array, shape (M,2) for the connection weigth

Alternatively, if the graph is dense, store the complete connectivity matrix similar to a regular dataset.

NeuroHDF node::

    Group["Connection Matrix"]

        Dataset["data"] -> array, shape (N,N) for connectivity matrix
        .attrs["axes_info"] = {
            0 : {"name" : "from region", },
            1 : {"name" : "to region" }
        }

        Group["properties"]
            Dataset["id"] : array, shape (N,1) with node identifiers

