Proposed Hierarchical Layout
============================
**Version 0.1**

A HDF5 file consist of a tree with group and dataset nodes. Each node can have attributes as key-value pairs.
Please refer to the `h5py documentation <>`_ for an introduction to the concepts and manipulation of HDF5 files.

In the following, we describe the way data is structured and laid-out as a NeuroHDF file using h5py. We make here
a proposal for a basic layout and core attributes, that can be customized.

First, we create a writable NeuroHDF file::

    import h5py
    myfile = h5py.File('firstfile.neurohdf')

Define global metadata pertaining to the purpose and content of the dataset::

    myfile.attrs["title"] = "A generic title"
    myfile.attrs["description"] = "A generic prose description of the content and purpose of the dataset"
    myfile.attrs["species"] = "The biological organism this dataset is representing in binomial form"
    myfile.attrs["creator"] = "The creator of the dataset including email"
    myfile.attrs["collaborators"] = "The collaborators related to the creation of the dataset"
    myfile.attrs["references"] = "Citation or URL reference for this dataset"

You need to be very clear about the type of data you want to store.

We represent the concept of a `spatial reference frame <>`_ in NeuroHDF as a *Region* HDF group node.
A Region node specifies as its metadata attributes:

* Coordinate system (origo and orientation), specified by an affine transformation (4D matrix)
* Oriented bounding box
* The semantics of origo
* The semantics of he +/- axes direction

A Region contains spatio-temporal datasets that are spatially transformed relative
to the local coordinate system defined by the Region. The datasets are either
regular or irregular . Regular datasets are fields defined on a regular grid, e.g.
2D images or 3D volumes. Irregular datasets are fields defined on their vertices and/or
their connectivity. Dataset group nodes specify metadata attributes:

Irregular datasets
* The affine transformation local to the Region they are contained in
* The unit strings for all axes after transformation
* An axis-aligned boundings box relative to the Region
The semantics of the field on the irregular spatio-temporal datastructure
is stored in the vertices/connectivity property node's metadata attributes.

Mapping to irregular datasets are defined for:
* 3D skeletons
* 2D contours
* M-to-N connectors with spatial location between skeletons
* surface meshes
* line strips (a special case of 3D skeletons)

Regular datasets (Homogeneous nd-arrays)
* The affine transformation from "voxel" space to Region space ?
  (The scaling defines the resolution)
* Need another affine?
* The unit strings for all axes after transformation
* An axis-aligned boundings box relative to the Region
* The semantics of the axes (after or before transformation?)

A distinction has to be made between the spatial datastructure that changes over time
vs. the fields defined over the fixed spatial datastructures that change over time.

What is the data model and philosophy adopted for NeuroHDF?

Do you have ...

    ..data in some spatial reference frame (i.e. there exists a well-defined origo and coordinate system)?
        ..yes
            ..is the underlying spatial structure of the data regular (on a grid) or irregular (vertices/connectivity)?

            ..does one aspect of the data have temporal extension?
                ..yes
                ..no

        ..no
            ..does it have spatial structure?
                ..yes
                    Genetic Expression Profile
                ..no
                    ..do multiple timepoints exist for on aspect/does one aspect of the data have temporal extension?
                        ..yes
                            Dynamic Network/Graph
                        ..no
                            Static Network/Graph


Real life scientific example datasets
-------------------------------------
* Biophysically realistic simulation of voltage across a neuronal morphology
  - Irregular 3D skeleton consisting of vertices and connectivity (segments)
  - Properties on the vertices and/or segments such as ion channel distributions etc.
  - Group of multiple trials with different initial condition and stimulation parameters
    - (Segment, time) array with voltage values across time.
    - (Stimulus, time) array representing the stimulus applied at specific timepoints, e.g. to segments

* Reconstructed skeletonized microcircuitry from electron microscopy
  - Sets of irregular 3D skeletons in a spatial reference system
  - Sets of connectors with location representing synapses connecting vertices of the 3D skeletons

* Full volume neuropile reconstruction from electron microscopy
  - Regular 3D grid segmenting the structures in a spatial reference system
  - Sets of area lists representing structures

* Behavioral experiments of tracked animals moving on a 2D plate
  - Irregular spatio-temporal data in a spatial reference system

* Cell division, differentiation and migration data in 3D (lineages)

* Confocal optical microcopy imaging
  - Sets of regular 2D grid images with multiple channels

* Spiking network simulation with point neurons

* Neurophysiological extracellular recordings
  - Regular 2D grid (? non spatial) - in concepto-temporal system
  - (Unit, time) array of voltage traces

* Neurophysiological intracellular recordings

* Gene expression array of genes assayed in a spatial volume
  for a particular genotypic state, physiological state, developmental stage,
  after perturbation with different set of parameters

* Network of brain regions and their connectivity

* Network of neurons and their connectivity (circuit diagram)

* Network of neuron classes and their connection probability (circuit diagram)

* Functional MRI dataset
  - Regular 3D grid with time steps in spatial reference system

* Structural MRI dataset
  - Regular 3D grid in spatial reference system

* Tractography dataset
  - Irregular 3D data in spatial reference system

* Diffusion MRI dataset
  - Regular 3D grid in spatial reference system with a number of gradient directions
  - Parameters: bvalues, bvectors

* Reconstructed surface of cortical and subcortical structures with atlas labels
  - Irregular 3D dataset with vertices and triangular faces in spatial reference system
  - (labels,) array with the length of the vertices
