Cookbook - Generic datasets
===========================

A proposal for data structures that are not spatio-temporally mapped, such as networks, behavioral or simulation results
(:ref:`datatypes` for more).


Networks
--------

The basic structure is similar to a static irregular dataset with vertices and connectivity.

NeuroHDF node::

    Group["My Network"]

        Group["vertices"]

            Group["connectivity"]

                Group["properties"] : dataset's first dimension must be M
                    Dataset["labels"] -> could express link modularity
                    Dataset["weight"] -> express weight of the connection
                    Dataset["fromid"] -> if connectivity is expressed based on the node id, not index
                    Dataset["toid"] -> dito. alternatively, store connectivity between ids in data ?

                Dataset["data"] : array, shape (M,2) stores the connectivity between vertices 0-indexed
                .attrs["semantics"] = {
                    0 : {"name":"connection"},
                    1 : {"name":"topology",
                         "column" : {
                            0 : {"name":"from"},
                            1 : {"name":"to"},
                         },
                         "directed" : True
                        }
                }

            Group["properties"]:
                Dataset["labels"] -> Nx1 array of labels. could express modules (hierarchical) of the network
                Dataset["color"] -> e.g. node color

            Dataset["data"] -> stores the node id in Nx1 array


Alternatively, if the graph is dense, store the complete connectivity matrix similar to a regular dataset.

NeuroHDF node::

    Group["Connection Matrix"]

        Dataset["data"] -> array, shape (N,N) for connectivity matrix
        .attrs["axes_semantics"] = {
            0 : {"name" : "fromregion", },
            1 : {"name" : "toregion" }
        }

        Group["properties"]
            Dataset["id"] : array, shape (N,1) with node properties

