Cookbook
========

We explain the data layout convention for several dataset use cases.

1. 3D skeleton (e.g. neuronal morphology)
-----------------------------------------
Spatial: Yes, N vertices with spatial location
Temporal: No
Generic: Label data on the vertices and connectivity

We stack multiple skeletons (tree topologies) where N vertices have a spatial location with M connections.

    Group["3D Skeletons"]

        Group["vertices"]

            Group["connectivity"]
                Group["properties"]: dataset's first dimension must be M
                    Dataset["labels"]
                Group["grouping"]
                    Dataset["index"]: SkeletonID | FromIndex | ToIndex
                Dataset["data"] -> stores the connectivity between vertices in Mx2 array 0-indexed (global topology)

            Group["grouping"]
                Dataset["index"]: SkeletonID | FromIndex | ToIndex
                Group["properties"]: child dataset's first dimension must be equal to the number of first dimension of the "index" dataset
                    Dataset["statistics"]: summary statistics for each skeleton
                     .attrs[""] -> named axes, named columns

            Group["properties"]: dataset's first dimension must be N
                Dataset["labels"] -> Nx1 array of labels. JSON-encoded metadata string encodes semantics
                 .attrs["semantics"] = "{1 : {"name" : "axonal arbor"}, 2 : {"name" : "dendritic arbor"}, 3 : {"name" : "cell body"} }"
            Dataset["data"] -> stores spatial location in Nx3 array

Example code to create the dataset node::

    import numpy as np
    import json
    import h5py
    myfile = h5py.File('ff.h5')

    dset = myfile.create_group("3D Skeletons")
    vert = dset.create_group("vertices")

    vert.create_dataset("data", data=np.random.random((10,3)))

    vert.create_group("properties")
    vert["properties"].create_dataset("labels", data=np.random.random_integers(1,3,(10,)))
    vert["properties"]["labels"].attrs["semantics"] = json.dumps({1 : {"name" : "axonal arbor"}, 2 : {"name" : "dendritic arbor"}, 3 : {"name" : "cell body"} })

    vert.create_group("grouping")
    vert["grouping"].create_dataset("index", data=np.array([[200,0,4],[300,5,9]]))

    con = vert.create_group("connectivity")
    con.create_dataset("data", data=np.array(range(10)))

    myfile.close()

Example code to create 3D skeleton dataset node from a set of SWC files::

A helper function to extract a subarray based on a given id using the index dataset of a grouping::

    def extract_array( grouping_index, dataset, value ):
        idx = grouping_index.value
        residx = np.where(idx[:,0] == value)[0]
        if len(residx) == 0:
            print("Value ID not found in group_index")
            return
        elif len(residx) > 1:
            print("Multiple value IDs foud in group_index")
            return
        else:
            validx = residx[0]
        fromidx = idx[validx, 1]
        toidx = idx[validx, 2]
        return dataset[fromidx:(toidx+1),:]

3D skeletons with changing vertices location
--------------------------------------------
The vertices location changes over time, but not the number of vertices. The connectivity stays the same.

3D skeletons with changing vertices location and number
-------------------------------------------------------
The number of vertices as well as the location changes over time. The connectivity has to be defined for each time frame as well.

3D skeletons with changing connectivity properties
--------------------------------------------------
The number of vertices and location is constant, the number of connections is constant, but the connectivity properties
change over time.

Microcircuit
------------
Consisting of a set of 3D skeletons, connectors and connectivity between skeletons and connectors

    Group["Microcircuitry"]

        # SOLUTION 1

        Group["vertices"]
        
            Dataset["data"]
            Group["properties"]
                Dataset["type"]
                .attrs = { 1 : "skeleton vertex", 2 : "connector vertex" }
                
            Group["connectivity"]
                Dataset["data"] -> contains parent and connector relations
                Group["properties"]
                    Dataset["type"]
                     .attrs = { 1 : "parent", 2 : "presynaptic", 3 : "postsynaptic" }
                Group["grouping"] -> groups the pre and post connectivity to the skeleton!
                    Dataset["index"]: SkeletonID | FromIndex | ToIndex


        # SOLUTION 2

        # A skeleton group as in example 1
        Group["Skeletons"]
            Group["vertices"]
            ...

        # A connector group
        Group["Connectors"]
            Group["vertices"]
                Dataset["data"]
                Group["properties"]
                    Dataset["labels"]
                     .attrs["semantics"] = "{1 : {"name" : "inhibitory"}, 2 : {"name" : "excitatory"} }"

        # A skeleton vertex - connector join array using ids
        Group["join"]
            Dataset["connectivity"] : Skeleton vertex ID or index? | Connector vertex ID or index?
            Group["properties"]
                Dataset["strength"]
                Dataset["synapsetype"]
            Group["grouping"]
                Dataset["index"] -> group joins according to skeleton id?

        # Common data query: For a given skeleton (ID), show all incoming/outgoing connectors.