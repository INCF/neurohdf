

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
    vert["properties"]["labels"].attrs["semantics"] = json.dumps({
        1 : {"name" : "axonal arbor"},
        2 : {"name" : "dendritic arbor"},
        3 : {"name" : "cell body"} })

    vert.create_group("grouping")
    vert["grouping"].create_dataset("index", data=np.array([[200,0,4],[300,5,9]]))

    con = vert.create_group("connectivity")
    con.create_dataset("data", data=np.array(range(10)))

    myfile.close()
