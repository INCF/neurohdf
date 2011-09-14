.. _datatypes:

Variety of neuroscience dataset types
-------------------------------------

If you think a basic dataset type is missing, `please add them <https://github.com/INCF/neurohdf/issues/1>`_!

Anatomy
^^^^^^^

* Reconstructed skeletonized microcircuitry from electron microscopy

  * Sets of irregular 3D skeletons in a spatial reference system
  * Sets of connectors with location representing synapses connecting vertices of the 3D skeletons

* Dense reconstruction of neuropile from electron microscopy

  * Regular 3D grid segmenting the structures in a spatial reference system
  * Sets of area lists representing structures
  * Sets of surface meshes representing structures

* Confocal optical microcopy imaging

  * Sets of regular 2D grid images with multiple channels

* Network of brain regions and their connectivity

* Network of neurons and their connectivity (circuit diagram)

* Network of neuron classes and their connection probability (circuit diagram)

Microscopy
``````````
Standardized, open formats

* Open Microscopy Environment (OME): `Metadata matters: access to image data in the real world <http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2878938/?tool=pubmed>`_

Simulation
^^^^^^^^^^

* Biophysically realistic simulation of voltage across a neuronal morphology

  * Irregular 3D skeleton consisting of vertices and connectivity (segments)
  * Properties on the vertices and/or segments such as ion channel distributions etc.
  * Group of multiple trials with different initial condition and stimulation parameters

    * (Segment, time) array with voltage values across time.
    * (Stimulus, time) array representing the stimulus applied at specific timepoints, e.g. to segments

* Spiking network simulation with point neurons

Software writing HDF5:

* `neuroConstruct <http://www.neuroconstruct.org/>`_

Behavior
^^^^^^^^

* Behavioral experiments of tracked animals moving on a 2D plate

  * Irregular spatio-temporal data in a spatial reference system

* Questionnaire results


Development
^^^^^^^^^^^

* Cell lineages: Cell division, differentiation and migration data in 3D

Physiology
^^^^^^^^^^

* Neurophysiological extracellular recordings

  * Regular 2D grid (? non spatial) - in concepto-temporal system
  * (Unit, time) array of voltage traces

* Neurophysiological intracellular recordings

* Spectro-temporal receptive fields

* Functions: Intensity-response function of neurons, Tuning curves, ...

Software writing HDF5:

* `stimfit <http://code.google.com/p/stimfit/>`_


Genomics/Proteomics
^^^^^^^^^^^^^^^^^^^

* Gene expression array of genes assayed in a spatial volume
  for a particular genotypic state, physiological state, developmental stage,
  after perturbation with different set of parameters

Neuroimaging
^^^^^^^^^^^^

* Functional MRI dataset
  - Regular 3D grid with time steps in spatial reference system

* Structural MRI dataset
  - Regular 3D grid in spatial reference system

* Tractography dataset
  - Irregular 3D data in spatial reference system

* Diffusion MRI dataset
  - Regular 3D grid in spatial reference system with a number of gradient directions
  - Parameters: bvalues, bvectors

* Reconstructed macroscale surfaces of cortical and subcortical structures with atlas labels
  - Irregular 3D dataset with vertices and triangular faces in spatial reference system
  - (labels,) array with the length of the vertices

* MRI datasets (PET, ...)

* EEG dataset

* MEG dataset

NIRS dataset
````````````
`INCF: Development of a standard file format for NIRS <http://datasharing.incf.org/ni/NIRS>`_