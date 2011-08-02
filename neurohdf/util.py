import numpy as np

def extract_array( grouping_index, dataset, value ):
    """
    Extracts a subarray of a dataset using an index.
    This is a form of fancy indexing operation with NeuroHDF conventions

    Parameters
    ----------
    grouping_index : h5py dataset
        The index dataset of a grouping Group
    dataset : h5py dataset
        The related dataset where this grouping index refers to
    value : int
        The integer id, the first column of the index dataset.
        The second and third column need to be start and end index
        using a zero-based index

    Returns
    -------
    array : nd-array
        The subarray requested or None when value not found as id

    """
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